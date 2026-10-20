<script setup lang="ts">
import type { NumberFieldDecrementProps } from 'radix-vue'
import { cn } from '@/lib/utils'
import { Minus } from 'lucide-vue-next'
import { NumberFieldDecrement, useForwardProps } from 'radix-vue'
import { computed, type HTMLAttributes } from 'vue'

const props = defineProps<NumberFieldDecrementProps & { class?: HTMLAttributes['class'] }>()

const delegatedProps = computed(() => {
  const { class: _, ...delegated } = props

  return delegated
})

const forwarded = useForwardProps(delegatedProps)
</script>

<template>
  <NumberFieldDecrement data-slot="decrement" v-bind="forwarded" :class="cn('absolute top-1/2 -translate-y-1/2 left-0 grid h-full w-6 place-items-center rounded text-fg-3 transition-colors duration-75 hover:text-fg disabled:text-fg-4', props.class)">
    <slot>
      <Minus class="size-3" :stroke-width="2" />
    </slot>
  </NumberFieldDecrement>
</template>
