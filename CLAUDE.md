# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Personal curation site built with Astro 5 + Tailwind CSS v4. Content is YAML/MDX files in `src/content/`. Deployed to GitHub Pages via GitHub Actions on push to `main`.

## Commands

- `npm run dev` — local dev server at localhost:4321 (search inactive)
- `npm run build` — Astro build + Pagefind search index generation
- `npm run preview` — serve built `dist/` (search active)

Search only works after `npm run build && npm run preview` — it is not available in dev mode.

## Content schemas

All content lives in `src/content/`. Use the Zod schemas in `src/content/config.ts` as the source of truth.

**Links** (`src/content/links/YYYY-MM-DD-slug.yaml`)
```yaml
title: string
url: URL
description: string        # 1–2 sentences
type: article | video | post | paper | thread | tool | episode
tags: [string]
date: YYYY-MM-DD           # publication date (shown in card)
added: YYYY-MM-DD          # date visited/saved (used for chronological sort)
note: string               # optional personal take
ai_note: boolean           # optional — true (default) = AI-assisted note; false = written in own words
resource: slug             # optional — parent resource slug
```

**TILs** (`src/content/til/YYYY-MM-DD-slug.mdx`)
```yaml
---
title: string
date: YYYY-MM-DD
tags: [string]
source_url: URL            # optional
source_title: string       # optional
ai_note: boolean           # optional — true (default) = AI-assisted; false = written in own words
---
```
Body: 1–5 sentences of markdown. No preamble ("In this post…"). Write the insight directly.

**Resources** (`src/content/resources/slug.yaml`)
```yaml
title: string
url: URL
description: string        # 1–2 sentences
type: blog | podcast | channel | newsletter | tool | site
tags: [string]
status: active | archived  # default: active
added: YYYY-MM-DD
note: string               # optional
ai_note: boolean           # optional — true (default) = AI-assisted; false = own words
```

## YAML gotchas

- **Titles with double quotes**: If a title contains `"quoted"` text, wrap the entire value in single quotes — `title: '"AI-native" mandates...'` — otherwise js-yaml treats the first `"` as a string delimiter and fails with "bad indentation of a mapping entry".
- **Notes/descriptions with colons**: If a `note` or `description` value contains a colon (e.g. `"The part that stuck: …"`), wrap the entire value in double quotes — `note: "…stuck: …"` — otherwise js-yaml parses the colon as a mapping separator.

## Conventions

- **Link vs TIL**: A Link points to an external piece of content. A TIL is a short learned fact written in first person from reading that content.
- **Link vs Resource**: A Resource is the home of something ongoing (a blog, podcast, newsletter). A Link is a single piece from it.
- **Slugs**: lowercase, hyphens only, max ~5 words.
- **Fetching content**: Use this fallback chain to get clean markdown from a URL:
  1. defuddle: `curl -s https://defuddle.md/example.com/post` (strip `https://` from the target URL)
  2. Jina Reader: `curl -s https://r.jina.ai/https://example.com/post`
  3. WebFetch tool

- **Local page archive**: After fetching, always save the raw markdown to `ref-sources/YYYY-MM-DD-slug.md` (matching the content file slug). This directory is gitignored — it's a local-only archive in case the original URL goes down. When writing descriptions or notes, pull from the saved local copy rather than re-fetching.
