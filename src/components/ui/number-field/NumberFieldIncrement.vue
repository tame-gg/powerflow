<script setup lang="ts">
import type { NumberFieldIncrementProps } from 'radix-vue'
import { cn } from '@/lib/utils'
import { Plus } from 'lucide-vue-next'
import { NumberFieldIncrement, useForwardProps } from 'radix-vue'
import { computed, type HTMLAttributes } from 'vue'

const props = defineProps<NumberFieldIncrementProps & { class?: HTMLAttributes['class'] }>()

const delegatedProps = computed(() => {
  const { class: _, ...delegated } = props

  return delegated
})

const forwarded = useForwardProps(delegatedProps)
</script>

<template>
  <NumberFieldIncrement data-slot="increment" v-bind="forwarded" :class="cn('absolute top-1/2 -translate-y-1/2 right-0 grid h-full w-6 place-items-center rounded text-fg-3 transition-colors duration-75 hover:text-fg disabled:text-fg-4', props.class)">
    <slot>
      <Plus class="size-3" :stroke-width="2" />
    </slot>
  </NumberFieldIncrement>
</template>
