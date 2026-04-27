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
