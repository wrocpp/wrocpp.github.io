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
 *
 * PREFLIGHT (`WROCPP_RENDER_ALL=1`): render future-dated posts too.
 *
 * The date gate has a sharp edge. A production build never renders a post
 * until its pubDate arrives, so a post that fails to render is invisible to
 * every local build and every CI run right up until the morning it publishes,
 * at which point it takes down that day's deploy and every one after it. That
 * happened on 2026-08-12: `{fmt}` in prose parsed as a JSX expression, three
 * scheduled deploys failed, and the social post fired at 08:00Z pointing at a
 * page that was not there.
 *
 * `npm run check:future` builds with this flag so every scheduled post is
 * actually rendered while it can still be fixed cheaply.
 */
export function isPublished(post: CollectionEntry<'posts'>): boolean {
  if (import.meta.env.DEV) return true;
  if (import.meta.env.WROCPP_RENDER_ALL) return !post.data.draft;
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
