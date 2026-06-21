import { defineCollection, z } from 'astro:content';

const resources = defineCollection({
  type: 'data',
  schema: z.object({
    title: z.string(),
    url: z.string().url(),
    description: z.string(),
    type: z.enum(['blog', 'podcast', 'channel', 'newsletter', 'tool', 'site']),
    tags: z.array(z.string()),
    status: z.enum(['active', 'archived']).default('active'),
    added: z.coerce.date(),
    note: z.string().optional(),
  }),
});

const links = defineCollection({
  type: 'data',
  schema: z.object({
    title: z.string(),
    url: z.string().url(),
    description: z.string(),
    type: z.enum(['article', 'video', 'post', 'paper', 'thread', 'tool', 'episode']),
    tags: z.array(z.string()),
    date: z.coerce.date(),
    added: z.coerce.date(),
    note: z.string().optional(),
    resource: z.string().optional(),
  }),
});

const til = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    tags: z.array(z.string()),
    source_url: z.string().url().optional(),
    source_title: z.string().optional(),
  }),
});

export const collections = { resources, links, til };
