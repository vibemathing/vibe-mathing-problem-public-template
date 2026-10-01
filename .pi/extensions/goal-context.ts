// MIT; 显式受信 session 的原生 compaction 清单投影；未配置时不调用模型/存储。
import { readFileSync, lstatSync, realpathSync } from 'node:fs';
import { resolve } from 'node:path';
import { compact, SettingsManager } from '@earendil-works/pi-coding-agent';
import { cleanPrevious, finalizeCompaction, projectMessages } from './goal-context-core.mjs';

export function registerEfficiency(pi, dependencies = { compact, SettingsManager }, binding = undefined) {
  let config = binding;
  if (!config) {
    const file = process.env.VIBE_GOAL_CONTEXT_CONFIG;
    if (!file) return; // 不额外扫描研究源、不启动任何模型或子进程。
    const info = lstatSync(file);
    if (!info.isFile() || info.isSymbolicLink() || info.uid !== process.getuid?.() ||
        (info.mode & 0o077) !== 0 || info.size > 16 * 1024 || realpathSync(file) !== file) {
      throw new Error('上下文配置必须为 owner-only 普通文件');
    }
    config = JSON.parse(readFileSync(file, 'utf8'));
  }
  if (config.schema_version !== 'goal-context.v1' || typeof config.session_id !== 'string' ||
      !config.session_id || typeof config.repository_root !== 'string' ||
      !config.repository_root.startsWith('/') || resolve(config.repository_root) !== config.repository_root) {
    throw new Error('上下文配置身份不完整');
  }
  const matches = ctx => ctx.isProjectTrusted?.() === true &&
    ctx.sessionManager.getSessionId() === config.session_id &&
    resolve(ctx.cwd) === config.repository_root;
  pi.on('context', (event, ctx) => matches(ctx)
    ? { messages: projectMessages(event.messages, ctx.sessionManager.getBranch()) } : undefined);
  pi.on('session_before_compact', async (event, ctx) => {
    if (!matches(ctx)) return;
    if (event.signal.aborted || !ctx.model) return { cancel: true };
    try {
      const preparation = cleanPrevious(event.preparation, event.branchEntries);
      const retry = dependencies.SettingsManager.create(ctx.cwd).getRetrySettings();
      const result = await dependencies.compact(preparation, ctx.model, undefined, undefined,
        event.customInstructions, event.signal, pi.getThinkingLevel(),
        (model, context, options) => ctx.modelRegistry.streamSimple(model, context, options),
        undefined, retry, undefined, undefined);
      if (event.signal.aborted) return { cancel: true };
      return { compaction: finalizeCompaction(result, event.branchEntries) };
    } catch {
      // 不保存残缺摘要、不在此另启第二次模型请求；保留会话恢复点。
      if (ctx.hasUI) ctx.ui.notify('压缩失败，原会话与恢复点保留。', 'error');
      return { cancel: true };
    }
  });
}

export default function (pi) { registerEfficiency(pi); }
