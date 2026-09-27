# 06 — Operations and Recovery

## Bootstrap sequence

A healthy run starts with environment, secrets, backend, verifier service, then project/workers. The repository's first-run flow records operator preferences and keeps credentials in gitignored configuration. Run diagnostics before starting long-lived work.

Core commands:

```text
bin/danus list [--json]
bin/danus new <project> [--roles high:3,xhigh:4] [--model M]
bin/danus assign <project>/<worker> (--task "..." | --file P | --stdin)
bin/danus start <project>[/<worker>]
bin/danus status <project>[/<worker>] [--json]
bin/danus stop <project>[/<worker>] [--force]
bin/danus finalize <project> [--paper <paper_id>] [<fact_id> ...]
```

The default roster in the supplied snapshot is three `high` and four `xhigh` workers. Treat model/effort defaults as deployment configuration rather than a universal Danus principle.

## Persistent services

`verify` is required and binds to loopback by default. The dashboard is optional and read-only. Service management uses detached sessions so processes survive the launching shell.

Typical runbook:

```text
bash scripts/services.sh up verify
bash scripts/services.sh status
bash scripts/doctor.sh
bin/danus new <project>
bin/danus assign <project>/<worker> --task "..."
bin/danus start <project>
bin/danus status <project>
```

Use `scripts/check-codex.sh` for backend readiness and `scripts/recover.sh` after machine/service restart. The service manager detects stale/foreign verify ownership so a different deployment on the same port is not mistaken for the current instance.

## Worker lifecycle

Workers run detached in their own process groups. A round is one Codex continuation session, not one tiny reasoning step. Default hard timeout is four hours; consecutive failure limit is five; max rounds may be unlimited. Control files encode pid, lock, stop flag, deadline, status, and logs.

Continuity lives in persisted stores. If a process dies, a fresh start reconstructs context from assignment, memory, and fact graph. Do not treat process identity as research state.

## `assign`

An assignment replaces that worker's `TASK.md`. It should be specific, mathematically discriminating, and consistent with current strategy. Reassign when the current task is obsolete or poorly targeted.

## `status`

Use status as a liveness/round signal. A `stuck?` label is deliberately soft because a legitimate deep round may run for hours. Diagnose with assignment quality, round age, logs, and shared progress before killing work.

## `stop`

Graceful stop writes a stop flag and lets the current round finish. `--force` terminates the process group, including an in-flight child. Prefer graceful stop unless the process is broken or immediate termination is required.

## `finalize`

Finalization records the selected verified target for a paper. With no fact id, it only suggests terminal facts and writes nothing. Every explicit target id must exist in the fact graph. Finalization does not stop workers; stopping is a separate decision.

## Recovery matrix

| Symptom | Check | Recovery |
|---|---|---|
| `fact_submit` unavailable | caller role / verify health | use worker role; restore verify service |
| project/worker missing | `list`, on-disk project metadata | recreate only if genuinely absent; do not invent state |
| stale pid | liveness and status | restart worker; persisted stores restore context |
| worker repeatedly fails | logs, consecutive failures, assignment | fix backend/config or sharpen task, then restart |
| foreign verify port | health pid vs service pid | choose distinct configured port or stop foreign process deliberately |
| configuration drift | env chain and runtime env | run doctor/recovery; prefer call-time configuration |
| selected fact later revoked | fact graph descendants | re-open affected target/paper route; rebuild from valid facts |

## Configuration precedence

The repository resolves configuration through checked-in examples, local gitignored env files, generated runtime env, and code defaults. Secrets belong only in local ignored config. Service-specific model/effort overrides fall back to neutral Danus defaults.

## Operational self-check

- required verifier healthy and belongs to this deployment;
- project target and worker assignments are explicit;
- current role has the required tool;
- all long-running state is persisted outside process memory;
- destructive/externally visible actions have operator approval;
- failure recovery preserves verified artifacts and does not bypass truth gates.
