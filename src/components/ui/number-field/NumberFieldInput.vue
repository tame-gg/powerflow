<script setup lang="ts">
import type { HTMLAttributes } from 'vue'
import { cn } from '@/lib/utils'
import { NumberFieldInput } from 'radix-vue'

const props = defineProps<{
  class?: HTMLAttributes['class']
}>()
</script>

<template>
  <NumberFieldInput
    data-slot="input"
    :class="cn('num flex h-6 w-full rounded border border-line-2 bg-well px-0 py-0 text-center text-[11px] font-medium text-fg shadow-none transition-colors placeholder:text-fg-4 focus:border-line-2 focus:ring-0 disabled:text-fg-4', props.class)"
  />
</template>
