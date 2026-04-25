# Releasing posts on wro.cpp

## How publishing works

A post is **publicly visible** when BOTH of these are true:

1. Its frontmatter has `draft: false`.
2. Its `pubDate` is today or earlier (UTC-day precision).

Before either condition is met, the post stays invisible in production but is fully visible in local `npm run dev` with a `DRAFT` pill. That's deliberate — you can review the entire future backlog locally before anything goes live.

Two consequences worth naming:

- **Posts don't need a commit on their launch day.** Setting `pubDate: 2026-05-13` and `draft: false` today means the post appears on the live site on 2026-05-13 without anyone touching the repo. The daily cron build rebuilds every morning UTC, picks up "today is 2026-05-13", and the post publishes itself.
- **Drafts never leak.** Even if `pubDate` is in the past, `draft: true` keeps the post hidden. Safety net for last-minute "actually this isn't ready."

## Daily cadence

Two events rebuild and deploy the site:

| Trigger | When | Purpose |
|---|---|---|
| **`push` to `main`** | Instant | Normal edit/commit workflow. Post updates go live within ~2 minutes. |
| **Daily cron (07:00 UTC)** | Every day | Picks up scheduled posts whose `pubDate` just became today. No commit needed. |

The cron runs ~09:00 Europe/Warsaw (CEST) / ~08:00 (CET). A post with `pubDate: 2026-05-13` publishes at approximately 09:00 Warsaw time on that date.

You can also trigger a manual deploy via the **"Run workflow"** button on the Actions tab (`workflow_dispatch`).

## Accepting a post

When a post is ready to ship:

1. **Review it locally**: `cd ~/dev/wrocpp.github.io && npm run dev` — visit the post on `http://localhost:5175/posts/<slug>/`. Drafts render with an orange `DRAFT` pill.
2. **Pick the publish date**. Biweekly Wednesdays is the series rhythm. Set `pubDate: YYYY-MM-DD` in the post's frontmatter.
3. **Flip `draft: true → false`** in the frontmatter.
4. **Commit**: `git commit -am "schedule: <slug> for <pubDate>"`.
5. **Push**: `git push origin main`.
6. The site rebuilds immediately. If `pubDate` is today or past, the post is live now. If in the future, it'll appear on the first cron build after that date.

## Accepting a batch (e.g. "first 3 posts")

Same flow, one commit per post (or a single batched commit — your call). The post archive at `/posts/` sorts newest-first automatically; each scheduled post slides into place on its date.

## Cross-posting the launch

For each flagship post, a launch checklist triggered on publish day:

- [ ] Post on [r/cpp](https://reddit.com/r/cpp) with a short "why this post" summary
- [ ] Post on [Hacker News](https://news.ycombinator.com/submit) if the topic is generally-shareable
- [ ] Announce on [Wro.cpp Slack](https://wrocpp.slack.com) `#announcements`
- [ ] Cross-post on LinkedIn
- [ ] Tag the release on GitHub: `git tag post-NN && git push --tags`
- [ ] Open a Discussion thread on the [site repo](https://github.com/wrocpp/wrocpp.github.io/discussions) for reader comments

This can be automated via a separate `post-launch.yml` workflow triggered by the tag push. Not set up yet — low priority until we see how often posts land.

## Reverting

If a post needs to come down (error, policy violation, fresh approach):

1. Edit the frontmatter: `draft: true`.
2. `git commit -am "revert: <slug>" && git push`.
3. Within ~2 minutes, the post disappears from production. URLs return 404.
4. The post stays in the repo and in local dev — it's just hidden from the public site.

RSS subscribers will have seen it if they polled between publish and revert; the RSS item stays in their client until they clear it.

## Troubleshooting

**A post appeared but I didn't want it to yet.**
Set `draft: true` and push. Gone in ~2 minutes.

**A post should have appeared but hasn't.**
Check: (a) `draft: false` in frontmatter, (b) `pubDate` is today or earlier, (c) commits pushed to `main`, (d) look at the Actions tab for a failed build. The most common miss is timezone — `pubDate: 2026-05-13` goes live on 2026-05-13 07:00 UTC (cron) or on the next push, whichever happens first.

**The cron isn't running.**
GitHub Actions scheduled workflows pause after 60 days of repo inactivity. Any commit or manual `workflow_dispatch` resumes them.
