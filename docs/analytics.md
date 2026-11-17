# Analytics on wro.cpp

The site uses **Google Analytics 4** with **Consent Mode v2**, plus three custom events tailored to a technical-blog audience.

## Setup (one-time)

1. Create a GA4 property at https://analytics.google.com (Admin -> Create Property -> Web data stream pointing at `https://wrocpp.github.io`).
2. Copy the **Measurement ID** (format: `G-XXXXXXXXXX`).
3. Set it as a build-time env var:
   - **Local dev:** add `PUBLIC_GA_ID=G-XXXXXXXXXX` to `.env` (gitignored).
   - **GitHub Pages deploy:** add a repository **secret** named `PUBLIC_GA_ID` at https://github.com/wrocpp/wrocpp.github.io/settings/secrets/actions, then expose it to the build step in `.github/workflows/deploy.yml` (uncomment the `env:` block under "Build").

If the env var is unset, the analytics script and the cookie banner render nothing -- safe for forks and preview deploys.

## What gets tracked

| Event | When | Why |
| --- | --- | --- |
| `page_view` | Every page load (built-in) | Pageviews + referrers per URL. |
| `post_read` | After every `/posts/<slug>/` page load | Funnel report: post 1 -> 2 -> 3 -> ... so you see drop-off between consecutive posts in the series. Includes `post_series_order`, `post_kind`, `post_language`. |
| `click_outbound` | Click on any external `<a href>` | Per-destination CTR (godbolt vs slack vs meetup vs github). Includes `link_url`, `link_domain`, `link_text`. |
| `scroll_depth` | Scroll past 25% / 50% / 75% / 100% | Differentiates "glanced at headline" from "actually read 1500 words". One event per threshold per page. |

All custom events fire through `gtag()`. Consent-Mode-v2 default: every category is `denied` until the visitor clicks **Accept** on the banner; while denied, GA4 still receives **cookieless pings** (aggregate counts only, no PII / no ads modeling).

## UTM tagging via `/push-to-buffer`

`scripts/push-to-buffer.py` rewrites the bare `https://wrocpp.github.io/posts/<slug>/` URL inside each caption to:

```
https://wrocpp.github.io/posts/<slug>/?utm_source=<linkedin|facebook>&utm_medium=social&utm_campaign=post-<NN>
```

GA4's **Acquisition -> Traffic acquisition** report then breaks each post's traffic down by source: LinkedIn vs Facebook vs direct/Slack vs organic search.

If you author your own URL with `?` or `#` already in it, the rewrite is skipped -- your tagging wins.

## Privacy & GDPR

