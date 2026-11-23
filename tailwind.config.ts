import tailwindcssForm from '@tailwindcss/forms'
import tailwindcssAnimate from 'tailwindcss-animate'

// Every colour is a Kestrel token from src/assets/theme.css. color-mix keeps
// Tailwind's opacity modifiers (bg-accent/10) working on hex and rgba values.
function token(name: string) {
  return `color-mix(in srgb, var(--${name}) calc(<alpha-value> * 100%), transparent)`
}

/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    './src/**/*.{ts,tsx,vue}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font)'],
        mono: ['var(--mono)'],
        serif: ['var(--serif)'],
      },
      colors: {
        background: token('bg'),
        foreground: token('text'),
        fg: {
          DEFAULT: token('text'),
          2: token('text-2'),
          3: token('text-3'),
          4: token('text-4'),
        },
        rail: token('rail'),
        well: token('well'),
        hover: token('hover'),
        raise: {
          DEFAULT: token('raise'),
          2: token('raise-2'),
          3: token('raise-3'),
        },
        line: {
          DEFAULT: token('line'),
          2: token('line-2'),
        },
        tick: token('tick'),
        grid: token('grid'),
        accent: token('accent'),
        gold: token('gold'),
        warn: token('warn'),
        danger: token('danger'),
        ok: token('ok'),
        cpu: token('cpu'),
        mem: token('mem'),
        disk: token('disk'),
        net: token('net'),
        gpu: token('gpu'),
        battery: token('battery'),
        sensors: token('sensors'),
        ports: token('ports'),
        projects: token('projects'),
        system: token('system'),
        screen: token('screen'),
        soc: token('soc'),
        adapter: token('adapter'),
        charge: token('charge'),
        loss: token('loss'),
        temp: token('temp'),
        other: token('other'),
      },
      backgroundImage: {
        surface: 'var(--surface)',
      },
      boxShadow: {
        pop: 'var(--pop-shadow)',
        flag: 'var(--flag-shadow)',
      },
      borderRadius: {
        DEFAULT: 'var(--r)',
        lg: 'var(--r)',
        pop: '10px',
        window: '12px',
      },
      transitionTimingFunction: {
        kestrel: 'var(--ease)',
      },
      keyframes: {
        'collapsible-down': {
          from: { height: 0 },
          to: { height: 'var(--radix-collapsible-content-height)' },
        },
        'collapsible-up': {
          from: { height: 'var(--radix-collapsible-content-height)' },
          to: { height: 0 },
        },
      },
      animation: {
        'collapsible-down': 'collapsible-down 0.2s ease-in-out',
        'collapsible-up': 'collapsible-up 0.2s ease-in-out',
        'beat': 'beat 900ms ease-out forwards',
        'fade': 'fade 80ms linear',
      },
    },
  },
  plugins: [tailwindcssForm, tailwindcssAnimate],
}
