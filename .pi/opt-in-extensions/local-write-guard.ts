// 可选的本地研究护栏：只检查工具调用，不拥有续行、证据或数学准入权。
import { lstatSync, readFileSync, realpathSync } from "node:fs";
import { isAbsolute, relative, resolve, sep } from "node:path";
import type { ExtensionAPI, ExtensionContext } from "@earendil-works/pi-coding-agent";

interface GuardPolicy {
  schema_version: string;
  repository_root: string;
  profile_file: string;
  scope: {
    session_id: string;
    lease_epoch: number;
    problem_id: string;
    problem_contract_sha256: string;
    statement_sha256: string;
  };
  protected_relative_paths: string[];
}

function within(root: string, path: string): boolean {
  const rel = relative(root, path);
  return rel === "" || (rel !== ".." && !rel.startsWith(`..${sep}`) && !isAbsolute(rel));
}

function privateFile(path: string): boolean {
  try {
    const s = lstatSync(path);
    return s.isFile() && !s.isSymbolicLink() && (s.mode & 0o777) === 0o600;
  } catch {
    return false;
  }
}

function policyValid(policy: any): policy is GuardPolicy {
  if (!policy || policy.schema_version !== "vibemathing.local-write-guard.v1") return false;
  if (typeof policy.repository_root !== "string" || !isAbsolute(policy.repository_root)
    || typeof policy.profile_file !== "string" || !isAbsolute(policy.profile_file)) return false;
  if (!Array.isArray(policy.protected_relative_paths) || !policy.protected_relative_paths.length) return false;
  if (new Set(policy.protected_relative_paths).size !== policy.protected_relative_paths.length) return false;
  for (const path of policy.protected_relative_paths) {
    if (typeof path !== "string" || !path || isAbsolute(path) || path.split(/[\\/]/).some((part) => part === ".." || part === "." || !part)) return false;
  }
  const scope = policy.scope;
  return scope && typeof scope.session_id === "string" && scope.session_id.length > 0
    && Number.isSafeInteger(scope.lease_epoch) && scope.lease_epoch > 0
    && typeof scope.problem_id === "string" && scope.problem_id.length > 0
    && /^[a-f0-9]{64}$/.test(scope.problem_contract_sha256)
    && /^[a-f0-9]{64}$/.test(scope.statement_sha256);
}

// 即使策略缺失，扩展也会安装拦截器；文件工具与 Shell 均不可静默放行。
export function loadGuardPolicy(path: string | undefined): GuardPolicy | undefined {
  if (!path || !privateFile(path)) return undefined;
  try {
    const value = JSON.parse(readFileSync(path, "utf8"));
    return policyValid(value) ? value : undefined;
  } catch {
    return undefined;
  }
}

function scopeMatches(
  ctx: ExtensionContext, policy: GuardPolicy, readProfile: (path: string) => any,
  checkPrivateFile: (path: string) => boolean,
): boolean {
  try {
    if (!ctx.isProjectTrusted() || ctx.sessionManager.getSessionId() !== policy.scope.session_id) return false;
    if (realpathSync(ctx.cwd) !== realpathSync(policy.repository_root)) return false;
    if (!checkPrivateFile(policy.profile_file)) return false;
    const profile = readProfile(policy.profile_file);
    return profile.channel === "local_pi" && profile.actor_state === "ACTIVE"
      && profile.required_session_id === policy.scope.session_id
      && profile.lease_epoch === policy.scope.lease_epoch
      && profile.problem_id === policy.scope.problem_id
      && profile.problem_contract_sha256 === policy.scope.problem_contract_sha256
      && profile.statement_sha256 === policy.scope.statement_sha256
      && profile.truth_plane_write === false && profile.truth_ledger_write === false;
  } catch {
    return false;
  }
}

function targetPath(path: unknown, cwd: string): { lexical: string; physical: string } | undefined {
  if (typeof path !== "string" || !path || path.includes("\0")) return undefined;
  let lexical: string;
  try { lexical = resolve(cwd, path); }
  catch { return undefined; }
  let probe = lexical;
  const tail: string[] = [];
  for (;;) {
    try {
      let physical = realpathSync(probe);
      for (const part of tail) physical = resolve(physical, part);
      return { lexical, physical };
    } catch (error: any) {
      if (error?.code !== "ENOENT" && error?.code !== "ENOTDIR") return undefined;
      const parent = resolve(probe, "..");
      if (parent === probe) return undefined;
      try {
        if (lstatSync(probe).isSymbolicLink()) return undefined;
      } catch (statError: any) {
        if (statError?.code !== "ENOENT" && statError?.code !== "ENOTDIR") return undefined;
      }
      tail.unshift(relative(parent, probe));
      probe = parent;
    }
  }
}

export function protectedPathDecision(path: unknown, cwd: string, policy: GuardPolicy) {
  if (!policyValid(policy) || !isAbsolute(policy.repository_root)) return { allowed: false, reason: "invalid_policy" };
  const target = targetPath(path, cwd);
  if (!target) return { allowed: false, reason: "unresolvable_path" };
  for (const relativePath of policy.protected_relative_paths) {
    const lexical = resolve(policy.repository_root, relativePath);
    if (!within(policy.repository_root, lexical)) return { allowed: false, reason: "invalid_protected_root" };
    let physical: string;
    try { physical = realpathSync(lexical); }
    catch { return { allowed: false, reason: "protected_root_missing_or_unreadable" }; }
    if (within(lexical, target.lexical) || within(physical, target.physical)) {
      return { allowed: false, reason: "protected_path" };
    }
  }
  return { allowed: true, reason: "outside_protected_paths" };
}

const MUTATING_TOOLS = new Set(["write", "edit", "bash", "powershell"]);
export function guardToolCall(
  event: { toolName: string; input?: unknown }, ctx: ExtensionContext,
  policy: GuardPolicy | undefined,
  readProfile: (path: string) => any = (path) => JSON.parse(readFileSync(path, "utf8")),
  checkPrivateFile: (path: string) => boolean = privateFile,
) {
  if (!MUTATING_TOOLS.has(event.toolName)) return undefined;
  const block = (reason: string) => ({ block: true as const, reason: `local-write-guard: ${reason}` });
  if (!policy || !policyValid(policy) || !scopeMatches(ctx, policy, readProfile, checkPrivateFile)) {
    return block("policy_or_identity_mismatch");
  }
  // 任意 Shell 可绕过词法扫描；无独立文件系统隔离时不能凭正则宣称保护。
  if (event.toolName === "bash" || event.toolName === "powershell") return block("shell_requires_independent_confinement");
  if (!event.input || typeof event.input !== "object") return block("missing_path");
  const input = event.input as Record<string, unknown>;
  const paths = ["path", "file_path"].filter((key) => Object.hasOwn(input, key)).map((key) => input[key]);
  if (!paths.length) return block("missing_path");
  for (const path of paths) {
    const result = protectedPathDecision(path, ctx.cwd, policy);
    if (!result.allowed) return block(result.reason);
  }
  return undefined;
}

export default function localWriteGuard(pi: ExtensionAPI) {
  const policy = loadGuardPolicy(process.env.VIBEMATH_LOCAL_WRITE_GUARD_POLICY);
  pi.on("tool_call", (event, ctx) => guardToolCall(event, ctx, policy));
}
