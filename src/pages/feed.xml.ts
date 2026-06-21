import { getCollection } from 'astro:content';
import type { APIRoute } from 'astro';

export const GET: APIRoute = async ({ site }) => {
  const base = site?.toString().replace(/\/$/, '') ?? '';

  const resources = await getCollection('resources');
  const links = await getCollection('links');
  const tils = await getCollection('til');

  type FeedEntry = { title: string; url: string; date: Date; description: string };

  const entries: FeedEntry[] = [
    ...resources.map(r => ({
      title: r.data.title,
      url: r.data.url,
      date: r.data.added,
      description: r.data.description,
    })),
    ...links.map(l => ({
      title: l.data.title,
      url: l.data.url,
      date: l.data.added,
      description: l.data.description,
    })),
    ...tils.map(t => ({
      title: `TIL: ${t.data.title}`,
      url: `${base}/til/${t.slug}`,
      date: t.data.date,
      description: t.data.source_title ? `via ${t.data.source_title}` : t.data.title,
    })),
  ].sort((a, b) => b.date.getTime() - a.date.getTime()).slice(0, 30);

  const items = entries.map(e => `
    <item>
      <title><![CDATA[${e.title}]]></title>
      <link>${e.url}</link>
      <guid>${e.url}</guid>
      <pubDate>${e.date.toUTCString()}</pubDate>
      <description><![CDATA[${e.description}]]></description>
    </item>`).join('');

  return new Response(
    `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Resources I Love</title>
    <link>${base}/</link>
    <description>Sam's curated feed of links, resources, and learnings.</description>
    <atom:link href="${base}/feed.xml" rel="self" type="application/rss+xml" />
    ${items}
  </channel>
</rss>`,
    { headers: { 'Content-Type': 'application/xml; charset=utf-8' } }
  );
};
