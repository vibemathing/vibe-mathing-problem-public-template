#!/usr/bin/env python3
"""经审查的 npm:pi-goal-x@0.31.9 前镜像 → 项目忽略缓存补丁；拒绝未知镜像。

先由 Pi 官方 `pi install --local npm:pi-goal-x@0.31.9` 安装到项目缓存。
运行：python3 scripts/install_goal_patch.py --project-root . --apply|--check
只修改本仓库的 .pi/npm；不删旧包/半成品，失败保留 stage 供隔离排查。
"""
from __future__ import annotations
import argparse
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
    for path in sorted(package.rglob('*')):
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


def install(root: Path, apply: bool) -> str:
    if root.is_symlink() or not root.is_dir() or root.resolve() != root:
        raise ValueError('project root must be a real absolute directory')
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
    identity = json.loads((package / 'package.json').read_text())
    if identity.get('name') != 'pi-goal-x' or identity.get('version') != '0.31.9' or identity.get('license') != 'MIT':
        raise ValueError('Goal package identity drift')
    length, digest = inventory(package)
    if (length, digest) == (metadata['patched_files'], metadata['patched_tree_sha256']):
        return 'PATCHED_VERIFIED'
    if (length, digest) != (metadata['upstream_files'], metadata['upstream_tree_sha256']):
        raise ValueError('unknown Goal package preimage; no files changed')
    if not apply:
        raise ValueError('Goal package remains upstream; run --apply before starting Pi')
    stage = npm / ('.goal-patch-stage-' + uuid.uuid4().hex)
    backup = npm / ('.goal-patch-upstream-' + uuid.uuid4().hex)
    shutil.copytree(package, stage, symlinks=True)
    # 修改严格局限于 stage。外部 patch 在无 fuzz/无逆向模式下重放固定 diff。
    result = subprocess.run(['patch', '--batch', '--forward', '--fuzz=0', '-p1', '-d', str(stage), '-i', str(patch)],
                            capture_output=True, text=True, timeout=15, check=False)
    if result.returncode != 0 or inventory(stage) != (metadata['patched_files'], metadata['patched_tree_sha256']):
        raise ValueError('Goal patch failed; original cache unchanged, stage retained')
    os.rename(package, backup)
    try:
        os.rename(stage, package)
    except BaseException:
        os.rename(backup, package)
        raise
    if inventory(package) != (metadata['patched_files'], metadata['patched_tree_sha256']):
        raise RuntimeError('Goal installed readback drift; original retained in ignored backup')
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
