#!/usr/bin/env python3
"""Research OS 认知事件的 owner-ledger 适配、WAL writer 与只读投影。

本模块只连接既有 Problem/Attempt/Obligation/Candidate/Evidence 身份；它不
写入这些 owner ledger，也不授予认知事件 Evidence、Result、Solution 或路线
控制权。事件 ledger 和 projection 都永久保持 ``candidate_only``。

``scope_sha256`` 的本模块绑定规则是 ProblemContract 的冻结范围对象：
``domain``、``quantifiers``、``definitions``、``assumptions`` 和
``allowed_axioms`` 的规范 JSON 摘要。该规则只用于身份校验，不改变
ProblemContract schema 或数学语义。
"""

from __future__ import annotations

import copy
import fcntl
import hashlib
import json
import os
import re
import sys
import threading
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping

from jsonschema import Draft202012Validator, FormatChecker

# Direct execution (``python scripts/vibe_mathing/research_os.py``) does not put
# ``scripts/`` on sys.path; package imports already have it through the package.
if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    from validate_research_os_events import event_digest, validate_events as validate_event_shape  # noqa: E402
except ModuleNotFoundError:  # Support ``import scripts.vibe_mathing.research_os`` from project root.
    from scripts.validate_research_os_events import event_digest, validate_events as validate_event_shape  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EVENT_LEDGER = ROOT / "research" / "records" / "research-os-events.jsonl"
PROJECTION_SCHEMA = ROOT / "research" / "schema" / "research-os-event-projection.v1.schema.json"
MAX_JSONL_RECORD_BYTES = 2 * 1024 * 1024
HEX64 = re.compile(r"^[a-f0-9]{64}$")
_TYPED_ID = re.compile(
    r"^(problem|outcome|obligation|candidate|evidence-link|admission|example|"
    r"conjecture|refutation|connection|source|observation|artifact|definition|"
    r"literature|task|job|research-os|verification):[a-z0-9][a-z0-9.-]*$"
)

_OWNER_SCHEMAS = {
    "problem": ("problem-library/records/canonical-problems.jsonl", "problem-library/schema/canonical-problem.schema.json", "problem_id"),
    "attempt": ("research/records/attempts.jsonl", "research/schema/attempt.schema.json", "attempt_id"),
    "obligation-graph": ("research/records/obligation-graphs.jsonl", "research/schema/obligation-graph.schema.json", "graph_id"),
    "candidate": ("research/records/candidate-artifacts.jsonl", "research/schema/candidate-artifact.schema.json", "candidate_id"),
    "evidence-link": ("research/records/evidence-links.jsonl", "research/schema/evidence-link.schema.json", "evidence_link_id"),
}
SCOPE_FIELDS = ("domain", "quantifiers", "definitions", "assumptions", "allowed_axioms")
MANAGED_PREFIXES = frozenset({"problem", "attempt", "obligation", "candidate", "evidence-link"})
EXTERNAL_PREFIXES = frozenset(
    {
        "outcome",
        "admission",
        "example",
        "conjecture",
        "refutation",
        "connection",
        "source",
        "observation",
        "artifact",
        "definition",
        "literature",
        "task",
        "job",
        "research-os",
        "verification",
    }
)
COGNITIVE_PREFIXES = frozenset({"research-os", "example", "conjecture", "refutation", "connection", "verification"})


class ResearchOsError(RuntimeError):
    """Research OS 连接层拒绝不安全或不一致输入。"""


class ResearchOsOwnerError(ResearchOsError):
    """既有 owner ledger 身份或引用无法证明。"""


class ResearchOsWriterError(ResearchOsError):
    """事件 writer、WAL 或 append-only 事务失败。"""


@dataclass(frozen=True)
class OwnerSnapshot:
    """只读 owner 身份快照；不携带数学正文投影。"""

    problems: dict[str, dict[str, Any]]
    attempts: dict[str, dict[str, Any]]
    candidates: dict[str, dict[str, Any]]
    evidence_links: dict[str, dict[str, Any]]
    obligations: dict[str, tuple[dict[str, Any], dict[str, Any]]]
    owner_ledger_bindings: tuple[dict[str, Any], ...]
    owner_snapshot_sha256: str


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON constant: {value}")


def _canonical_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ResearchOsError(f"cannot canonicalize finite JSON: {exc}") from exc


def canonical_json_sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _require_sha256(value: Any, label: str) -> str:
    if not isinstance(value, str) or HEX64.fullmatch(value) is None:
        raise ResearchOsError(f"{label} must be a lowercase SHA-256 digest")
    return value


def _safe_project_path(root: Path, relative: str | Path, label: str) -> Path:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise ResearchOsError(f"{label} path escapes project root: {path}")
    resolved = (root / path).absolute()
    current = root
    for part in path.parts:
        current /= part
        if current.is_symlink():
            raise ResearchOsError(f"{label} path contains a symlink: {current}")
    return resolved


def _load_json(path: Path, label: str) -> Any:
    if path.is_symlink() or not path.is_file():
        raise ResearchOsError(f"{label} must be a regular file: {path}")
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            parse_constant=_reject_constant,
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise ResearchOsError(f"{label} is not finite JSON: {exc}") from exc


