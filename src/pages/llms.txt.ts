import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

export const GET: APIRoute = async () => {
  const toolset = await getCollection('toolset', ({ data }) => !data.draft);
  toolset.sort(
    (a, b) => b.data.lastReviewed.getTime() - a.data.lastReviewed.getTime(),
  );

  const lines: string[] = [
    '# wro.cpp',
    '',
    '> A curated reference for working C++ developers in 2026. Premium open-source first. Hard OSS made easier. Runnable claims, freshness bar, methodology you can audit.',
    '',
    'wro.cpp is a Wroclaw-based C++ community hub. The Toolset section is the part most useful to AI coding agents: opinionated, scenario-driven, freshness-stamped reference material, with each page available as a plain-text companion at /toolset/<slug>/llms.txt.',
    '',
    '## Toolset (machine-readable)',
    '',
    '- [C++26 compiler support](https://wrocpp.github.io/toolset/compiler-support/llms.txt): per-feature, per-compiler matrix derived from godbolt examples we re-verify on every publish.',
  ];

  for (const e of toolset) {
    if (!e.data.agentInstructions) continue;
    const url = `https://wrocpp.github.io/toolset/${e.id}/llms.txt`;
    lines.push(`- [${e.data.title}](${url}): ${e.data.summary}`);
  }

  lines.push('');
  lines.push('## Toolset (human-readable)');
  lines.push('');
  lines.push('- [Toolset hub](https://wrocpp.github.io/toolset/): index of all sections, editorial principles, and "how we test" methodology.');
  for (const e of toolset) {
    const url = `https://wrocpp.github.io/toolset/${e.id}/`;
    lines.push(`- [${e.data.title}](${url}): ${e.data.summary}`);
  }

  lines.push('');
  lines.push('## Optional');
  lines.push('');
  lines.push('- [Posts](https://wrocpp.github.io/posts/): the wro.cpp blog timeline (long-form C++ articles).');
  lines.push('- [Events](https://wrocpp.github.io/events/): meetup history and upcoming sessions.');
  lines.push('');

  return new Response(lines.join('\n'), {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=3600',
    },
  });
};
