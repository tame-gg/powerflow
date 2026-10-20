import { cva, type VariantProps } from 'class-variance-authority'

export { default as Button } from './Button.vue'

// Kestrel's .btn family (src/assets/theme.css): 24px, hairline border,
// top-lit surface, ghost and danger tones.
export const buttonVariants = cva(
  'btn justify-center disabled:pointer-events-none [&_svg]:pointer-events-none [&_svg]:size-3 [&_svg]:shrink-0',
  {
    variants: {
      variant: {
        default: '',
        destructive: 'danger',
        outline: '',
        secondary: '',
        ghost: 'ghost',
        link: 'h-auto border-0 bg-none px-0 text-gold hover:bg-transparent hover:underline',
      },
      size: {
        default: '',
        xs: 'h-5 px-1.5 text-[11px]',
        sm: '',
        lg: 'h-7 px-3',
        icon: 'h-7 w-8 px-0',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  },
)

export type ButtonVariants = VariantProps<typeof buttonVariants>
