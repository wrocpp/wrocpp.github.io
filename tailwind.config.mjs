/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        // Brand canon (unchanged from 2021 Wro.cpp brand book)
        brand: {
          orange: '#EA541E',
          orangeHot: '#D6481A',
          blue: '#3EB5E9',
          blueDeep: '#2E8FB8',
          ink: '#414142',
        },
        // Extended design palette
        paper: {
          DEFAULT: '#FCFAF5', // warm off-white
          2: '#F3EFE6',        // card surface
          3: '#E8E1D0',        // divider tint
        },
        ink: {
          DEFAULT: '#1B1B1D',  // body text
          muted: '#55555A',    // secondary
          faint: '#8A8A90',    // tertiary
        },
        rule: '#D7D2C4',
        code: {
          bg: '#1B1B1D',
          text: '#F3EFE6',
          muted: '#A8A39B',
        },
      },
      fontFamily: {
        display: ['Quicksand', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        serif: ['"Source Serif 4"', 'Georgia', 'serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'Menlo', 'monospace'],
      },
      maxWidth: {
        prose: '68ch',
        wide: '72rem',
      },
      spacing: {
        rail: '14rem',
      },
      letterSpacing: {
        tightdisplay: '-0.02em',
      },
    },
  },
  plugins: [],
};
