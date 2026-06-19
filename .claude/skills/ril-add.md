# ril-add

Add a new entry to the RIL tracker. Takes a URL and creates the appropriate content file.

## Usage

```
/ril-add <url>
/ril-add <url> --resource
/ril-add <url> --link
/ril-add --til "Title of what I learned"
```

## Steps

### 1. Determine content type

If no flag provided, ask the user:
- **Resource** (`--resource`): An ongoing source you return to repeatedly — a blog homepage, podcast feed, YouTube channel, newsletter, or tool you use regularly. Links to the *home* of something, not a specific piece of content.
- **Link** (`--link`): A single piece of content you want to share — a specific article, video, post, paper, or thread. One-off.
- **TIL** (`--til`): A short atomic note on something you learned. Can have an optional source URL. Body text is written by you — keep it 1-5 sentences, punchy. Not an essay.

### 2. Fetch metadata (skip for TIL with no URL)

Try in order, stop at first success:
1. Use the `defuddle` skill to fetch the URL as clean markdown
2. Try `https://r.jina.ai/<url>` via WebFetch
3. Use WebFetch directly on the URL

### 3. Extract from fetched content

Generate:
- `title`: The page or article title — clean, no site suffix
- `description`: 1–2 sentences. What it is, not why it's good.
- `type`:
  - For **resources**: `blog` | `podcast` | `channel` | `newsletter` | `tool` | `site`
  - For **links**: `article` | `video` | `post` | `paper` | `thread` | `tool`
- `tags`: 2–5 lowercase kebab-case tags (e.g. `ai`, `web-dev`, `data-science`)

### 4. Show preview and ask for confirmation

```
Title:       [proposed title]
Type:        [proposed type]
Description: [proposed description]
Tags:        [tag1, tag2, tag3]
Note:        (leave blank, or add your personal take on why it's worth it)
```

Ask if anything needs editing and if they want to add a personal `note`.

### 5. Generate filename and write file

**Today's date**: use the current date in YYYY-MM-DD format.

**Resource** → `src/content/resources/<slug>.yaml`
```yaml
title: <title>
url: <url>
description: <description>
type: <type>
tags: [tag1, tag2]
status: active
added: <YYYY-MM-DD>
note: <note>  # omit line if empty
```

**Link** → `src/content/links/<YYYY-MM-DD>-<slug>.yaml`
```yaml
title: <title>
url: <url>
description: <description>
type: <type>
tags: [tag1, tag2]
date: <YYYY-MM-DD>
note: <note>  # omit line if empty
resource: <parent-resource-slug>  # omit if not applicable
```

**TIL** → `src/content/til/<YYYY-MM-DD>-<slug>.mdx`
```mdx
---
title: <title>
date: <YYYY-MM-DD>
tags: [tag1, tag2]
source_url: <url>  # omit if none
source_title: <source title>  # omit if none
---

<1–5 sentence body — the thing itself, no preamble>
```

**Slug rules**: lowercase, hyphens only, no special chars, max ~5 words.

### 6. Offer to commit

Ask: "Want me to commit this?" If yes:
```
git add src/content/<type>/<filename>
git commit -m "add: <title>"
```
