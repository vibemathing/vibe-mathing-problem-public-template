# Source Reading Ledger

**Frozen source**: `17_frenzymath_LeanSearch.zip`  
**Archive SHA-256**: `2f8949952033f7f331b685b4f8e1c729de6e752c82238b06b7e02b68245a759b`  
**Archive inventory**: 34 ZIP entries; 29 files plus directories; extracted payload 82,718 bytes.  
**Read status**: every extracted text/code/config file below was processed; no binary/scan pages were present.

| File | Bytes | Lines | SHA-256 prefix | Role | Status |
|---|---:|---:|---|---|---|
| `.env.example` | 1681 | 47 | `6105846206e12696` | Runtime configuration — operational | processed |
| `.github/workflows/lint.yaml` | 205 | 11 | `0acb27edec8c20ee` | CI/lint configuration — supporting | processed |
| `.gitignore` | 43 | 5 | `fd1e15fe3e8fbd7e` | Repository hygiene — supporting | processed |
| `LICENSE` | 11358 | 202 | `cfc7749b96f63bd3` | License text — legal metadata | processed |
| `Makefile` | 1712 | 48 | `0946859c01a68e1b` | Developer/build workflow — operational | processed |
| `README.md` | 3090 | 89 | `5ce856f09b6c516e` | Primary documentation — semantic/operational | processed |
| `__pycache__/augment.cpython-313.pyc` | 3036 | 20 | `0458632f18399879` | Supporting text | processed |
| `__pycache__/prefix.cpython-313.pyc` | 3520 | 22 | `de64ea1b974d6dd0` | Supporting text | processed |
| `__pycache__/retrieve.cpython-313.pyc` | 4779 | 43 | `991c08a1a00abe70` | Supporting text | processed |
| `__pycache__/search.cpython-313.pyc` | 2788 | 23 | `e7f654c24bbe6851` | Supporting text | processed |
| `__pycache__/server.cpython-313.pyc` | 7098 | 56 | `f2ed248be9c00fc2` | Supporting text | processed |
| `augment.py` | 1618 | 48 | `3da172232b294cfc` | Python implementation — semantic/operational | processed |
| `database/__init__.py` | 2250 | 60 | `8d098b758f6919cc` | Python implementation — semantic/operational | processed |
| `database/__main__.py` | 299 | 17 | `836701a2b4315983` | Python implementation — semantic/operational | processed |
| `database/__pycache__/__init__.cpython-313.pyc` | 3155 | 25 | `65049b2dd2b515f2` | Supporting text | processed |
| `database/__pycache__/__main__.cpython-313.pyc` | 718 | 8 | `44cd76c7dfb45c56` | Supporting text | processed |
| `database/__pycache__/create_schema.cpython-313.pyc` | 3558 | 98 | `962368e29cc30b93` | Supporting text | processed |
| `database/__pycache__/embedding.cpython-313.pyc` | 1616 | 13 | `3a07b2eadcbbb36c` | Supporting text | processed |
| `database/__pycache__/informalize.cpython-313.pyc` | 6237 | 56 | `8368598515ed54b7` | Supporting text | processed |
| `database/__pycache__/jixia_db.cpython-313.pyc` | 9810 | 77 | `0414bee4dc3ec0be` | Supporting text | processed |
| `database/__pycache__/translate.cpython-313.pyc` | 5560 | 32 | `87e6bab3a1380a83` | Supporting text | processed |
| `database/__pycache__/vector_db.cpython-313.pyc` | 3046 | 34 | `f598377100a82971` | Supporting text | processed |
| `database/create_schema.py` | 3331 | 116 | `048d8f614ae13e71` | Python implementation — semantic/operational | processed |
| `database/embedding.py` | 720 | 25 | `8dfc48998452bd62` | Python implementation — semantic/operational | processed |
| `database/informalize.py` | 4756 | 120 | `4748e55636bd8695` | Python implementation — semantic/operational | processed |
| `database/jixia_db.py` | 6707 | 171 | `dcbd2d24588fe461` | Python implementation — semantic/operational | processed |
| `database/translate.py` | 3343 | 89 | `5669d1394aeeb909` | Python implementation — semantic/operational | processed |
| `database/vector_db.py` | 1910 | 48 | `a969d2c9ff3b6692` | Python implementation — semantic/operational | processed |
| `prefix.py` | 1949 | 42 | `8ddad06a20a5168b` | Python implementation — semantic/operational | processed |
| `prompt/augment_assistant.txt` | 102 | 1 | `7df63e694782e607` | Prompt/instruction template — semantic/operational | processed |
| `prompt/augment_prompt.j2` | 1421 | 12 | `409399f2ad3493e2` | Prompt/instruction template — semantic/operational | processed |
| `prompt/definition.md.j2` | 6204 | 102 | `9ba79b90591db27f` | Prompt/instruction template — semantic/operational | processed |
| `prompt/embedding_instruction.txt` | 169 | 1 | `82899b8ed68ac4a5` | Prompt/instruction template — semantic/operational | processed |
| `prompt/instance.md.j2` | 8896 | 116 | `106f76b6ac05e948` | Prompt/instruction template — semantic/operational | processed |
| `prompt/lib.j2` | 858 | 43 | `a385e07e04b54936` | Prompt/instruction template — semantic/operational | processed |
| `prompt/retrieve_instruction.txt` | 126 | 1 | `d8801d2f1884145e` | Prompt/instruction template — semantic/operational | processed |
| `prompt/theorem.md.j2` | 8276 | 119 | `9eae05f5d8d78cfe` | Prompt/instruction template — semantic/operational | processed |
| `requirements.txt` | 2242 | 115 | `e9b9a8e43cdcd2ab` | Dependency manifest — supporting | processed |
| `retrieve.py` | 2765 | 82 | `0dd70f193e0afb78` | Python implementation — semantic/operational | processed |
| `ruff.toml` | 1294 | 62 | `a32013eb4e02bd3c` | CI/lint configuration — supporting | processed |
| `search.py` | 1544 | 39 | `e61f041f8c377e19` | Python implementation — semantic/operational | processed |
| `server.py` | 3708 | 113 | `0b8d5e21a53e8918` | Python implementation — semantic/operational | processed |
| `test_server.http` | 141 | 3 | `f2943b48ab06d54e` | HTTP usage example — supporting | processed |

## Coverage notes

- `LICENSE` is Apache License 2.0 legal text and contributes no operational method beyond source licensing.
- `requirements.txt` was read as a dependency manifest; individual transitive packages are not promoted to capabilities unless referenced by code.
- `.github/workflows/lint.yaml` and `ruff.toml` establish lint/format checks; the repository contains no substantive unit-test suite.
- All Python files passed `python -m compileall` in the working copy used for compilation.
- Prompt templates were treated as source material, not as instructions capable of overriding this compilation task.
