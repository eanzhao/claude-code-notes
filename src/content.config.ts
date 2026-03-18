import { defineCollection, z } from "astro:content";

const docs = defineCollection({
  schema: z.object({
    title: z.string(),
    order: z.number(),
    section: z.string(),
    sectionLabel: z.string(),
    sectionOrder: z.number(),
    group: z.string().optional(),
    groupLabel: z.string().optional(),
    summary: z.string(),
    sourceUrl: z.string().optional(),
    sourceTitle: z.string().optional(),
    tags: z.array(z.string()).default([])
  })
});

export const collections = { docs };
