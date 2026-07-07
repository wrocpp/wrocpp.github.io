import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';
import { isPublished, byDateDesc } from '../lib/posts';

export async function GET(context: APIContext) {
  // RSS always uses production-style filter — drafts never leak to subscribers,
  // even when serving from dev.
  const today = new Date().toISOString().slice(0, 10);
  const posts = (await getCollection('posts')).filter(
    (p) => !p.data.draft && p.data.pubDate.toISOString().slice(0, 10) <= today,
  );
  return rss({
    title: 'wro.cpp — Wrocław C++ community',
    description:
      'Modern C++ for production: safety, performance, security, compliance, and the tooling that ships C++ in cars, trading systems, and hospitals. Flagship posts, news short-form, and community content from the Wroclaw C++ scene. Most posts are AI-generated and human-reviewed; see https://wrocpp.github.io/ai.',
    site: context.site!,
    xmlns: { ai: 'https://wrocpp.github.io/ns/ai-disclosure' },
    items: posts.sort(byDateDesc).map((p) => ({
      title: p.data.title,
      description: p.data.summary,
      pubDate: p.data.pubDate,
      link: `/posts/${p.id}/`,
      categories: p.data.tags,
      customData: `<ai:declaration>${p.data.aiDisclosure}</ai:declaration>`,
    })),
  });
  // suppress unused import warning (kept for future use)
  void isPublished;
}
