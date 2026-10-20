import { cva, type VariantProps } from 'class-variance-authority'

export { default as Badge } from './Badge.vue'

// Kestrel's .chip tones (src/assets/theme.css).
export const badgeVariants = cva(
  'chip',
  {
    variants: {
      variant: {
        default: 'accent',
        secondary: '',
        destructive: 'danger',
        outline: 'bg-transparent',
        warn: 'warn',
        ok: 'ok',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  },
)

export type BadgeVariants = VariantProps<typeof badgeVariants>