- **Cookieless by default:** Consent Mode v2 starts with all categories `denied`. The browser receives no GA-set cookies until the visitor clicks Accept.
- **Banner:** appears on first visit; choice is persisted in `localStorage` under the key `wrocpp:consent` (`granted` or `denied`). No nag.
- **No ads, no remarketing:** `ad_storage` and `ad_personalization` start denied and stay denied even on Accept (we only flip the analytics-related categories on Accept; ads-related stay denied -- see CookieConsent.astro for the consent state map if you want to change this).
- **`anonymize_ip: true`** is enforced in the gtag config (so even granted-consent visitors don't have their IP recorded).

## Local testing

```bash
# Dev mode -- analytics script renders if PUBLIC_GA_ID is in .env.
PUBLIC_GA_ID=G-XXXXXXXXXX npm run dev
```

In Chrome DevTools, open the **Network** tab and filter for `google-analytics.com` or `analytics.google.com`. Click around to see `collect?...` beacons fire (page_view, then your interaction events).

GA4's **Realtime** report (https://analytics.google.com -> Reports -> Realtime) shows your own visit within 30 seconds.

## Reading the data

Once you have a few posts of traffic, the questions to answer:

- Which post drives the most pageviews? **Reports -> Engagement -> Pages and screens.**
- Where does the traffic come from? **Reports -> Acquisition -> Traffic acquisition** (UTM-tagged).
- Is the series funnel converging? **Explore -> Funnel exploration**, steps = `post_read` filtered by `post_series_order` 1, 2, 3 ...
- Do readers click through to godbolt? **Reports -> Engagement -> Events**, filter `click_outbound` by `link_domain = godbolt.org`.
- Is the audience growing? **Reports -> Acquisition -> User acquisition** by week.

Slack member count, Meetup RSVPs, and GitHub stars are not in GA4 -- check those manually once a week. The `click_outbound` event tells you the click-through, but the conversion rate (clicked -> joined Slack) requires correlating with Slack admin.

## Monthly social review

`scripts/social-analytics-report.py` joins the LinkedIn company page's post analytics with GA4 site traffic and
the repository, to learn which posts earn attention. This section is the **pre-registration**: the questions,
the metrics, the thresholds and the verdict rule are fixed here, in a commit that comes before the export is
opened, so they cannot be tuned to the result. A report cites the commit of this file.

### Privacy

The raw exports and every per-post table are private, and this repository is public. They live in
`.notes/analytics/YYYY-MM/`, which `.gitignore` ignores. The script refuses to write into any directory that
git does not ignore (exit 3). Only aggregate rules, this document and the script are committed.

### The monthly export

**GA4**, standard Reports (not Explorations, whose default retention would drop the oldest weeks). Custom date
range for the review window, no comparison, rows per page at the maximum, then Share > Download File > CSV.

| | `ga4-linkedin-landing-by-date.csv` | `ga4-all-sources-by-landing.csv` |
|---|---|---|
| Report | Engagement > Landing page | Acquisition > Traffic acquisition |
| Dimensions | Landing page + query string, then Date | Session source / medium, then Landing page + query string |
| Filter | Session source matches regex `linkedin\|lnkd` (or "contains" `linkedin`) | none |
| Metrics | Sessions, Engaged sessions, Engagement rate, Average engagement time per session | the same |

Join on the landing page and the source. Never join on `utm_campaign`: its value `post-NN` is a series
number and repeats across series.

**LinkedIn**: the company page's Updates analytics, custom range for the window, Export. Save the per-post
sheet as `linkedin-posts.csv` and the daily sheet as `linkedin-daily.csv` (CSV UTF-8). Needed columns: post
text or title, post link, created date and time, impressions, clicks, reactions, comments, reposts.

GA4 counts are lower bounds, because visitors who decline analytics consent send only cookieless pings.

### Questions

Each hypothesis compares group A with group B on one primary metric, and only these four produce a verdict.
Everything else in a report is descriptive.

| # | Claim | A | B | Primary metric |
|---|---|---|---|---|
| H1 | A card headline with a checkable number or a reframed habit earns more attention | `hook_number` yes or `hook_reframe` yes | neither | `imp_index` |
| H2 | News earns more attention than evergreen | tag `news` | no tag `news` | `imp_index` |
| H3 | Naming a person draws more conversation | `person_role` answer or credit | none | `comment_repost_rate` |
| H4 | A runnable demo brings more readers to the site | `content_type` demo | code or commentary | `site_sessions_per_1000` |

The metrics:

- `imp_index`: a post's impressions divided by the median impressions of the other mature, undisturbed posts
  within `TREND_DAYS` days of it. This removes follower growth.
- `comment_repost_rate`: comments plus reposts per 1,000 impressions, pooled over the group, because most posts
  have none.
- `site_sessions_per_1000`: GA4 sessions from LinkedIn in the first `FIRST_DAYS` days after sending, per 1,000
  impressions.

`hook_number`, `hook_reframe` and `person_role` are labelled blind, from the text only, by the rules in
[social-labels-codebook.md](social-labels-codebook.md).

### Which posts are compared

Only mature, undisturbed posts: sent at least `MATURITY_DAYS` days before the export, not on a day listed in
`DISTURBANCES` in the script, and sent once. Others are listed separately and never counted as zero. A post
above `OUTLIER_MULTIPLE` times the median impressions is an outlier, and every table shows the result with and
without outliers. Every factor table also shows a placebo row (even against odd calendar days), which is the
noise floor.

### The verdict rule

With r the ratio of the group medians (A over B), or the pooled ratio for `comment_repost_rate`:

- **Too little data**: either group has fewer than `MIN_GROUP` posts.
- **Supported**: r is at least `EFFECT_RATIO`, and r stays above 1 after dropping A's best post, and r is above 1
  on both sides of `SPLIT_DATE` (at least `MIN_PER_HALF` posts of the smaller group on each side), and r
  exceeds the placebo ratio.
- **Contradicted**: r is at most 1 over the whole window and on both sides of `SPLIT_DATE`.
- Anything else is **too little data**, reported with its lean and its numbers.

Cadence and timing are reported but not given verdicts. The posting hour and the slot are one variable (every
16:00Z post is a second post of the day), and most double days fall in one month, so the data cannot separate
them. Those questions go to experiments.

### Reports and rule changes

The report starts with its own coverage: how many LinkedIn rows were matched, and the share of impressions
they hold. It is complete only if that share is at least `COVERAGE_MIN`; otherwise the script exits with an
error, and `--allow-unmatched` marks the report INCOMPLETE.

A playbook rule (`docs/STYLE.md`, the `advertise-post` skill) changes only when a verdict supports it, and the
edit cites the group sizes, both medians, r, and "holds on both sides of the split". A contradicted claim is
softened or removed. A claim with too little data stays as it is, and the question becomes an experiment.

### Registered values

`scripts/tests/test_social_analytics.py` fails if these differ from the constants in the script.

<!-- preregistration:start -->
MATURITY_DAYS = 7
MIN_GROUP = 10
EFFECT_RATIO = 1.5
OUTLIER_MULTIPLE = 5
TREND_DAYS = 7
FIRST_DAYS = 3
SPLIT_DATE = 2026-09-13
MIN_PER_HALF = 5
AGREEMENT_MIN = 0.8
COVERAGE_MIN = 0.95
PREFIX_CHARS = 60
SLACK_DAYS = 3
FUZZY_MIN = 0.85
H1 = imp_index
H2 = imp_index
H3 = comment_repost_rate
H4 = site_sessions_per_1000
<!-- preregistration:end -->
