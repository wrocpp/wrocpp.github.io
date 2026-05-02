import type { APIRoute, GetStaticPaths } from 'astro';
import { getCollection } from 'astro:content';

export const getStaticPaths: GetStaticPaths = async () => {
  const entries = await getCollection('toolset', ({ data }) => !data.draft);
  return entries
    .filter((e) => e.data.agentInstructions)
    .map((entry) => ({
      params: { slug: entry.slug },
      props: { entry },
    }));
};

export const GET: APIRoute = async ({ props }) => {
  const { entry } = props as { entry: Awaited<ReturnType<typeof getCollection<'toolset'>>>[number] };
  const { title, summary, lastReviewed, agentInstructions } = entry.data;
  const reviewed = lastReviewed.toISOString().slice(0, 10);

  const body = [
    `# ${title}`,
    '',
    `> ${summary}`,
    '',
    `Reviewed: ${reviewed}`,
    `Source:   https://wrocpp.github.io/toolset/${entry.slug}/`,
    '',
    '---',
    '',
    agentInstructions ?? '',
    '',
  ].join('\n');

  return new Response(body, {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=3600',
    },
  });
};
