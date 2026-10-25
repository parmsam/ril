#!/usr/bin/env python3
"""Fetch a YouTube video's metadata + transcript as markdown via yt-dlp.

Usage: yt_fetch.py <youtube-url> [out.md]
Prints markdown to stdout, or writes to out.md if given.
"""
import glob, html, json, re, subprocess, sys, tempfile
from pathlib import Path

TS = re.compile(r"(\d+):(\d\d):(\d\d)\.(\d+) -->")
TAG = re.compile(r"<[^>]+>")


def secs(m):
    return int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3])


def fmt(s):
    s = int(s)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60}:{s % 60:02d}"


def parse_vtt(path):
    """Return [(start_sec, line)], collapsing the rolling duplicates in auto-captions."""
    out, recent, start = [], [], 0
    for block in Path(path).read_text().split("\n\n"):
        lines = block.strip().splitlines()
        m = next((TS.search(l) for l in lines if TS.search(l)), None)
        if not m:
            continue
        start = secs(m)
        for raw in lines[[i for i, l in enumerate(lines) if TS.search(l)][0] + 1:]:
            text = html.unescape(TAG.sub("", raw)).replace("\xa0", " ").strip()
            if not text or text in recent:
                continue
            out.append((start, text))
            recent = (recent + [text])[-3:]
    return out


def paragraphs(cues, chapters, every=60):
    """Group caption lines into timestamped paragraphs (by chapter if present, else ~every 60s)."""
    bounds = [(c["start_time"], c["title"]) for c in chapters or []]
    paras, cur, cur_start, chap_i = [], [], None, 0
    for start, text in cues:
        new_chap = chap_i < len(bounds) and start >= bounds[chap_i][0]
        if cur and (new_chap or (not bounds and start - cur_start >= every)):
            paras.append((cur_start, None, " ".join(cur)))
            cur = []
        if new_chap:
            paras.append((bounds[chap_i][0], bounds[chap_i][1], None))
            chap_i += 1
        if not cur:
            cur_start = start
        cur.append(text)
    if cur:
        paras.append((cur_start, None, " ".join(cur)))
    return paras


def main():
    url = sys.argv[1]
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(
            ["yt-dlp", "--skip-download", "--write-info-json", "--write-subs", "--write-auto-subs",
             "--sub-langs", "en,en-orig,en-US,en-GB", "--sub-format", "vtt",
             "-o", f"{d}/v.%(ext)s", url],
            check=True, capture_output=True, text=True,
        )
        info = json.loads(Path(f"{d}/v.info.json").read_text())
        manual = set((info.get("subtitles") or {}).keys())
        vtts = sorted(glob.glob(f"{d}/v.*.vtt"))
        # Prefer human-made English subs, then original-language auto, then translated auto
        rank = lambda p: (Path(p).suffixes[0][1:] not in manual, "orig" not in p)
        vtt = min(vtts, key=rank) if vtts else None
        cues = parse_vtt(vtt) if vtt else []
        source = ("manual" if Path(vtt).suffixes[0][1:] in manual else "auto-generated") if vtt else None

    d = info.get("upload_date") or ""
    md = [
        f"# {info['title']}",
        "",
        f"- **URL:** {info.get('webpage_url', url)}",
        f"- **Channel:** {info.get('channel') or info.get('uploader')} ({info.get('channel_url', '')})",
        f"- **Published:** {d[:4]}-{d[4:6]}-{d[6:]}" if d else "- **Published:** unknown",
        f"- **Duration:** {fmt(info.get('duration') or 0)}",
        "",
        "## Description",
        "",
        info.get("description") or "(none)",
        "",
    ]
    if info.get("chapters"):
        md += ["## Chapters", ""] + [f"- [{fmt(c['start_time'])}] {c['title']}" for c in info["chapters"]] + [""]
    md += ["## Transcript", ""]
    if cues:
        md += [f"_Captions: {source}_", ""]
        for start, chap, text in paragraphs(cues, info.get("chapters")):
            md += [f"### {chap}" if chap else f"[{fmt(start)}] {text}", ""]
    else:
        md += ["(no English captions available)", ""]

    text = "\n".join(md)
    if len(sys.argv) > 2:
        Path(sys.argv[2]).write_text(text)
        print(f"wrote {sys.argv[2]} ({len(cues)} caption lines, {source or 'no captions'})")
    else:
        print(text)


if __name__ == "__main__":
    main()
