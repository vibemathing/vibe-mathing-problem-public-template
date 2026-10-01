// 仅处理 Pi 自动附加、且与元数据逐字相符的尾部文件清单；不改数学正文。
import { createHash } from 'node:crypto';
export const digest = text => createHash('sha256').update(text).digest('hex');

export function fileSuffix(details) {
  const parts = [];
  for (const [key, tag] of [['readFiles', 'read-files'], ['modifiedFiles', 'modified-files']]) {
    const paths = details?.[key];
    if (!Array.isArray(paths) || paths.some(p => typeof p !== 'string')) return '';
    if (paths.length) parts.push(`<${tag}>\n${paths.join('\n')}\n</${tag}>`);
  }
  return parts.length ? '\n\n' + parts.join('\n\n') : '';
}

export function projectSummary(summary, details) {
  const suffix = fileSuffix(details);
  if (!suffix || typeof summary !== 'string' || !summary.endsWith(suffix)) return summary;
  const body = summary.slice(0, -suffix.length);
  return body + `\n\n[历史文件清单保存在本会话 compaction entry 的 details；SHA256=${digest(suffix)}；非数学证据。]`;
}

export function cleanPrevious(preparation, branchEntries) {
  const source = [...branchEntries].reverse().find(e => e.type === 'compaction' && e.summary === preparation.previousSummary);
  return { ...preparation, previousSummary: source
    ? projectSummary(preparation.previousSummary, source.details) : preparation.previousSummary };
}

export function projectMessages(messages, branchEntries) {
  const sources = new Map(branchEntries.filter(e => e.type === 'compaction').map(e => [e.summary, e.details]));
  return messages.map(message => message.role === 'compactionSummary' && sources.has(message.summary)
    ? { ...message, summary: projectSummary(message.summary, sources.get(message.summary)) } : message);
}

export function finalizeCompaction(result, branchEntries) {
  const previous = [...branchEntries].reverse().find(e => e.type === 'compaction');
  return { ...result, summary: projectSummary(result.summary, result.details), details: {
    ...result.details,
    efficiencyVersion: '0.1.0',
    previousCatalogEntryId: previous?.id ?? null,
    fileCatalogSha256: digest(fileSuffix(result.details)),
  } };
}
