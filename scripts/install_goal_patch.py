#!/usr/bin/env python3
"""经审查的 npm:pi-goal-x@0.31.9 前镜像 → 项目忽略缓存补丁；拒绝未知镜像。

先由 Pi 官方 `pi install --local npm:pi-goal-x@0.31.9` 安装到项目缓存。
运行：python3 scripts/install_goal_patch.py --project-root . --apply|--check
只修改本仓库的 .pi/npm；不删旧包/半成品，失败保留 stage/quarantine 供隔离排查。
两个目录 rename 不是跨崩溃原子事务：若进程恰在两次 rename 间退出，
原件仍在 `.pi/npm/.goal-patch-upstream-*`；禁止盲目重装，须先离线核对备份再恢复。
"""
from __future__ import annotations
import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import uuid


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def inventory(package: Path) -> tuple[int, str]:
    rows = []
    if package.is_symlink() or not package.is_dir():
        raise ValueError('Goal npm cache is not a real package directory')
    for path in (package, *sorted(package.rglob('*'))):
        info = path.lstat()
        if not (stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode)) or info.st_uid != os.getuid() or info.st_mode & 0o022:
            raise ValueError('Goal package member is not owner-controlled regular data')
        if stat.S_ISDIR(info.st_mode):
            continue
        if info.st_size > 5_000_000:
            raise ValueError('Goal package member exceeds bound')
        data = path.read_bytes()
        rows.append({'path': path.relative_to(package).as_posix(), 'bytes': len(data), 'sha256': sha(data)})
    return len(rows), sha(json.dumps(rows, sort_keys=True, separators=(',', ':')).encode())


def tree_state(package: Path) -> tuple:
    """确认准备过程未替换 inode，也未就地重写后还原相同字节。"""
    rows = []
    for path in (package, *sorted(package.rglob('*'))):
        info = path.lstat()
        rows.append((path.relative_to(package).as_posix(), info.st_dev, info.st_ino,
                     info.st_mode, info.st_size, info.st_mtime_ns, info.st_ctime_ns))
    return tuple(rows)


@contextmanager
def install_lock(npm: Path):
    """仅协调使用本安装器的同一缓存写入；非协作 writer 须靠发布前复读。"""
    lock = npm / '.goal-patch-install.lock'
    fd = os.open(lock, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600)
    try:
        info = os.fstat(fd)
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or
                info.st_nlink != 1 or info.st_mode & 0o077 or info.st_size):
            raise ValueError('Goal install lock must be an empty owner-only regular file')
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise ValueError('another Goal installer owns the cache lock') from exc
        yield
    finally:
        os.close(fd)


def install(root: Path, apply: bool) -> str:
    # . 为受信 cwd 的正常入口；拒绝词法越界及任何实际符号链接分量。
    if '..' in root.parts or root.is_symlink():
        raise ValueError('unsafe project root')
    root = root.absolute()
    if not root.is_dir() or root.resolve() != root:
        raise ValueError('project root must be a real directory without symlinks')
    metadata = json.loads((root / 'governance/control-plane/pi-goal-upstream.v1.json').read_text())
    patch = root / metadata['patch_file']
    if patch.is_symlink() or sha(patch.read_bytes()) != metadata['patch_sha256']:
        raise ValueError('reviewed patch drift')
    settings = json.loads((root / '.pi/settings.json').read_text())
    if settings.get('packages') != [metadata['package']]:
        raise ValueError('Pi project package declaration drift')
    npm = root / '.pi/npm'
    modules = npm / 'node_modules'
    package = modules / 'pi-goal-x'
    for folder in (root / '.pi', npm, modules):
        if folder.is_symlink() or not folder.is_dir() or folder.stat().st_uid != os.getuid() or folder.stat().st_mode & 0o022:
            raise ValueError('untrusted Pi npm cache directory')
    ignored = subprocess.run(['git', '-C', str(root), 'check-ignore', '-q', '--', '.pi/npm/.probe'], check=False)
    tracked = subprocess.run(['git', '-C', str(root), 'ls-files', '-z', '--', '.pi/npm'], capture_output=True, check=False)
    if ignored.returncode != 0 or tracked.returncode != 0 or tracked.stdout:
        raise ValueError('Goal npm cache must be Git-ignored and untracked')
    with install_lock(npm):
        preimage = inventory(package)
        identity = json.loads((package / 'package.json').read_text())
        if identity.get('name') != 'pi-goal-x' or identity.get('version') != '0.31.9' or identity.get('license') != 'MIT':
            raise ValueError('Goal package identity drift')
        state = tree_state(package)
        if preimage != inventory(package) or state != tree_state(package):
            raise ValueError('Goal package changed while reading the preimage')
        if preimage == (metadata['patched_files'], metadata['patched_tree_sha256']):
            return 'PATCHED_VERIFIED'
        if preimage != (metadata['upstream_files'], metadata['upstream_tree_sha256']):
            raise ValueError('unknown Goal package preimage; no files changed')
        if not apply:
            raise ValueError('Goal package remains upstream; run --apply before starting Pi')
        stage = npm / ('.goal-patch-stage-' + uuid.uuid4().hex)
        backup = npm / ('.goal-patch-upstream-' + uuid.uuid4().hex)
        shutil.copytree(package, stage, symlinks=True)
        # 修改严格局限于 stage。外部 patch 在无 fuzz/无逆向模式下重放固定 diff。
        result = subprocess.run(['patch', '--batch', '--forward', '--fuzz=0', '-p1', '-d', str(stage), '-i', str(patch)],
                                capture_output=True, text=True, timeout=15, check=False)
        expected = (metadata['patched_files'], metadata['patched_tree_sha256'])
        if result.returncode != 0 or inventory(stage) != expected:
            raise ValueError('Goal patch failed; original cache unchanged, stage retained')
        # 协作安装受 flock 保护；非协作写入则在最后一步逐字节和 inode 双重复读。
        # 最终复读与 rename 之间仍有不可消除的非协作 writer 窗口。
        if inventory(package) != preimage or tree_state(package) != state:
            raise ValueError('Goal package preimage changed before promotion; current owner bytes preserved')
        if backup.exists() or backup.is_symlink():
            raise ValueError('Goal backup target unexpectedly exists')
        os.rename(package, backup)
        try:
            os.rename(stage, package)
            if inventory(package) != expected:
                raise RuntimeError('Goal installed readback drift')
        except BaseException as failure:
            # 第一 rename 后的失败：旧树在 backup。绝不覆盖当前失败镜像。
            if package.exists() or package.is_symlink():
                quarantine = npm / ('.goal-patch-failed-' + uuid.uuid4().hex)
                try:
                    os.rename(package, quarantine)
                except BaseException as exc:
                    raise RuntimeError('Goal rollback blocked; original retained in upstream backup') from exc
            if package.exists() or package.is_symlink():
                raise RuntimeError('Goal rollback blocked by a concurrent target; original retained in upstream backup')
            try:
                os.rename(backup, package)
            except BaseException as exc:
                raise RuntimeError('Goal rollback blocked; original retained in upstream backup') from exc
            raise failure
        return 'PATCHED_VERIFIED'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-root', type=Path, required=True)
    operation = parser.add_mutually_exclusive_group(required=True)
    operation.add_argument('--check', action='store_true')
    operation.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    try:
        print('Goal install: ' + install(args.project_root, args.apply))
        return 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError, subprocess.TimeoutExpired) as error:
        print('Goal install: BLOCK (' + type(error).__name__ + ')', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
