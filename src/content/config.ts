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
    testedOn: z.string().optional(),
    relatedPosts: z.array(z.string()).default([]),
    licence: z.string().optional(),
    cost: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { posts, events, speakers, toolset };
