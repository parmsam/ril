---
name: youtube-fetch
description: Fetch a YouTube video's title, channel, publish date, duration, description, chapters, and full transcript as clean markdown using yt-dlp. Use for any youtube.com / youtu.be URL when adding a link, TIL, or ref-source — defuddle/Jina don't return transcripts for YouTube. Trigger phrases include a YouTube URL, "get the transcript", "fetch this video".
---

# youtube-fetch

Use this instead of the defuddle → Jina → WebFetch chain for YouTube URLs. Those return the page shell without a transcript.

## Run

```bash
python3 -I .claude/skills/youtube-fetch/yt_fetch.py "<youtube-url>" ref-sources/YYYY-MM-DD-slug.md
```

Leave out the output path to print to stdout. No `sleep 2` needed (this doesn't hit defuddle).

## Output

Markdown with:
- `# Title`, URL, channel, published date (`YYYY-MM-DD`, use it for the link's `date`), duration
- `## Description`: the uploader's full description
- `## Chapters`, when the video has them
- `## Transcript`: timestamped paragraphs, split by chapter if there are chapters, otherwise about every 60s. The rolling duplicate lines from auto-captions are collapsed. A `_Captions: manual|auto-generated_` line says where the text came from.

Caption preference: human-made English subs, then original-language auto captions (`en-orig`), then translated auto captions.

## Notes

- Auto-captions have no punctuation guarantees and include `[music]`-style tags. Proper nouns may be wrong, so check names against the description/title before putting them in a `description` or `note`.
- If there are no English captions, the transcript section says so. In that case, write the description from the uploader's description only.
- If yt-dlp errors with a bot or sign-in check, update it first (`pip install -U yt-dlp`). If it still fails, try adding `--cookies-from-browser chrome` to the yt-dlp call in the script.
- Content type: a single video is a Link with `type: video`. A channel URL is a Resource with `type: channel`.
