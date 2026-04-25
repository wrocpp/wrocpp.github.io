import type { CollectionEntry } from 'astro:content';

/**
 * Is a post publicly visible?
 *
 * Rules:
 *  - In `npm run dev` (local): EVERY post is visible, including drafts.
 *  - In production: post must have `draft: false` AND `pubDate` must be today
 *    or earlier (UTC-day precision).
 *
 * This lets authors schedule future posts by setting a `pubDate`:
 *   - Write the post, set `pubDate: 2026-05-13`, flip `draft: false`, commit.
 *   - On 2026-05-13 the daily cron build publishes it automatically.
 *   - Before that day it's invisible in production, visible in dev for review.
 */
export function isPublished(post: CollectionEntry<'posts'>): boolean {
  if (import.meta.env.DEV) return true;
  if (post.data.draft) return false;
  const today = new Date().toISOString().slice(0, 10);     // YYYY-MM-DD, UTC
  const pub = post.data.pubDate.toISOString().slice(0, 10);
  return pub <= today;
}

/**
 * Sort posts newest-first by pubDate.
 */
export function byDateDesc<T extends CollectionEntry<'posts'>>(a: T, b: T): number {
  return b.data.pubDate.valueOf() - a.data.pubDate.valueOf();
}
