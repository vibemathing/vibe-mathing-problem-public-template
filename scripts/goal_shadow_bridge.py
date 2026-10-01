#!/usr/bin/env python3
"""显式 sealed-pair-v1 checkpoint/index owner 只读校验 → 独立影子库。

只支持此版本的 pair owner；母版 report_local_checkpoint.py 不提供此格式，
不能把任意 JSON、Goal 恢复或数学证据伪装成可恢复的 pair。
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from functools import wraps
import hashlib
import json
import math
import os
from pathlib import Path
import re
import signal
import sqlite3
import stat
import sys
import threading
from urllib.parse import quote

if __name__ == '__main__' and sys.flags.isolated:
    # -I -S 不加载脚本目录或 user-site；唯一项目依赖由固定同级路径显式装载。
    from importlib.util import module_from_spec, spec_from_file_location
    store_path = Path(__file__).with_name('goal_snapshot_store.py')
    if store_path.is_symlink() or not store_path.is_file():
        raise ValueError('冻结存储模块路径无效')
    spec = spec_from_file_location('goal_snapshot_store', store_path)
    if spec is None or spec.loader is None:
        raise ValueError('冻结存储模块无法加载')
    module = module_from_spec(spec)
    sys.modules['goal_snapshot_store'] = module
    spec.loader.exec_module(module)

from goal_snapshot_store import BINDINGS, KEY, MAX_BYTES, SHA, SnapshotStore, sha

OWNER_MARKER = 'OPEN-PROBLEM-CHECKPOINT-COMMIT-V1'
INDEX_SCHEMA = 'sealed-candidate-pair-index.v1'
CONFIG_SCHEMA = 'sealed-pair-shadow.v1'
CONFIG_KEYS = {'schema_version', *BINDINGS, 'repository_root', 'runtime_root',
               'checkpoint', 'index', 'shadow_root', 'restore_root'}
MAX_MANIFEST_FILES = 128
MAX_MANIFEST_BYTES = 48 * 1024 * 1024
MAX_PAIR_BYTES = 64 * 1024 * 1024
MAX_OPERATION_SECONDS = 40


@contextmanager
def operation_budget():
    """直接调用和 CLI 都有墙钟上限；中断 SQLite 未提交事务，绝不伪报成功。"""
    if threading.current_thread() is not threading.main_thread():
        raise ValueError('影子操作只允许在主线程执行')
    if signal.getitimer(signal.ITIMER_REAL)[0]:
        raise ValueError('已有 SIGALRM 计时器，拒绝覆盖')
    previous = signal.getsignal(signal.SIGALRM)
    def timeout(_signal, _frame):
        raise TimeoutError('影子操作总时间超限')
    signal.signal(signal.SIGALRM, timeout)
    signal.setitimer(signal.ITIMER_REAL, MAX_OPERATION_SECONDS)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)


def bounded(fn):
    @wraps(fn)
    def run(*args, **kwargs):
        with operation_budget():
            return fn(*args, **kwargs)
    return run


def strict_json(raw: bytes):
    def pairs(items):
        result = {}
        for k, v in items:
            if k in result:
                raise ValueError('重复 JSON key')
            result[k] = v
        return result
    def finite_float(text):
        number = float(text)
        if not math.isfinite(number):
            raise ValueError('非有限 JSON 数值')
        return number
    value = json.loads(raw.decode('utf8'), object_pairs_hook=pairs, parse_float=finite_float,
                       parse_constant=lambda _: (_ for _ in ()).throw(ValueError('非标准 JSON 数值')))
    if not isinstance(value, dict):
        raise ValueError('JSON 顶层必须是对象')
    return value


def safe_path(raw: str, *, root: Path | None = None) -> Path:
    if not isinstance(raw, str):
        raise ValueError('路径必须是字符串')
    path = Path(raw)
    if not path.is_absolute() or '..' in path.parts or any(p == '' for p in path.parts):
        raise ValueError('路径必须是无越界分量的绝对路径')
    if root is not None and not path.is_relative_to(root):
        raise ValueError('路径越出冻结根')
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ValueError('路径含符号链接')
    return path


def private_dir(path: Path) -> None:
    path = safe_path(str(path))
    info = path.stat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
        raise ValueError('影子/恢复目录必须预先存在且 owner-only')


def read_source(path: Path) -> tuple[bytes, tuple[int, int, int, int, int]]:
    """O_NOFOLLOW + 有界单次读取；同一描述符前后 fstat，拒绝就地变动。"""
    safe_path(str(path))
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        a = os.fstat(fd)
        if not stat.S_ISREG(a.st_mode) or a.st_uid != os.getuid():
            raise ValueError('来源必须是 owner 普通文件')
        data = bytearray()
        while len(data) <= MAX_BYTES:
            chunk = os.read(fd, min(1024 * 1024, MAX_BYTES + 1 - len(data)))
            if not chunk:
                break
            data.extend(chunk)
        b = os.fstat(fd)
        left = (a.st_dev, a.st_ino, a.st_size, a.st_mtime_ns, a.st_ctime_ns)
        right = (b.st_dev, b.st_ino, b.st_size, b.st_mtime_ns, b.st_ctime_ns)
        if left != right or b.st_size != len(data):
            raise ValueError('来源并发变化')
        if len(data) > MAX_BYTES:
            raise ValueError('来源超过上限')
        return bytes(data), right
    finally:
        os.close(fd)


def config_file(path: Path, expected_config_sha256: str | None = None) -> dict:
    path = safe_path(str(path))
    s = path.stat()
    if not stat.S_ISREG(s.st_mode) or s.st_uid != os.getuid() or s.st_mode & 0o077:
        raise ValueError('配置必须为 owner-only 普通文件')
    data, fingerprint = read_source(path)
    if len(data) > 16 * 1024:
        raise ValueError('配置字节超限')
    if expected_config_sha256 is not None and (not SHA.fullmatch(expected_config_sha256) or
                                               sha(data) != expected_config_sha256):
        raise ValueError('命令入口冻结配置与 Python 配置不一致')
    cfg = strict_json(data)
    if set(cfg) != CONFIG_KEYS or cfg['schema_version'] != CONFIG_SCHEMA:
        raise ValueError('不支持的配置格式')
    for key in BINDINGS:
        value = cfg[key]
        if not isinstance(value, str) or (key == 'problem_id' and not value.startswith('problem:')) or (key != 'problem_id' and not SHA.fullmatch(value)):
            raise ValueError('冻结身份无效: ' + key)
    for key in ('repository_root', 'runtime_root', 'shadow_root', 'restore_root'):
        cfg[key] = safe_path(cfg[key])
    if cfg['repository_root'].parent != cfg['runtime_root'].parent:
        raise ValueError('repository/runtime owner 目录不相邻')
    cfg['checkpoint'] = safe_path(cfg['checkpoint'], root=cfg['runtime_root'])
    cfg['index'] = safe_path(cfg['index'], root=cfg['repository_root'])
    for key in ('shadow_root', 'restore_root'):
        private_dir(cfg[key])
    for output in (cfg['shadow_root'], cfg['restore_root']):
        for original in (cfg['repository_root'], cfg['runtime_root']):
            if output.is_relative_to(original) or original.is_relative_to(output):
                raise ValueError('影子/恢复目录不能包含或处于原始研究目录')
    if cfg['shadow_root'] == cfg['restore_root'] or cfg['shadow_root'].is_relative_to(cfg['restore_root']) or cfg['restore_root'].is_relative_to(cfg['shadow_root']):
        raise ValueError('影子库与恢复目录不得嵌套')
    for key in ('repository_root', 'runtime_root'):
        if not cfg[key].is_dir():
            raise ValueError('冻结来源根不存在')
    cfg['_config_input'] = (path, data, fingerprint)
    return cfg


def check_config_input(cfg):
    path, data, fingerprint = cfg['_config_input']
    now, state = read_source(path)
    if data != now or fingerprint != state:
        raise ValueError('配置并发变化；拒绝继续')


def binding(cfg):
    return {k: cfg[k] for k in BINDINGS}


def relative_artifact(locator: str) -> Path:
    if not isinstance(locator, str) or not locator or '\\' in locator:
        raise ValueError('manifest locator 非法')
    path = Path(locator)
    if path.is_absolute() or '..' in path.parts or path.as_posix() != locator:
        raise ValueError('manifest locator 越界')
    return path


def validate_pair(cfg: dict, checkpoint: bytes, index: bytes, *, artifacts: bool) -> list[tuple[Path, bytes, tuple[int, int, int, int, int]]]:
    if len(checkpoint) + len(index) > MAX_PAIR_BYTES:
        raise ValueError('双文档总字节超限')
    cp, idx = strict_json(checkpoint), strict_json(index)
    for key, expected in binding(cfg).items():
        if cp.get(key) != expected or idx.get(key) != expected:
            raise ValueError('checkpoint/index 冻结身份错配: ' + key)
    if cp.get('schema_version') != '1.0.0' or idx.get('schema_version') != INDEX_SCHEMA:
        raise ValueError('未知 sealed-pair-v1 owner 文档格式')
    if idx.get('candidate_only') is not True or idx.get('claim_ceiling') != 'candidate_only':
        raise ValueError('候选文档不得晋升准入')
    if not isinstance(cp.get('sequence'), int) or isinstance(cp.get('sequence'), bool) or cp['sequence'] <= 0 or type(idx.get('sequence')) is not int or idx['sequence'] != cp['sequence']:
        raise ValueError('checkpoint/index 序列错配')
    expected_locator = 'runtime/' + cfg['checkpoint'].relative_to(cfg['runtime_root']).as_posix()
    if idx.get('latest_checkpoint') != expected_locator or not isinstance(cp.get('state_vector'), dict) or cp['state_vector'].get('claim_boundary') != 'candidate_only':
        raise ValueError('checkpoint locator 或 candidate 边界错配')
    seal = cp.get('integrity')
    if not isinstance(seal, dict) or set(seal) != {'commit_marker', 'payload_sha256'} or seal['commit_marker'] != OWNER_MARKER:
        raise ValueError('未知/缺失 owner checkpoint integrity')
    payload = {k: v for k, v in cp.items() if k != 'integrity'}
    expected = sha(json.dumps(payload, sort_keys=True, separators=(',', ':'), allow_nan=False).encode())
    if seal['payload_sha256'] != expected:
        raise ValueError('owner checkpoint integrity 无效，不得重签')
    manifest = cp.get('artifact_manifest')
    if not isinstance(manifest, dict) or not {'locator', 'sha256', 'bytes', 'files'} <= set(manifest) or type(manifest['files']) is not int or manifest['files'] != 1:
        raise ValueError('未知/无效 owner artifact_manifest')
    items = [manifest] + (manifest.get('supplementary', []) if isinstance(manifest.get('supplementary', []), list) else [None])
    if len(items) > MAX_MANIFEST_FILES:
        raise ValueError('owner manifest 总文件数超限')
    total = len(checkpoint) + len(index)
    entries = []
    seen_locators: set[str] = set()
    for item in items:
        if not isinstance(item, dict) or not {'locator', 'sha256', 'bytes'} <= set(item) or not SHA.fullmatch(str(item['sha256'])) or type(item['bytes']) is not int or item['bytes'] < 0:
            raise ValueError('owner manifest 条目无效')
        relative = relative_artifact(item['locator'])
        if item['locator'] in seen_locators:
            raise ValueError('owner manifest locator 重复')
        seen_locators.add(item['locator'])
        path = safe_path(str(cfg['repository_root'] / relative), root=cfg['repository_root'])
        total += item['bytes']
        if total > MAX_MANIFEST_BYTES:
            raise ValueError('owner manifest 总字节超限')
        entries.append((path, item))
    observations = []
    if artifacts:
        for path, item in entries:
            raw, fingerprint = read_source(path)
            if len(raw) != item['bytes'] or sha(raw) != item['sha256']:
                raise ValueError('owner artifact_manifest 字节或摘要变化')
            # 已检验的 A 才是冻结基线；不能再次读取 B 后把 B 当作新真相。
            observations.append((path, raw, fingerprint))
    return observations


def stable_sources(cfg):
    cp, cp_stat = read_source(cfg['checkpoint'])
    idx, idx_stat = read_source(cfg['index'])
    artifacts = validate_pair(cfg, cp, idx, artifacts=True)
    # 源与附件必须与首次已验证字节及 inode/mtime/ctime 相同，绝不另立基线。
    originals = [(cfg['checkpoint'], cp, cp_stat), (cfg['index'], idx, idx_stat), *artifacts]
    def verify():
        for path, data, fingerprint in originals:
            fresh, current = read_source(path)
            if fresh != data or current != fingerprint:
                raise ValueError('来源并发变化；拒绝发布影子快照')
    verify()
    return cp, idx, verify


@bounded
def save(config: Path, name: str, parent: str | None, *, expected_config_sha256: str | None = None):
    cfg = config_file(config, expected_config_sha256)
    if not KEY.fullmatch(name) or parent is not None and not KEY.fullmatch(parent):
        raise ValueError('快照 ID 无效')
    cp, idx, precommit_sources = stable_sources(cfg)
    db = cfg['shadow_root'] / 'snapshots.sqlite'
    if db.exists() and (db.is_symlink() or not db.is_file() or db.stat().st_uid != os.getuid() or db.stat().st_mode & 0o077):
        raise ValueError('影子数据库权限无效')
    check_config_input(cfg)
    store = SnapshotStore(db, binding(cfg))
    try:
        def precommit():
            check_config_input(cfg)
            precommit_sources()
        return {**store.save(name, cp, idx, parent=parent, precommit=precommit), 'candidate_only': True}
    finally:
        store.close()


@bounded
def restore(config: Path, name: str, destination: str, *, expected_config_sha256: str | None = None):
    cfg = config_file(config, expected_config_sha256)
    if not KEY.fullmatch(name) or not KEY.fullmatch(destination) or destination.startswith('.'):
        raise ValueError('快照或恢复目录名无效')
    db = cfg['shadow_root'] / 'snapshots.sqlite'
    if not db.is_file() or db.is_symlink() or db.stat().st_uid != os.getuid() or db.stat().st_mode & 0o077:
        raise ValueError('影子数据库不存在或权限无效')
    store = SnapshotStore(db, binding(cfg))
    try:
        cp, idx = store.restore(name)
        validate_pair(cfg, cp, idx, artifacts=False)
    finally:
        store.close()
    check_config_input(cfg)
    target = cfg['restore_root'] / destination
    target.mkdir(mode=0o700, exist_ok=False)
    # 恢复只创建全新目录；不可重放到原文件或 active locator。
    for basename, data in (('checkpoint.json', cp), ('index.json', idx)):
        fd = os.open(target / basename, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, 'wb') as out:
            out.write(data)
            out.flush()
            os.fsync(out.fileno())
    fd = os.open(target, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    return {'snapshot': name, 'output': str(target), 'candidate_only': True, 'original_recovery_head_changed': False}


@bounded
def status(config: Path, *, expected_config_sha256: str | None = None):
    cfg = config_file(config, expected_config_sha256)
    db = cfg['shadow_root'] / 'snapshots.sqlite'
    if not db.exists():
        return {'configured': True, 'shadow_exists': False, 'snapshots': 0, 'candidate_only': True}
    db = safe_path(str(db), root=cfg['shadow_root'])
    if not db.is_file() or db.stat().st_uid != os.getuid() or db.stat().st_mode & 0o077:
        raise ValueError('影子数据库权限无效')
    connection = sqlite3.connect('file:' + quote(str(db)) + '?mode=ro', uri=True, timeout=5)
    try:
        identity = connection.execute('SELECT binding FROM identity LIMIT 2').fetchall()
        if identity != [(json.dumps(binding(cfg), sort_keys=True),)]:
            raise ValueError('影子数据库绑定不匹配')
        count = connection.execute('SELECT COUNT(*) FROM snapshots').fetchone()[0]
    finally:
        connection.close()
    return {'configured': True, 'shadow_exists': True, 'snapshots': count, 'candidate_only': True}


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', required=True, type=Path)
    parser.add_argument('--expected-config-sha256', help='命令入口已验证的配置字节 SHA-256')
    commands = parser.add_subparsers(dest='op', required=True)
    commands.add_parser('status')
    s = commands.add_parser('save'); s.add_argument('name'); s.add_argument('parent', nargs='?')
    r = commands.add_parser('restore'); r.add_argument('name'); r.add_argument('destination')
    args = parser.parse_args()
    try:
        result = (status(args.config, expected_config_sha256=args.expected_config_sha256) if args.op == 'status' else
                  save(args.config, args.name, args.parent, expected_config_sha256=args.expected_config_sha256) if args.op == 'save' else
                  restore(args.config, args.name, args.destination, expected_config_sha256=args.expected_config_sha256))
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, sqlite3.Error) as exc:
        print('shadow snapshot BLOCK: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