def _read_jsonl_bytes(
    path: Path,
    *,
    required: bool,
    label: str,
) -> tuple[list[dict[str, Any]], bytes | None]:
    """Read one owner ledger once and return both parsed rows and exact bytes."""
    if path.is_symlink():
        raise ResearchOsError(f"{label} must be a regular file: {path}")
    if not path.exists():
        if required:
            raise ResearchOsError(f"{label} is missing: {path}")
        return [], None
    if not path.is_file():
        raise ResearchOsError(f"{label} must be a regular file: {path}")
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ResearchOsError(f"cannot read {label}: {path}") from exc
    if raw and not raw.endswith(b"\n"):
        raise ResearchOsError(f"{label} is truncated (missing final newline): {path}")
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(raw.splitlines(), 1):
        if not line.strip():
            raise ResearchOsError(f"{label}:{line_number}: blank JSONL line")
        if len(line) > MAX_JSONL_RECORD_BYTES:
            raise ResearchOsError(f"{label}:{line_number}: record exceeds 2 MiB")
        try:
            value = json.loads(line.decode("utf-8"), parse_constant=_reject_constant)
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            raise ResearchOsError(f"{label}:{line_number}: invalid finite JSON") from exc
        if not isinstance(value, dict):
            raise ResearchOsError(f"{label}:{line_number}: record must be an object")
        rows.append(value)
    return rows, raw


def _read_jsonl(path: Path, *, required: bool, label: str) -> list[dict[str, Any]]:
    rows, _ = _read_jsonl_bytes(path, required=required, label=label)
    return rows


def _schema_validate(root: Path, schema_relative: str, value: Mapping[str, Any], label: str) -> None:
    schema = _load_json(_safe_project_path(root, schema_relative, f"{label} schema"), f"{label} schema")
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # jsonschema exposes several schema exception types.
        raise ResearchOsOwnerError(f"{label} schema is invalid") from exc
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value),
        key=lambda item: list(item.absolute_path),
    )
    if errors:
        path = "/".join(str(part) for part in errors[0].absolute_path) or "<root>"
        raise ResearchOsOwnerError(f"{label} schema invalid at {path}: {errors[0].message}")


