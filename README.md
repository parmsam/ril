# RIL — Resources I Love

A personal curation site — my view of the internet. Links, ongoing resources, and short atomic learnings worth sharing.

**Live site:** https://parmsam.github.io/ril  
**RSS feed:** https://parmsam.github.io/ril/feed.xml

---

## What it is

Three content types, one unified chronological feed:

| Type | What goes here | Example |
|---|---|---|
| **Resource** | An ongoing source you return to repeatedly | Simon Willison's blog, Linear Digressions podcast |
| **Link** | A single piece of content worth reading | A specific article, video, or post |
| **TIL** | A short atomic note on something learned (1–5 sentences) | A Zod trick, a CLI flag, a mental model |

The distinction between resource and link matters: a resource is the *homepage* of something alive (a blog, podcast, channel); a link is one specific piece of content, optionally attributed to a parent resource.

TIL entries are intentionally terse — the point is the thing itself, not an essay about it.

---

## Stack

| Layer | Choice |
|---|---|
| Framework | [Astro 5](https://astro.build) — TypeScript-first, file-based routing, static output |
| Schema | [Zod](https://zod.dev) via Astro content collections — YAML/MDX files are type-checked at build time |
| Styling | [Tailwind CSS v4](https://tailwindcss.com) — CSS-first config, no JS build step |
| Search | [Pagefind](https://pagefind.app) — build-time index, ~5 KB JS, no server needed |
| Deploy | GitHub Actions → GitHub Pages |

---

## Adding content with Claude Code

This repo is designed to work with [Claude Code](https://claude.ai/code). The `.claude/skills/ril-add.md` skill lets you add new entries from inside your editor without touching YAML manually:

```
/ril-add <url>              # prompts for type
/ril-add <url> --resource   # ongoing source (blog, podcast, channel)
/ril-add <url> --link       # one-off content (article, video, post)
/ril-add --til "title"      # short learning, no URL required
```

Claude fetches the page via [defuddle](https://defuddle.md) (falling back to Jina reader, then plain fetch), proposes a title, description, type, and tags, asks for confirmation, writes the file, and offers to commit — all in one step.

---

## Adding content

Use the Claude Code skill from inside this project:

```
/ril-add <url>              # prompts for type
/ril-add <url> --resource   # ongoing source
/ril-add <url> --link       # one-off content
/ril-add --til "title"      # short learning (no URL required)
```

The skill fetches the URL (via defuddle → Jina reader → plain fetch), proposes a title, description, type, and tags, lets you confirm or edit, then writes the file and offers to commit.

### Manual format

**Resource** — `src/content/resources/<slug>.yaml`
```yaml
title: Simon Willison's Weblog
url: https://simonwillison.net
description: Covers AI, Python, and web tooling with strong opinions.
type: blog        # blog | podcast | channel | newsletter | tool | site
tags: [ai, python, web]
status: active    # active | archived
added: 2025-06-19
note: Optional personal take on why it's worth following.
```

**Link** — `src/content/links/<YYYY-MM-DD>-<slug>.yaml`
```yaml
title: Understanding LLM Tokenization
url: https://example.com/article
description: What it covers in 1–2 sentences.
type: article     # article | video | post | paper | thread | tool
tags: [ai, llm]
date: 2025-06-19
note: Optional personal note.
resource: simon-willison-blog  # optional parent resource slug
```

**TIL** — `src/content/til/<YYYY-MM-DD>-<slug>.mdx`
```mdx
---
title: z.coerce.date() handles YAML date strings automatically
date: 2025-06-19
tags: [typescript, zod]
source_url: https://zod.dev      # optional
source_title: Zod docs           # optional
---

The thing itself in 1–5 sentences. No preamble.
```

---

## Development

```bash
npm install
npm run dev        # dev server at localhost:4321 (search inactive)
npm run build      # production build + pagefind index
npm run preview    # preview the built site
```

Search requires a built index — run `npm run build` first, then `npm run preview`.

---

## Deployment

Pushes to `main` trigger the GitHub Actions workflow (`.github/workflows/deploy.yml`), which builds the site, runs Pagefind to generate the search index, and deploys to GitHub Pages automatically.

To deploy manually: `Actions → Deploy to GitHub Pages → Run workflow`.
