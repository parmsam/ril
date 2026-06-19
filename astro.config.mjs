import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import mdx from '@astrojs/mdx';

// For GitHub Pages:
// - User site (username.github.io): set site only, no base
// - Project site (username.github.io/ril): set both site and base: '/ril'
export default defineConfig({
  site: 'https://parmsam.github.io',
  base: '/ril',
  integrations: [mdx()],
  vite: {
    plugins: [tailwindcss()],
  },
});
