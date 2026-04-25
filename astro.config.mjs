import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://wrocpp.github.io',
  integrations: [mdx(), sitemap(), tailwind()],
  markdown: {
    shikiConfig: {
      // Dual theme; the site is light-first but dark readers get dimmed github.
      themes: { light: 'github-light', dark: 'github-dark-dimmed' },
      // Preserve author-intended line breaks. Long lines get a horizontal
      // scrollbar, not a soft-wrap that disfigures code shape.
      wrap: false,
    },
  },
});
