import test from "node:test";
import assert from "node:assert/strict";
import { closeSync, constants, openSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import localWriteGuard, { guardToolCall, loadGuardPolicy, protectedPathDecision } from "../.pi/opt-in-extensions/local-write-guard.ts";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const policy = {
  schema_version: "vibemathing.local-write-guard.v1",
  repository_root: root,
  profile_file: "/private/synthetic-profile.json",
  scope: {
    session_id: "synthetic-session",
    lease_epoch: 1,
    problem_id: "problem:synthetic-only",
    problem_contract_sha256: "a".repeat(64),
    statement_sha256: "b".repeat(64),
  },
  protected_relative_paths: [".pi/skills"],
};
const profile = {
  actor_state: "ACTIVE", channel: "local_pi", required_session_id: policy.scope.session_id,
  lease_epoch: policy.scope.lease_epoch, problem_id: policy.scope.problem_id,
  problem_contract_sha256: policy.scope.problem_contract_sha256,
  statement_sha256: policy.scope.statement_sha256,
  truth_plane_write: false, truth_ledger_write: false,
};
const ctx = {
  cwd: root, hasUI: false, isProjectTrusted: () => true,
  sessionManager: { getSessionId: () => policy.scope.session_id },
};
function call(toolName, input, activePolicy = policy, context = ctx, activeProfile = profile) {
  return guardToolCall({ toolName, input }, context, activePolicy, () => activeProfile, () => true);
}

test("文件工具保护词法路径与物理别名，不阻止普通候选文件", () => {
  assert.equal(call("write", { path: ".pi/skills/solve/probe.txt" })?.block, true);
  assert.equal(call("edit", { file_path: ".pi/skills/solve/probe.txt" })?.block, true);
  assert.equal(call("write", { path: ".pi/skills/../skills/probe.txt" })?.block, true);
  assert.equal(call("write", { path: "research/artifacts/candidates/probe.txt" }), undefined);
  assert.equal(call("read", { path: ".pi/skills/solve/SKILL.md" }), undefined);
  const fd = openSync(resolve(root, ".pi/skills"), constants.O_RDONLY | constants.O_DIRECTORY);
  try {
    const alias = `/proc/self/fd/${fd}/solve/probe.txt`;
    assert.equal(protectedPathDecision(alias, root, policy).allowed, false);
  } finally {
    closeSync(fd);
  }
});

test("缺少保护目录、畸形路径或错误身份都拒绝写工具", () => {
  assert.equal(call("write", { path: "research/artifacts/candidates/probe.txt" }, {
    ...policy, protected_relative_paths: ["missing-protected-root"],
  })?.block, true);
  assert.equal(call("write", {})?.block, true);
  assert.equal(call("write", { path: "" })?.block, true);
  assert.equal(call("write", { path: "ok.txt", file_path: ".pi/skills/probe.txt" })?.block, true);
  assert.equal(call("write", { path: "ok.txt" }, undefined), undefined); // 实参省略使用有效策略
  assert.equal(guardToolCall({ toolName: "write", input: { path: "ok.txt" } }, ctx, undefined)?.block, true);
  assert.equal(call("write", { path: "ok.txt" }, policy, { ...ctx, isProjectTrusted: () => false })?.block, true);
  assert.equal(call("write", { path: "ok.txt" }, policy, { ...ctx, sessionManager: { getSessionId: () => "other" } })?.block, true);
  assert.equal(call("write", { path: "ok.txt" }, policy, ctx, { ...profile, lease_epoch: 2 })?.block, true);
  assert.equal(protectedPathDecision("ok.txt", root, { ...policy, protected_relative_paths: ["../outside"] }).allowed, false);
  assert.equal(loadGuardPolicy(undefined), undefined);
});

test("任何 Shell 都拒绝：旧 Hook 的 awk 内嵌写入不得靠词法扫描放行", () => {
  const shell = `awk 'BEGIN { print 1 > ".pi/skills/solve/probe.txt" }'`;
  for (const toolName of ["bash", "powershell"]) {
    assert.match(call(toolName, { command: shell })?.reason || "", /shell_requires_independent_confinement/);
    assert.equal(call(toolName, { command: "ls .pi/skills" })?.block, true);
  }
});

test("不安装任何续行钩子；策略未配置时仍拒绝写入", () => {
  const saved = process.env.VIBEMATH_LOCAL_WRITE_GUARD_POLICY;
  try {
    delete process.env.VIBEMATH_LOCAL_WRITE_GUARD_POLICY;
    const handlers = new Map();
    localWriteGuard({ on: (event, handler) => handlers.set(event, handler) });
    assert.deepEqual([...handlers.keys()], ["tool_call"]);
    assert.equal(handlers.get("tool_call")({ toolName: "write", input: { path: "ok.txt" } }, ctx)?.block, true);
  } finally {
    if (saved === undefined) delete process.env.VIBEMATH_LOCAL_WRITE_GUARD_POLICY;
    else process.env.VIBEMATH_LOCAL_WRITE_GUARD_POLICY = saved;
  }
});
