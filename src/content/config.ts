import { defineCollection, z } from 'astro:content';

const posts = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    slug: z.string().optional(), // falls back to file name if omitted
    pubDate: z.date(),
    updatedDate: z.date().optional(),
    author: z.string().default('filip-sajdak'),
    language: z.enum(['en', 'pl']).default('en'),
    kind: z.enum(['flagship', 'short', 'event-recap']).default('flagship'),
    series: z.string().optional(),
    series_order: z.number().optional(),
    audience: z.enum(['polyglot', 'working-cpp', 'mixed']).default('working-cpp'),
    tags: z.array(z.string()).default([]),
    summary: z.string(),
    cover: z.string().optional(),
    draft: z.boolean().default(false),
    discussion: z.string().url().optional(),
    godbolt_links: z
      .array(
        z.object({
          label: z.string(),
          url: z.string().url(),
        }),
      )
      .optional(),
  }),
});

const events = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    /** Episode number, e.g. 36 for "Wro.cpp #36". */
    episode: z.number().int().positive().optional(),
    date: z.date(),
    endDate: z.date().optional(),
    kind: z.enum(['meetup-online', 'meetup-in-person', 'cfp', 'conference']).default('meetup-online'),
    location: z.string().optional(),
    venue: z.string().optional(),
    venueUrl: z.string().url().optional(),
    streamUrl: z.string().url().optional(),
    /** Link to the meetup.com event page. */
    meetupUrl: z.string().url().optional(),
    /** Primary recording (e.g., the full meetup stream). Individual talk recordings go on each talk. */
    recordingUrl: z.string().url().optional(),
    registrationUrl: z.string().url().optional(),
    language: z.enum(['en', 'pl']).default('pl'),
    summary: z.string(),
    /** Actual attendee count for past events. */
    attendees: z.number().int().nonnegative().optional(),
    talks: z
      .array(
        z.object({
          title: z.string(),
          speaker: z.string(),
          abstract: z.string().optional(),
          recordingUrl: z.string().url().optional(),
          slidesUrl: z.string().url().optional(),
        }),
      )
      .optional(),
    draft: z.boolean().default(false),
  }),
});

const speakers = defineCollection({
  type: 'content',
  schema: z.object({
    name: z.string(),
    affiliation: z.string().optional(),
    bio: z.string(),
    links: z
      .object({
        website: z.string().url().optional(),
        github: z.string().optional(),
        linkedin: z.string().optional(),
        twitter: z.string().optional(),
        mastodon: z.string().optional(),
      })
      .optional(),
  }),
});

const toolset = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    slug: z.string().optional(),
    summary: z.string(),
    kind: z.enum(['matrix', 'curated', 'recipe', 'integration']),
    tags: z.array(z.string()).default([]),
    lastReviewed: z.coerce.date(),
    nextReviewBy: z.coerce.date().optional(),
    /**
     * Public launch date. Distinct from lastReviewed: lastReviewed
     * tracks "is this still accurate" (refreshes quarterly); launchDate
     * is the one-time ship event. Page is always-live the moment the
     * MR merges -- no isPublished gating. launchDate drives Buffer
     * scheduling for the social ad.
     */
    launchDate: z.coerce.date().optional(),
    testedOn: z.string().optional(),
    relatedPosts: z.array(z.string()).default([]),
    licence: z.string().optional(),
    cost: z.string().optional(),
    draft: z.boolean().default(false),
    /**
     * Topical cluster shown as a section header on /toolset/. URLs stay
     * flat (/toolset/<slug>/); cluster only drives hub grouping.
     */
    cluster: z
      .enum([
        'safety',
        'performance',
        'security',
        'compliance',
        'ai-tooling',
        'reflection',
        'general',
      ])
      .default('general'),
    /**
     * Pre-built Docker image readers can pull to reproduce every claim
     * on the page locally. e.g. "ghcr.io/wrocpp/cpp-safety:2026-05".
     */
    containerImage: z.string().optional(),
    /**
     * Entry-point script inside the container, relative to the working
     * directory the reader mounts. e.g. "scripts/run-asan.sh".
     */
    containerEntry: z.string().optional(),
    /**
     * Pinned commit URL in the C++ examples repo so readers can clone
     * the source the container runs against.
     */
    exampleRepo: z.string().url().optional(),
    /**
     * Concise instructions an AI agent can fetch and act on. Rendered as
     * /toolset/<slug>/llms.txt and indexed in /llms.txt at the site root
     * (per https://llmstxt.org/).
     */
    agentInstructions: z.string().optional(),
    /**
     * SHA256 hex of the body (everything after the closing frontmatter
     * delimiter). Stale-snapshot guard for agentInstructions: edit the
     * body and the hash drifts; the prebuild check (scripts/
     * check-llms-sync.py) refuses to ship until you re-review
     * agentInstructions and re-record the hash. Missing the field is
     * tolerated only on entries with NO agentInstructions.
     */
    bodyHash: z.string().optional(),
  }),
});

export const collections = { posts, events, speakers, toolset };
