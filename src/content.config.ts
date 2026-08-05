import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const board = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/board' }),
  schema: z.object({
    name: z.string(),
    role: z.string(),
    roleGroup: z.enum(['Editorial Leadership', 'Editorial Board and Reviewers', 'Advisory Board']),
    qualification: z.string(),
    designation: z.string(),
    institution: z.string().optional(),
    email: z.string().optional(),
    order: z.number().default(50),
  }),
});

const sections = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/sections' }),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    editorNote: z.string().optional(),
    order: z.number().default(50),
  }),
});

const issues = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/issues' }),
  schema: z.object({
    volume: z.number(),
    number: z.number(),
    year: z.number(),
    period: z.string(),
    status: z.enum(['Published', 'In production', 'Open for submissions']),
    editorialTitle: z.string(),
    editorialAuthor: z.string(),
    summary: z.string(),
    publicationDate: z.string().optional(),
    submissionDeadline: z.string().optional(),
    order: z.number().default(50),
  }),
});

const articles = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/articles' }),
  schema: z.object({
    title: z.string(),
    authors: z.array(z.string()),
    affiliations: z.array(z.string()).optional(),
    abstract: z.string(),
    keywords: z.array(z.string()),
    articleType: z.enum([
      'Research Article',
      'Review Article',
      'Case Comment',
      'Short Communication',
      'Book Review',
      'Editorial',
    ]),
    section: z.string(),
    issue: z.string(),
    pageRange: z.string().optional(),
    doi: z.string().optional(),
    pdf: z.string().optional(),
    receivedDate: z.string().optional(),
    acceptedDate: z.string().optional(),
    publishedDate: z.string().optional(),
    references: z.array(z.string()).optional(),
    order: z.number().default(50),
  }),
});

const announcements = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/announcements' }),
  schema: z.object({
    title: z.string(),
    date: z.string(),
    summary: z.string(),
    pinned: z.boolean().default(false),
  }),
});

const pages = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/pages' }),
  schema: z.object({
    title: z.string(),
    navLabel: z.string(),
    navGroup: z.enum(['About', 'For Authors', 'Standalone', 'Footer only']),
    summary: z.string(),
    updated: z.string(),
    order: z.number().default(50),
    showContactForm: z.boolean().default(false),
  }),
});

export const collections = { board, sections, issues, articles, announcements, pages };
