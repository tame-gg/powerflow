<script lang="ts" setup>
import type { HTMLAttributes } from 'vue'
import { cn } from '@/lib/utils'
import { MotionDirective as motion } from '@vueuse/motion'

interface ShimmerProps {
  as?: keyof HTMLElementTagNameMap
  class?: HTMLAttributes['class']
  duration?: number
  spread?: number
  delay?: number
  repeatDelay?: number
}

defineOptions({
  directives: {
    motion: motion(),
  },
})

const props = defineProps<ShimmerProps>()
</script>

<template>
  <div
    v-motion
    :initial="{ backgroundPosition: '100% center' }"
    :enter="{
      backgroundPosition: '0% center',
      transition: {
        repeat: Infinity,
        duration: 1200,
        delay: props.delay ?? 200,
        repeatDelay: props.repeatDelay ?? 0,
        ease: 'linear',
      },
    }"
    :class="cn(
      'relative inline-block bg-[length:250%_100%,auto]',
      '[--base-color:hsl(var(--input))] [--base-gradient-color:hsl(var(--primary))]',
      '[--bg:linear-gradient(90deg,#0000_calc(50%-var(--spread)),var(--base-gradient-color),#0000_calc(50%+var(--spread)))] [background-repeat:no-repeat,padding-box]',
      props.class,
    )"
    :style="{
      '--spread': `${props.spread ?? 20}px`,
      'background-image': 'var(--bg), linear-gradient(var(--base-color), var(--base-color))',
    }"
  >
    <slot />
  </div>
</template>
