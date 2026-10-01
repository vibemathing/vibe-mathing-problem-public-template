#!/usr/bin/env python3
"""sealed-pair-v1 只读源的无损影子存储：SQLite 事务 + zstd 有界差量；不是数学准入。"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import sqlite3
import subprocess
import tempfile

MAX_BYTES = 32 * 1024 * 1024
MAX_DEPTH = 8
SHA = re.compile(r'[0-9a-f]{64}\Z')
KEY = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,119}\Z')
BINDINGS = ('problem_id', 'problem_contract_sha256', 'statement_sha256')


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def encode(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()


def read_input(path: Path) -> bytes:
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as stream:
        data = stream.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError('输入超过单文档上限')
    return data


class SnapshotStore:
    def __init__(self, path: Path, binding: dict):
        self.path = Path(path).absolute()
        self.binding = {k: binding[k] for k in BINDINGS}
        if any(p.is_symlink() for p in (self.path, *self.path.parents)):
            raise ValueError('存储路径不得经过符号链接')
        if not self.path.parent.is_dir():
            raise ValueError('存储父目录须预先存在')
        if self.path.parent.stat().st_mode & 0o077:
            raise ValueError('存储父目录须为 owner-only')
        if self.path.exists() and (not self.path.is_file() or self.path.stat().st_mode & 0o077):
            raise ValueError('存储文件须为 owner-only 普通文件')
        if not self.path.exists():
            fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW, 0o600)
            os.close(fd)
        self.db = sqlite3.connect(self.path, timeout=5)
        self.db.execute('PRAGMA foreign_keys=ON')
        self.db.execute('PRAGMA synchronous=FULL')
        self.db.executescript('''
            CREATE TABLE IF NOT EXISTS identity(binding TEXT NOT NULL UNIQUE);
            CREATE TABLE IF NOT EXISTS objects(
                digest TEXT PRIMARY KEY, codec TEXT NOT NULL, payload BLOB NOT NULL,
                base TEXT REFERENCES objects(digest), depth INTEGER NOT NULL, raw_bytes INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS snapshots(
                position INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE,
                checkpoint TEXT NOT NULL REFERENCES objects(digest),
                idx TEXT NOT NULL REFERENCES objects(digest), parent TEXT REFERENCES snapshots(name));
        ''')
        identity = json.dumps(self.binding, sort_keys=True)
        try:
            self.db.execute('BEGIN IMMEDIATE')
            rows = self.db.execute('SELECT binding FROM identity').fetchall()
            if rows and rows != [(identity,)]:
                raise ValueError('存储绑定不匹配')
            if not rows:
                self.db.execute('INSERT INTO identity(binding) VALUES(?)', (identity,))
            self.db.commit()
        except BaseException:
            self.db.rollback()
            self.db.close()
            raise

    def close(self):
        self.db.close()

    def _codec(self, raw: bytes, base: bytes | None = None, *, decompress=False) -> bytes:
        # 原生成熟 codec，临时文件仅属于本次调用；操作完成后自动回收，不触碰历史输入。
        with tempfile.TemporaryDirectory(prefix='snapshot-codec-', dir=self.path.parent) as directory:
            root = Path(directory)
            command = ['/usr/bin/zstd', '-q', '-c', '--no-progress', '--memory=64MB']
            command += ['-d'] if decompress else ['-3', '--stream-size=' + str(len(raw))]
            if base is not None:
                fd = os.open(root / 'base', os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
                with os.fdopen(fd, 'wb') as output: output.write(base)
                command += ['--patch-from=' + str(root / 'base')]
            def limits():
                resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_BYTES * 2, MAX_BYTES * 2))
            fd = os.open(root / 'output', os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            with os.fdopen(fd, 'wb') as output:
                proc = subprocess.run(command, input=raw, stdout=output, stderr=subprocess.PIPE,
                                      timeout=30, preexec_fn=limits, env={'PATH': '/usr/bin:/bin', 'LC_ALL': 'C'})
            if proc.returncode:
                raise ValueError('zstd 编解码失败')
            result = (root / 'output').read_bytes()
            if decompress and len(result) > MAX_BYTES:
                raise ValueError('解码结果超过上限')
            return result

    def _select_encoding(self, raw: bytes, base_id: str | None):
        full = self._codec(raw)
        if base_id:
            row = self.db.execute('SELECT depth FROM objects WHERE digest=?', (base_id,)).fetchone()
            if row and row[0] < MAX_DEPTH:
                patch = self._codec(raw, self._load(base_id))
                # 差量至少减少20%才承担恢复依赖；深度到8后自动生成完整快照。
                if len(patch) < len(full) * 0.8:
                    return 'zstd-patch', patch, base_id, row[0] + 1
        return 'zstd', full, None, 0

    def _load(self, digest: str, seen=None) -> bytes:
        seen = set() if seen is None else seen
        if not SHA.fullmatch(digest) or digest in seen or len(seen) > MAX_DEPTH:
            raise ValueError('对象摘要/依赖链无效')
        seen.add(digest)
        row = self.db.execute('SELECT codec,payload,base,depth,raw_bytes FROM objects WHERE digest=?', (digest,)).fetchone()
        if not row:
            raise ValueError('对象缺失')
        codec, payload, base_id, depth, size = row
        if not 0 <= depth <= MAX_DEPTH or not 0 <= size <= MAX_BYTES:
            raise ValueError('对象预算无效')
        if codec == 'raw' and base_id is None and depth == 0:
            raw = bytes(payload)
        elif codec == 'zstd' and base_id is None and depth == 0:
            raw = self._codec(payload, decompress=True)
        elif codec == 'zstd-patch' and base_id is not None and depth > 0:
            base = self._load(base_id, seen)
            parent_depth = self.db.execute('SELECT depth FROM objects WHERE digest=?', (base_id,)).fetchone()[0]
            if depth != parent_depth + 1:
                raise ValueError('差量深度不匹配')
            raw = self._codec(payload, base, decompress=True)
        else:
            raise ValueError('对象编码无效')
        if len(raw) != size or sha(raw) != digest:
            raise ValueError('恢复内容摘要不匹配')
        return raw

    def _put(self, raw: bytes, base_id: str | None) -> str:
        digest = sha(raw)
        existing = self.db.execute('SELECT digest FROM objects WHERE digest=?', (digest,)).fetchone()
        if existing:
            if self._load(digest) != raw:
                raise ValueError('已有对象不一致')
            return digest
        codec, payload, base, depth = self._select_encoding(raw, base_id)
        self.db.execute('INSERT INTO objects VALUES(?,?,?,?,?,?)', (digest, codec, payload, base, depth, len(raw)))
        if self._load(digest) != raw:
            raise ValueError('写后恢复校验失败')
        return digest

    def _validate(self, checkpoint: bytes, index: bytes):
        for raw in (checkpoint, index):
            if not raw or len(raw) > MAX_BYTES:
                raise ValueError('输入大小无效')
            value = json.loads(raw, parse_constant=lambda _: (_ for _ in ()).throw(ValueError('非标准 JSON 数值')))
            if not isinstance(value, dict) or any(value.get(k) != v for k, v in self.binding.items()):
                raise ValueError('候选文档冻结身份不匹配')
        idx = json.loads(index)
        if idx.get('candidate_only') is not True or idx.get('claim_ceiling') != 'candidate_only':
            raise ValueError('本存储只接受 candidate_only，不提供准入')

    def save(self, name: str, checkpoint: bytes, index: bytes, *, parent: str | None = None, precommit=None) -> dict:
        if not KEY.fullmatch(name):
            raise ValueError('快照 ID 无效')
        self._validate(checkpoint, index)
        ids = sha(checkpoint), sha(index)
        try:
            self.db.execute('BEGIN IMMEDIATE')
            existing = self.db.execute('SELECT checkpoint,idx,parent FROM snapshots WHERE name=?', (name,)).fetchone()
            if existing:
                if existing != (*ids, parent):
                    raise ValueError('幂等 ID 冲突')
                self.restore(name)
                if precommit is not None: precommit()
                self.db.commit()
                return {'snapshot': name, 'checkpoint_sha256': ids[0], 'index_sha256': ids[1], 'created': False}
            latest = self.db.execute('SELECT name,checkpoint,idx FROM snapshots ORDER BY position DESC LIMIT 1').fetchone()
            if parent != (latest[0] if latest else None):
                raise ValueError('父快照不是当前恢复头；拒绝过期写入')
            self._put(checkpoint, latest[1] if latest else None)
            self._put(index, latest[2] if latest else None)
            self.db.execute('INSERT INTO snapshots(name,checkpoint,idx,parent) VALUES(?,?,?,?)', (name, *ids, parent))
            if precommit is not None: precommit()
            self.db.commit()
        except BaseException:
            self.db.rollback()
            raise
        return {'snapshot': name, 'checkpoint_sha256': ids[0], 'index_sha256': ids[1], 'created': True}

    def restore(self, name: str) -> tuple[bytes, bytes]:
        row = self.db.execute('SELECT checkpoint,idx FROM snapshots WHERE name=?', (name,)).fetchone()
        if not row:
            raise ValueError('快照不存在')
        result = self._load(row[0]), self._load(row[1])
        self._validate(*result)
        return result

    def stats(self) -> dict:
        objects, raw, packed, depth = self.db.execute('SELECT COUNT(*),COALESCE(SUM(raw_bytes),0),COALESCE(SUM(length(payload)),0),COALESCE(MAX(depth),0) FROM objects').fetchone()
        return {'snapshots': self.db.execute('SELECT COUNT(*) FROM snapshots').fetchone()[0],
                'objects': objects, 'object_raw_bytes': raw, 'packed_payload_bytes': packed,
                'max_delta_depth': depth, 'database_bytes': self.path.stat().st_size}