def _index_unique(rows: Iterable[Mapping[str, Any]], key: str, label: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        identity = row.get(key)
        if not isinstance(identity, str) or not identity:
            raise ResearchOsOwnerError(f"{label} missing {key}")
        if identity in result:
            raise ResearchOsOwnerError(f"{label} duplicate {key}: {identity}")
        result[identity] = dict(row)
    return result


def problem_scope(problem: Mapping[str, Any]) -> dict[str, Any]:
    """Return the frozen ProblemContract scope object used by this adapter."""
    missing = [field for field in SCOPE_FIELDS if field not in problem]
    if missing:
        raise ResearchOsOwnerError(f"ProblemContract scope fields missing: {missing}")
    return {field: copy.deepcopy(problem[field]) for field in SCOPE_FIELDS}


def problem_scope_sha256(problem: Mapping[str, Any]) -> str:
    return canonical_json_sha256(problem_scope(problem))


def problem_statement_sha256(problem: Mapping[str, Any]) -> str:
    statement = problem.get("statement")
    if not isinstance(statement, Mapping):
        raise ResearchOsOwnerError("ProblemContract statement must be an object")
    return canonical_json_sha256(statement)


def _prefix(identity: str) -> str:
    return identity.split(":", 1)[0]


def _validate_typed_ref(identity: str, label: str) -> None:
    if not isinstance(identity, str) or _TYPED_ID.fullmatch(identity) is None:
        raise ResearchOsOwnerError(f"{label} is not a valid typed ID: {identity!r}")


class ResearchOsOwnerLedgerAdapter:
    """只读读取并证明认知事件对 owner ledger 的身份引用。

    该适配器不把 owner ledger 的数学内容复制到 projection。对于尚未由
    本仓库拥有的 source/outcome/admission 等身份，只保留 typed opaque ref；
    这表示“本 adapter 未拥有该 ledger”，不是对其存在或真值的宣称。
    """

    def __init__(self, project_root: Path | str) -> None:
        self.root = Path(project_root).expanduser().resolve()
        self.snapshot = self._load_snapshot()
        self._event_schema = _load_json(
            _safe_project_path(self.root, "research/schema/research-os-event.v1.schema.json", "Research OS event schema"),
            "Research OS event schema",
        )

    def _load_snapshot(self) -> OwnerSnapshot:
        records: dict[str, dict[str, dict[str, Any]]] = {}
        owner_ledger_bindings: list[dict[str, Any]] = []
        for prefix, (record_relative, schema_relative, id_field) in _OWNER_SCHEMAS.items():
            path = _safe_project_path(self.root, record_relative, f"{prefix} owner ledger")
            rows, raw = _read_jsonl_bytes(
                path,
                required=(prefix == "problem"),
                label=f"{prefix} owner ledger",
            )
            if raw is not None:
                for row in rows:
                    _schema_validate(self.root, schema_relative, row, prefix)
            records[prefix] = _index_unique(rows, id_field, f"{prefix} owner ledger")
            owner_ledger_bindings.append(
                {
                    "owner_kind": prefix,
                    "path": record_relative,
                    "present": raw is not None,
                    "sha256": _sha256_bytes(raw) if raw is not None else None,
                    "record_count": len(rows),
                }
            )

        problems = records["problem"]
        attempts = records["attempt"]
        for attempt_id, attempt in attempts.items():
            problem_id = attempt.get("problem_id")
            problem = problems.get(problem_id)
            if problem is None:
                raise ResearchOsOwnerError(f"Attempt references unknown ProblemContract: {attempt_id}")
            expected = canonical_json_sha256(problem)
            declared = attempt.get("problem_contract_sha256")
            if declared is not None and declared != expected:
                raise ResearchOsOwnerError(f"Attempt ProblemContract digest drift: {attempt_id}")

        obligations: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
        for graph in records["obligation-graph"].values():
            _schema_validate(self.root, "research/schema/obligation-graph.schema.json", graph, "ObligationGraph")
            problem = problems.get(graph.get("problem_id"))
            if problem is None:
                raise ResearchOsOwnerError(f"ObligationGraph references unknown ProblemContract: {graph.get('graph_id')}")
            expected_contract = canonical_json_sha256(problem)
            if graph.get("problem_contract_sha256") != expected_contract:
                raise ResearchOsOwnerError(f"ObligationGraph ProblemContract digest drift: {graph.get('graph_id')}")
            attempt = attempts.get(graph.get("attempt_id"))
            if attempt is None:
                raise ResearchOsOwnerError(f"ObligationGraph references unknown Attempt: {graph.get('graph_id')}")
            if attempt.get("problem_id") != graph.get("problem_id"):
                raise ResearchOsOwnerError(f"ObligationGraph crosses ProblemContract: {graph.get('graph_id')}")
            for obligation in graph.get("obligations", []):
                identity = obligation.get("obligation_id")
                if identity in obligations:
                    previous_graph, previous_obligation = obligations[identity]
                    if (
                        previous_graph.get("problem_id") != graph.get("problem_id")
                        or previous_obligation.get("statement_sha256") != obligation.get("statement_sha256")
                    ):
                        raise ResearchOsOwnerError(f"ambiguous obligation identity: {identity}")
                obligations[identity] = (dict(graph), dict(obligation))

        for candidate_id, candidate in records["candidate"].items():
            graph = next(
                (graph for graph, _ in obligations.values() if graph.get("graph_id") == candidate.get("graph_id")),
                None,
            )
            if graph is None:
                raise ResearchOsOwnerError(f"Candidate references unknown ObligationGraph: {candidate_id}")
            expected_contract = canonical_json_sha256(problems[graph["problem_id"]])
            for field in ("problem_id", "graph_id", "attempt_id", "problem_contract_sha256"):
                expected = expected_contract if field == "problem_contract_sha256" else graph.get(field)
                if candidate.get(field) != expected:
                    raise ResearchOsOwnerError(f"Candidate owner binding drift: {candidate_id}/{field}")

        for link_id, link in records["evidence-link"].items():
            candidate = records["candidate"].get(link.get("candidate_id"))
            if candidate is None:
                raise ResearchOsOwnerError(f"EvidenceLink references unknown Candidate: {link_id}")
            if link.get("graph_id") != candidate.get("graph_id") or link.get("obligation_id") != candidate.get("obligation_id"):
                raise ResearchOsOwnerError(f"EvidenceLink owner binding drift: {link_id}")

        bindings = tuple(sorted(owner_ledger_bindings, key=lambda item: item["owner_kind"]))
        return OwnerSnapshot(
            problems=records["problem"],
            attempts=attempts,
            candidates=records["candidate"],
            evidence_links=records["evidence-link"],
            obligations=obligations,
            owner_ledger_bindings=bindings,
            owner_snapshot_sha256=canonical_json_sha256(list(bindings)),
        )

    def ensure_snapshot_current(self) -> None:
        """Refuse validation if any owner ledger changed after snapshot load."""
        for binding in self.snapshot.owner_ledger_bindings:
            record_relative = binding["path"]
            path = _safe_project_path(self.root, record_relative, f"{binding['owner_kind']} owner ledger")
            _, raw = _read_jsonl_bytes(path, required=False, label=f"{binding['owner_kind']} owner ledger")
            present = raw is not None
            digest = _sha256_bytes(raw) if raw is not None else None
            if present != binding["present"] or digest != binding["sha256"]:
                raise ResearchOsOwnerError(
                    f"owner ledger changed after snapshot: {binding['owner_kind']} ({record_relative})"
                )

    def _known_statement_digests(self, problem_id: str) -> set[str]:
        problem = self.snapshot.problems[problem_id]
        result = {problem_statement_sha256(problem)}
        result.update(
            obligation["statement_sha256"]
            for graph, obligation in self.snapshot.obligations.values()
            if graph.get("problem_id") == problem_id
        )
        return result

    def _resolve_ref(self, identity: str, binding: Mapping[str, Any]) -> str:
        prefix = _prefix(identity)
        if prefix not in MANAGED_PREFIXES and prefix not in EXTERNAL_PREFIXES:
            raise ResearchOsOwnerError(f"unsupported Research OS reference prefix: {identity}")
        if prefix == "problem":
            problem = self.snapshot.problems.get(identity)
            if problem is None:
                raise ResearchOsOwnerError(f"event references unknown ProblemContract: {identity}")
            if identity != binding["problem_id"]:
                raise ResearchOsOwnerError(f"event crosses ProblemContract: {identity}")
            return "managed"
        if prefix == "attempt":
            attempt = self.snapshot.attempts.get(identity)
            if attempt is None:
                raise ResearchOsOwnerError(f"event references unknown Attempt: {identity}")
            if attempt.get("problem_id") != binding["problem_id"]:
                raise ResearchOsOwnerError(f"event Attempt crosses ProblemContract: {identity}")
            if attempt.get("problem_contract_sha256") not in {None, binding["problem_contract_sha256"]}:
                raise ResearchOsOwnerError(f"event Attempt contract digest drift: {identity}")
            return "managed"
        if prefix == "obligation":
            resolved = self.snapshot.obligations.get(identity)
            if resolved is None:
                raise ResearchOsOwnerError(f"event references unknown Obligation: {identity}")
            graph, _ = resolved
            if graph.get("problem_id") != binding["problem_id"] or graph.get("problem_contract_sha256") != binding["problem_contract_sha256"]:
                raise ResearchOsOwnerError(f"event Obligation crosses ProblemContract: {identity}")
            return "managed"
        if prefix == "candidate":
            candidate = self.snapshot.candidates.get(identity)
            if candidate is None:
                raise ResearchOsOwnerError(f"event references unknown Candidate: {identity}")
            if candidate.get("problem_id") != binding["problem_id"] or candidate.get("problem_contract_sha256") != binding["problem_contract_sha256"]:
                raise ResearchOsOwnerError(f"event Candidate crosses ProblemContract: {identity}")
            return "managed"
        if prefix == "evidence-link":
            link = self.snapshot.evidence_links.get(identity)
            if link is None:
                raise ResearchOsOwnerError(f"event references unknown EvidenceLink: {identity}")
            candidate = self.snapshot.candidates.get(link.get("candidate_id"))
            if candidate is None or candidate.get("problem_id") != binding["problem_id"]:
                raise ResearchOsOwnerError(f"event EvidenceLink crosses ProblemContract: {identity}")
            return "managed"
        return "external"

    def validate_events(self, events: list[dict[str, Any]]) -> list[str]:
        """Return structural and owner-binding errors without mutating input."""
        try:
            self.ensure_snapshot_current()
        except ResearchOsError as exc:
            return [f"owner snapshot:{exc}"]
        schema_errors = validate_event_shape(events, self._event_schema)
        if schema_errors:
            return list(schema_errors)
        errors: list[str] = []
        prior_object_ids: set[str] = set()
        known_binding: dict[str, Any] | None = None
        for index, event in enumerate(events, 1):
            try:
                binding = event["problem_contract"]
                problem_id = binding["problem_id"]
                problem = self.snapshot.problems.get(problem_id)
                if problem is None:
                    raise ResearchOsOwnerError(f"event references unknown ProblemContract: {problem_id}")
                if problem.get("lifecycle") != "active":
                    raise ResearchOsOwnerError(f"event ProblemContract is not active: {problem_id}")
                expected_contract = canonical_json_sha256(problem)
                if binding["problem_contract_sha256"] != expected_contract:
                    raise ResearchOsOwnerError(f"ProblemContract digest mismatch: {problem_id}")
                if binding["scope_sha256"] != problem_scope_sha256(problem):
                    raise ResearchOsOwnerError(f"ProblemContract scope digest mismatch: {problem_id}")
                if binding["statement_sha256"] not in self._known_statement_digests(problem_id):
                    raise ResearchOsOwnerError(f"ProblemContract statement identity is not observed in owner ledgers: {problem_id}")
                if known_binding is None:
                    known_binding = dict(binding)
                elif binding != known_binding:
                    raise ResearchOsOwnerError("ProblemContract binding drifts within event ledger")

                payload = event["payload"]
                refs = payload["refs"]
                if event["event_kind"] == "working_set_created" and f"problem:{problem_id.removeprefix('problem:')}" not in refs:
                    raise ResearchOsOwnerError("working_set_created must reference its ProblemContract")
                for ref in refs:
                    _validate_typed_ref(ref, f"event {index} payload.refs")
                    if _prefix(ref) in COGNITIVE_PREFIXES and ref not in prior_object_ids:
                        raise ResearchOsOwnerError(f"event {index} references a future or unknown cognitive object: {ref}")
                    self._resolve_ref(ref, binding)
                object_id = event["object_id"]
                if event["event_kind"] != "working_set_created" and event["payload"]["action"] in {"revised", "superseded", "invalidated"} and object_id not in prior_object_ids:
                    raise ResearchOsOwnerError(f"event {index} revises an unknown cognitive object: {object_id}")
                prior_object_ids.add(object_id)
            except ResearchOsError as exc:
                errors.append(f"event {index} owner:{exc}")
        return errors

    def ensure_valid(self, events: list[dict[str, Any]]) -> None:
        errors = self.validate_events(events)
        if errors:
            raise ResearchOsOwnerError("; ".join(errors))


_LOCK_GUARD = threading.Lock()
_LOCKS: dict[str, threading.RLock] = {}


def _thread_lock(path: Path) -> threading.RLock:
    key = str(path)
    with _LOCK_GUARD:
        return _LOCKS.setdefault(key, threading.RLock())


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


class ResearchOsEventWriter:
    """单机 append-only event writer，使用 flock、WAL、fsync 与原子替换。"""

    def __init__(
        self,
        project_root: Path | str,
        event_path: Path | str | None = None,
        *,
        owner_adapter: ResearchOsOwnerLedgerAdapter | None = None,
        require_owner_binding: bool = True,
    ) -> None:
        self.root = Path(project_root).expanduser().resolve()
        self.owner_adapter = owner_adapter
        self.require_owner_binding = require_owner_binding
        if owner_adapter is not None and owner_adapter.root != self.root:
            raise ResearchOsWriterError("owner adapter must use the same project root as the event writer")
        requested = Path(event_path) if event_path is not None else Path("research/records/research-os-events.jsonl")
        # 保留未解析的路径，以便后续显式拒绝 symlink，而不是把 symlink
        # 静默解析成另一个可写目标。
        self.event_path = (self.root / requested if not requested.is_absolute() else requested).absolute()
        if ".." in requested.parts:
            raise ResearchOsWriterError("event ledger path cannot contain '..'")
        try:
            self.event_path.relative_to(self.root)
        except ValueError as exc:
            raise ResearchOsWriterError("event ledger must stay inside project root") from exc
        if self.event_path.is_symlink():
            raise ResearchOsWriterError(f"event ledger cannot be a symlink: {self.event_path}")
        self.lock_path = self.event_path.with_name(f".{self.event_path.name}.lock")
        self.wal_path = self.event_path.with_name(f".{self.event_path.name}.wal")
        self.schema = _load_json(
            _safe_project_path(self.root, "research/schema/research-os-event.v1.schema.json", "Research OS event schema"),
            "Research OS event schema",
        )

    def _check_parent_chain(self) -> None:
        current = self.root
        for part in self.event_path.relative_to(self.root).parts[:-1]:
            current /= part
            if current.is_symlink():
                raise ResearchOsWriterError(f"event ledger parent cannot be a symlink: {current}")

    @contextmanager
    def _locked(self) -> Iterator[None]:
        self._check_parent_chain()
        self.event_path.parent.mkdir(parents=True, exist_ok=True)
        self._check_parent_chain()
        guard = _thread_lock(self.lock_path)
        guard.acquire()
        handle = None
        try:
            self._check_regular(self.lock_path, "event lock")
            handle = self.lock_path.open("a+b")
            os.chmod(self.lock_path, 0o600)
        except BaseException:
            if handle is not None:
                handle.close()
            guard.release()
            raise
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            yield
        finally:
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            finally:
                handle.close()
                guard.release()

    @contextmanager
    def _locked_existing(self) -> Iterator[None]:
        """Acquire an existing lock without creating runtime files."""
        self._check_parent_chain()
        self._check_regular(self.lock_path, "event lock")
        if not self.lock_path.exists():
            raise ResearchOsWriterError("event lock is missing; refusing an unlocked projection read")
        if (os.stat(self.lock_path).st_mode & 0o777) != 0o600:
            raise ResearchOsWriterError("event lock must have mode 0600 for projection read")
        guard = _thread_lock(self.lock_path)
        guard.acquire()
        handle = None
        try:
            self._check_regular(self.lock_path, "event lock")
            handle = self.lock_path.open("rb")
        except BaseException:
            if handle is not None:
                handle.close()
            guard.release()
            raise
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            yield
        finally:
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            finally:
                handle.close()
                guard.release()

    def _check_regular(self, path: Path, label: str) -> None:
        if path.is_symlink():
            raise ResearchOsWriterError(f"{label} cannot be a symlink: {path}")
        if path.exists() and not path.is_file():
            raise ResearchOsWriterError(f"{label} must be a regular file: {path}")

    def _read_bytes_unlocked(self) -> bytes:
        self._check_regular(self.event_path, "event ledger")
        if not self.event_path.exists():
            return b""
        try:
            raw = self.event_path.read_bytes()
        except OSError as exc:
            raise ResearchOsWriterError(f"cannot read event ledger: {self.event_path}") from exc
        if raw and not raw.endswith(b"\n"):
            raise ResearchOsWriterError("event ledger is truncated")
        if any(not line.strip() for line in raw.splitlines()):
            raise ResearchOsWriterError("event ledger contains blank lines")
        return raw

    def _parse_events(self, raw: bytes) -> list[dict[str, Any]]:
        events: list[dict[str, Any]] = []
        for line_number, line in enumerate(raw.splitlines(), 1):
            if len(line) > MAX_JSONL_RECORD_BYTES:
                raise ResearchOsWriterError(f"event ledger line {line_number} exceeds 2 MiB")
            try:
                value = json.loads(line.decode("utf-8"), parse_constant=_reject_constant)
            except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
                raise ResearchOsWriterError(f"event ledger line {line_number} is invalid JSON") from exc
            if not isinstance(value, dict):
                raise ResearchOsWriterError(f"event ledger line {line_number} is not an object")
            events.append(value)
        errors = validate_event_shape(events, self.schema)
        if errors:
            raise ResearchOsWriterError("existing event ledger is invalid: " + "; ".join(errors))
        return events

    @staticmethod
    def _immutable_part(event: Mapping[str, Any]) -> dict[str, Any]:
        return {key: copy.deepcopy(value) for key, value in event.items() if key not in {"sequence", "previous_event_sha256", "event_sha256"}}

    def _normalise(self, event: Mapping[str, Any], events: list[dict[str, Any]]) -> dict[str, Any]:
        if not isinstance(event, Mapping):
            raise ResearchOsWriterError("event must be an object")
        value = copy.deepcopy(dict(event))
        expected_sequence = len(events) + 1
        expected_previous = events[-1]["event_sha256"] if events else None
        if "sequence" not in value:
            value["sequence"] = expected_sequence
        if "previous_event_sha256" not in value:
            value["previous_event_sha256"] = expected_previous
        if value.get("sequence") != expected_sequence:
            raise ResearchOsWriterError(f"new event sequence must be {expected_sequence}")
        if value.get("previous_event_sha256") != expected_previous:
            raise ResearchOsWriterError("new event previous_event_sha256 does not match chain head")
        computed = event_digest(value)
        if "event_sha256" not in value:
            value["event_sha256"] = computed
        if value.get("event_sha256") != computed:
            raise ResearchOsWriterError("new event event_sha256 does not match payload")
        errors = validate_event_shape([*events, value], self.schema)
        if errors:
            raise ResearchOsWriterError("new event is invalid: " + "; ".join(errors))
        return value

    def _resolve_duplicate(self, event: Mapping[str, Any], events: list[dict[str, Any]]) -> dict[str, Any] | None:
        event_id = event.get("event_id")
        if not isinstance(event_id, str):
            return None
        existing = next((item for item in events if item.get("event_id") == event_id), None)
        if existing is None:
            return None
        if self._immutable_part(existing) != self._immutable_part(event):
            raise ResearchOsWriterError(f"event_id exists with different content: {event_id}")
        return copy.deepcopy(existing)

    def _atomic_replace(self, path: Path, data: bytes, token: str) -> None:
        self._check_regular(path, "runtime file")
        temporary = path.with_name(f".{path.name}.{token}.tmp")
        try:
            if temporary.exists() or temporary.is_symlink():
                raise ResearchOsWriterError(f"runtime temporary path already exists: {temporary}")
            with temporary.open("xb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            os.chmod(temporary, 0o600)
            os.replace(temporary, path)
            os.chmod(path, 0o600)
            _fsync_directory(path.parent)
        except OSError as exc:
            raise ResearchOsWriterError(f"atomic replace failed: {path}") from exc
        finally:
            if temporary.exists() or temporary.is_symlink():
                temporary.unlink(missing_ok=True)

    def _remove_wal(self) -> None:
        self._check_regular(self.wal_path, "event WAL")
        if not self.wal_path.exists():
            return
        try:
            self.wal_path.unlink()
            _fsync_directory(self.wal_path.parent)
        except OSError as exc:
            raise ResearchOsWriterError("cannot remove committed event WAL") from exc

    def _recover_wal(self) -> None:
        self._check_regular(self.wal_path, "event WAL")
        if not self.wal_path.exists():
            return
        try:
            raw = self.wal_path.read_bytes()
            wal = json.loads(raw.decode("utf-8"), parse_constant=_reject_constant)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            raise ResearchOsWriterError("event WAL is invalid") from exc
        if not isinstance(wal, dict) or wal.get("schema_version") != "1.0.0":
            raise ResearchOsWriterError("event WAL schema is invalid")
        transaction_id = wal.get("transaction_id")
        if not isinstance(transaction_id, str) or re.fullmatch(r"[A-Za-z0-9._-]{1,128}", transaction_id) is None:
            raise ResearchOsWriterError("event WAL transaction_id is invalid")
        base_digest = _require_sha256(wal.get("base_sha256"), "event WAL base_sha256")
        target_digest = _require_sha256(wal.get("target_sha256"), "event WAL target_sha256")
        if transaction_id != target_digest[:32]:
            raise ResearchOsWriterError("event WAL transaction_id does not bind target digest")
        base_count = wal.get("base_event_count")
        pending = wal.get("events")
        if not isinstance(base_count, int) or base_count < 0 or not isinstance(pending, list) or not pending:
            raise ResearchOsWriterError("event WAL transaction shape is invalid")
        for event in pending:
            if not isinstance(event, dict):
                raise ResearchOsWriterError("event WAL pending item is not an object")
        current = self._read_bytes_unlocked()
        current_digest = _sha256_bytes(current)
        current_lines = current.splitlines(keepends=True)
        if base_count > len(current_lines):
            raise ResearchOsWriterError("event WAL base event count exceeds current ledger")
        base_prefix = b"".join(current_lines[:base_count])
        if _sha256_bytes(base_prefix) != base_digest:
            raise ResearchOsWriterError("event WAL base digest does not match current ledger prefix")
        target = base_prefix + b"".join(_canonical_bytes(event) + b"\n" for event in pending)
        if _sha256_bytes(target) != target_digest:
            raise ResearchOsWriterError("event WAL target digest mismatch")
        if current_digest == target_digest:
            self._remove_wal()
            return
        if current_digest != base_digest:
            raise ResearchOsWriterError("event WAL base/target mismatch; refusing guessed recovery")
        events = self._parse_events(current)
        if len(events) != base_count:
            raise ResearchOsWriterError("event WAL base event count mismatch")
        recovered = self._parse_events(target)
        if validate_event_shape(recovered, self.schema):
            raise ResearchOsWriterError("event WAL recovered target fails event validation")
        self._atomic_replace(self.event_path, target, f"recover-{transaction_id}")
        self._remove_wal()

    def _commit(self, events: list[dict[str, Any]], pending: list[dict[str, Any]], fail_point: str | None) -> None:
        if fail_point not in {None, "after_wal", "after_replace"}:
            raise ResearchOsWriterError(f"unsupported failure injection point: {fail_point}")
        if not pending:
            return
        current = self._read_bytes_unlocked()
        if current.count(b"\n") != len(events):
            raise ResearchOsWriterError("event ledger changed during append transaction")
        target = current + b"".join(_canonical_bytes(event) + b"\n" for event in pending)
        transaction_id = hashlib.sha256(target).hexdigest()[:32]
        if self.wal_path.exists() or self.wal_path.is_symlink():
            raise ResearchOsWriterError("event WAL contains an unresolved transaction")
        wal = {
            "schema_version": "1.0.0",
            "transaction_id": transaction_id,
            "base_sha256": _sha256_bytes(current),
            "target_sha256": _sha256_bytes(target),
            "base_event_count": len(events),
            "events": copy.deepcopy(pending),
        }
        self._atomic_replace(self.wal_path, _canonical_bytes(wal) + b"\n", f"wal-{transaction_id}")
        if fail_point == "after_wal":
            raise ResearchOsWriterError("failure injection: after_wal")
        self._atomic_replace(self.event_path, target, f"event-{transaction_id}")
        if fail_point == "after_replace":
            raise ResearchOsWriterError("failure injection: after_replace")
        self._remove_wal()

    def append_many(
        self,
        events_to_append: list[Mapping[str, Any]],
        *,
        owner_adapter: ResearchOsOwnerLedgerAdapter | None = None,
        fail_point: str | None = None,
    ) -> list[dict[str, Any]]:
        if not isinstance(events_to_append, list):
            raise ResearchOsWriterError("append_many requires a list")
        with self._locked():
            self._recover_wal()
            current_raw = self._read_bytes_unlocked()
            events = self._parse_events(current_raw)
            working = copy.deepcopy(events)
            pending: list[dict[str, Any]] = []
            stored: list[dict[str, Any]] = []
            for candidate in events_to_append:
                duplicate = self._resolve_duplicate(candidate, working)
                if duplicate is not None:
                    stored.append(duplicate)
                    continue
                normalised = self._normalise(candidate, working)
                working.append(normalised)
                pending.append(normalised)
                stored.append(copy.deepcopy(normalised))
            selected_adapter = owner_adapter if owner_adapter is not None else self.owner_adapter
            if self.require_owner_binding and selected_adapter is None:
                raise ResearchOsWriterError(
                    "owner-bound event append requires an explicit ResearchOsOwnerLedgerAdapter"
                )
            if selected_adapter is not None:
                if selected_adapter.root != self.root:
                    raise ResearchOsWriterError("owner adapter must use the same project root as the event writer")
                selected_adapter.ensure_valid(working)
            self._commit(events, pending, fail_point)
            return stored

    def append(
        self,
        event: Mapping[str, Any],
        *,
        owner_adapter: ResearchOsOwnerLedgerAdapter | None = None,
        fail_point: str | None = None,
    ) -> dict[str, Any]:
        return self.append_many([event], owner_adapter=owner_adapter, fail_point=fail_point)[0]

    def read_events(self) -> list[dict[str, Any]]:
        with self._locked():
            self._recover_wal()
            return self._parse_events(self._read_bytes_unlocked())


class ResearchOsProjector:
    """从事件 ledger 派生不含数学正文的 candidate-only metadata projection。"""

    def __init__(self, project_root: Path | str, owner_adapter: ResearchOsOwnerLedgerAdapter | None = None) -> None:
        self.root = Path(project_root).expanduser().resolve()
        self.owner_adapter = owner_adapter or ResearchOsOwnerLedgerAdapter(self.root)
        self.schema = _load_json(
            _safe_project_path(self.root, "research/schema/research-os-event-projection.v1.schema.json", "Research OS projection schema"),
            "Research OS projection schema",
        )

    def project_events(self, events: list[dict[str, Any]], *, ledger_sha256: str, ledger_path: str) -> dict[str, Any]:
        if not isinstance(events, list) or not events:
            raise ResearchOsError("cannot project an empty Research OS event ledger")
        _require_sha256(ledger_sha256, "ledger_sha256")
        errors = self.owner_adapter.validate_events(events)
        if errors:
            raise ResearchOsOwnerError("; ".join(errors))
        relative_path = Path(ledger_path)
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise ResearchOsError("projection ledger_path must be project-relative")
        binding = events[0]["problem_contract"]
        histories: dict[tuple[str, str], list[dict[str, Any]]] = {}
        external_refs: set[str] = set()
        managed_ref_count = 0
        for event in events:
            key = (event["object_kind"], event["object_id"])
            histories.setdefault(key, []).append(event)
            for ref in event["payload"]["refs"]:
                if _prefix(ref) in MANAGED_PREFIXES:
                    managed_ref_count += 1
                elif _prefix(ref) not in COGNITIVE_PREFIXES:
                    external_refs.add(ref)
        objects: list[dict[str, Any]] = []
        for (object_kind, object_id), history in sorted(histories.items()):
            latest = history[-1]
            payload = latest["payload"]
            action = payload["action"]
            status = {
                "superseded": "superseded",
                "invalidated": "invalidated",
            }.get(action, "current")
            objects.append(
                {
                    "object_kind": object_kind,
                    "object_id": object_id,
                    "latest_event_id": latest["event_id"],
                    "latest_sequence": latest["sequence"],
                    "event_kind": latest["event_kind"],
                    "action": action,
                    "effective_status": status,
                    "history_count": len(history),
                    "refs": list(payload["refs"]),
                    "statement_sha256": payload.get("statement_sha256"),
                    "scope_sha256": payload.get("scope_sha256"),
                    "artifact_sha256": payload.get("artifact_sha256"),
                    "coverage": payload.get("coverage"),
                    "note_sha256": canonical_json_sha256(payload["note"]),
                }
            )
        generated_at = max(event["recorded_at"] for event in events)
        projection: dict[str, Any] = {
            "schema_version": "research-os-event-projection.v1",
            "projection_id": f"research-os-projection:{binding['problem_id'].removeprefix('problem:')}",
            "ledger_id": "research-os-cognitive-events",
            "ledger_path": relative_path.as_posix(),
            "ledger_sha256": ledger_sha256,
            "chain_head_sha256": events[-1]["event_sha256"],
            "problem_contract": {
                **binding,
                "owner_locator": "problem-library/records/canonical-problems.jsonl",
            },
            "owner_snapshot_sha256": self.owner_adapter.snapshot.owner_snapshot_sha256,
            "owner_ledgers": copy.deepcopy(list(self.owner_adapter.snapshot.owner_ledger_bindings)),
            "claims_ceiling": "candidate_only",
            "event_count": len(events),
            "current_object_count": len(objects),
            "managed_ref_count": managed_ref_count,
            "opaque_ref_count": len(external_refs),
            "opaque_ref_ids": sorted(external_refs),
            "objects": objects,
            "generated_at": generated_at,
            "non_authoritative": True,
            "non_mathematical_truth": True,
            "projection_sha256": "",
        }
        projection["projection_sha256"] = canonical_json_sha256(
            {key: value for key, value in projection.items() if key != "projection_sha256"}
        )
        schema_errors = sorted(
            Draft202012Validator(self.schema, format_checker=FormatChecker()).iter_errors(projection),
            key=lambda item: list(item.absolute_path),
        )
        if schema_errors:
            path = "/".join(str(part) for part in schema_errors[0].absolute_path) or "<root>"
            raise ResearchOsError(f"derived projection fails schema at {path}: {schema_errors[0].message}")
        return projection

    def project_file(self, ledger_path: Path | str | None = None) -> dict[str, Any]:
        path = Path(ledger_path) if ledger_path is not None else Path("research/records/research-os-events.jsonl")
        if ".." in path.parts:
            raise ResearchOsError("event ledger path cannot contain '..'")
        path = self.root / path if not path.is_absolute() else path
        try:
            path.relative_to(self.root)
        except ValueError as exc:
            raise ResearchOsError("event ledger must stay inside project root") from exc
        writer = ResearchOsEventWriter(self.root, path, require_owner_binding=False)
        writer._check_parent_chain()
        if path.is_symlink():
            raise ResearchOsError(f"event ledger must be a regular file: {path}")
        if not path.is_file() and not writer.wal_path.exists():
            raise ResearchOsError(f"event ledger must be a regular file: {path}")
        with writer._locked_existing():
            if writer.wal_path.exists() or writer.wal_path.is_symlink():
                raise ResearchOsError("event ledger has an unresolved WAL; projection refuses a stale read")
            if not path.is_file():
                raise ResearchOsError(f"event ledger must be a regular file: {path}")
            raw = writer._read_bytes_unlocked()
            events = writer._parse_events(raw)
            relative = path.relative_to(self.root).as_posix()
            return self.project_events(events, ledger_sha256=_sha256_bytes(raw), ledger_path=relative)


def validate_projection(stored: Mapping[str, Any], expected: Mapping[str, Any], schema: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    schema_errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(stored),
        key=lambda item: list(item.absolute_path),
    )
    errors.extend(f"schema:{'/'.join(str(part) for part in issue.absolute_path) or '<root>'}: {issue.message}" for issue in schema_errors)
    if stored.get("projection_sha256") != canonical_json_sha256({key: value for key, value in stored.items() if key != "projection_sha256"}):
        errors.append("projection self-digest mismatch")
    if stored.get("owner_snapshot_sha256") != canonical_json_sha256(stored.get("owner_ledgers")):
        errors.append("owner snapshot digest mismatch")
    if dict(stored) != dict(expected):
        errors.append("projection is stale or nondeterministic")
    return errors


__all__ = [
    "DEFAULT_EVENT_LEDGER",
    "EXTERNAL_PREFIXES",
    "MANAGED_PREFIXES",
    "OwnerSnapshot",
    "PROJECTION_SCHEMA",
    "ResearchOsError",
    "ResearchOsEventWriter",
    "ResearchOsOwnerError",
    "ResearchOsOwnerLedgerAdapter",
    "ResearchOsProjector",
    "ResearchOsWriterError",
    "canonical_json_sha256",
    "problem_scope",
    "problem_scope_sha256",
    "problem_statement_sha256",
    "validate_projection",
]
