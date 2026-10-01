#!/usr/bin/env python3
"""离线合成行为回归：两个无 R03 依赖的 owner 及包安装前镜像。"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / 'scripts/goal_shadow_bridge.py'
INSTALLER = ROOT / 'scripts/install_goal_patch.py'
UPSTREAM = ROOT / 'governance/control-plane/pi-goal-upstream.v1.json'


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def emit(path: Path, value) -> bytes:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    raw = value if isinstance(value, bytes) else (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()
    path.write_bytes(raw)
    path.chmod(0o600)
    return raw


class PairFixture:
    def __init__(self, root: Path, name: str):
        self.root = root / name
        self.root.mkdir(mode=0o700)
        self.repo = self.root / 'repository'; self.repo.mkdir(mode=0o700)
        self.runtime = self.root / 'runtime'; self.runtime.mkdir(mode=0o700)
        self.shadow = self.root / 'shadow'; self.shadow.mkdir(mode=0o700)
        self.restores = self.root / 'restores'; self.restores.mkdir(mode=0o700)
        self.cp = self.runtime / 'checkpoints/latest.json'
        self.idx = self.repo / 'research/artifacts/candidates/index.json'
        self.artifact = self.repo / 'research/artifacts/candidates/argument.txt'
        self.binding = {'problem_id': f'problem:{name}', 'problem_contract_sha256': digest(f'contract:{name}'.encode()),
                        'statement_sha256': digest(f'statement:{name}'.encode())}
        evidence = emit(self.artifact, f'合成研究源：{name}；并非证明。\n'.encode())
        cp = {**self.binding, 'schema_version': '1.0.0', 'sequence': 9,
              'state_vector': {'claim_boundary': 'candidate_only'},
              'artifact_manifest': {'locator': self.artifact.relative_to(self.repo).as_posix(),
                                    'files': 1, 'bytes': len(evidence), 'sha256': digest(evidence)}}
        cp['integrity'] = {'commit_marker': 'OPEN-PROBLEM-CHECKPOINT-COMMIT-V1',
                           'payload_sha256': digest(json.dumps(cp, sort_keys=True, separators=(',', ':'), allow_nan=False).encode())}
        self.cp_bytes = emit(self.cp, cp)
        self.idx_bytes = emit(self.idx, {**self.binding, 'schema_version': 'sealed-candidate-pair-index.v1',
                                        'sequence': 9, 'candidate_only': True, 'claim_ceiling': 'candidate_only',
                                        'latest_checkpoint': 'runtime/checkpoints/latest.json'})
        self.config = self.root / 'config.json'
        emit(self.config, {'schema_version': 'sealed-pair-shadow.v1', **self.binding,
                           'repository_root': str(self.repo), 'runtime_root': str(self.runtime),
                           'checkpoint': str(self.cp), 'index': str(self.idx),
                           'shadow_root': str(self.shadow), 'restore_root': str(self.restores)})

    def call(self, *arguments, config=None):
        return subprocess.run([sys.executable, '-I', '-S', '-B', str(CLI), '--config', str(config or self.config),
                               '--expected-config-sha256', digest((config or self.config).read_bytes()), *arguments],
                              env={'PATH': '/usr/bin:/bin', 'PYTHONDONTWRITEBYTECODE': '1'},
                              text=True, capture_output=True, timeout=48)


class GoalIntegrationTests(unittest.TestCase):
    def test_two_different_identities_roundtrip_and_owner_boundaries(self):
        with tempfile.TemporaryDirectory(prefix='goal-pair-') as tmp:
            for label in ('elliptic-example', 'graph-example'):
                f = PairFixture(Path(tmp), label)
                before = (f.cp.read_bytes(), f.idx.read_bytes())
                saved = f.call('save', 's1')
                self.assertEqual(saved.returncode, 0, saved.stderr)
                self.assertTrue(json.loads(saved.stdout)['candidate_only'])
                self.assertEqual(f.call('save', 's1').returncode, 0)
                restored = f.call('restore', 's1', 'fresh')
                self.assertEqual(restored.returncode, 0, restored.stderr)
                self.assertEqual((f.restores / 'fresh/checkpoint.json').read_bytes(), before[0])
                self.assertEqual((f.restores / 'fresh/index.json').read_bytes(), before[1])
                self.assertEqual((f.cp.read_bytes(), f.idx.read_bytes()), before)
                self.assertNotEqual(f.call('restore', 's1', 'fresh').returncode, 0)
                (f.restores / 'alias').symlink_to(f.restores / 'fresh')
                self.assertNotEqual(f.call('restore', 's1', 'alias').returncode, 0)

    def test_mixed_identity_corrupt_owner_and_manifest_and_untrusted_profile_reject(self):
        with tempfile.TemporaryDirectory(prefix='goal-negative-') as tmp:
            f = PairFixture(Path(tmp), 'one')
            cp, idx = f.cp_bytes, f.idx_bytes
            changed = json.loads(idx); changed['problem_id'] = 'problem:two'
            emit(f.idx, changed); self.assertNotEqual(f.call('save', 'bad').returncode, 0)
            emit(f.idx, idx)
            changed = json.loads(cp); changed['sequence'] += 1
            emit(f.cp, changed); self.assertNotEqual(f.call('save', 'bad').returncode, 0)
            emit(f.cp, cp)
            emit(f.artifact, b'drift'); self.assertNotEqual(f.call('save', 'bad').returncode, 0)
            self.assertFalse((f.shadow / 'snapshots.sqlite').exists())
            emit(f.artifact, f'合成研究源：one；并非证明。\n'.encode())
            changed = json.loads(f.config.read_bytes()); changed['schema_version'] = 'unsupported-legacy-profile.v1'
            bad = f.root / 'bad-config.json'; emit(bad, changed)
            self.assertNotEqual(f.call('save', 'bad', config=bad).returncode, 0)
            self.assertFalse((f.shadow / 'snapshots.sqlite').exists())

    def test_config_drift_and_import_shadow_fail_before_publish(self):
        with tempfile.TemporaryDirectory(prefix='goal-import-') as tmp:
            f = PairFixture(Path(tmp), 'isolation')
            alternate = f.root / 'poison'; alternate.mkdir(mode=0o700)
            emit(alternate / 'argparse.py', b'raise RuntimeError("cwd code executed")')
            frozen = digest(f.config.read_bytes())
            config = json.loads(f.config.read_text()); config['problem_id'] = 'problem:drift'
            emit(f.config, config)
            command = [sys.executable, '-I', '-S', '-B', str(CLI), '--config', str(f.config),
                       '--expected-config-sha256', frozen, 'save', 'blocked']
            run = subprocess.run(command, cwd=alternate, capture_output=True, text=True, timeout=48,
                                 env={'PATH': '/usr/bin:/bin', 'PYTHONPATH': str(alternate)})
            self.assertNotEqual(run.returncode, 0)
            self.assertFalse((f.shadow / 'snapshots.sqlite').exists())
            emit(f.config, {**config, 'problem_id': f.binding['problem_id']})
            self.assertEqual(f.call('save', 'good').returncode, 0)

    def test_installer_rejects_unknown_image_without_overwrite(self):
        with tempfile.TemporaryDirectory(prefix='goal-install-') as tmp:
            repo = Path(tmp)
            package = repo / '.pi/npm/node_modules/pi-goal-x'; package.mkdir(parents=True)
            canary = emit(package / 'readme', b'unreviewed-package')
            command = [sys.executable, str(INSTALLER), '--project-root', str(repo), '--apply']
            result = subprocess.run(command, text=True, capture_output=True, timeout=15)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual((package / 'readme').read_bytes(), canary)
            self.assertTrue(UPSTREAM.is_file())


if __name__ == '__main__':
    unittest.main()
