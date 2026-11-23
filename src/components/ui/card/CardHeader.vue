<script setup lang="ts">
import type { HTMLAttributes } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps<{
  class?: HTMLAttributes['class']
}>()
</script>

<template>
  <div :class="cn('flex min-h-8 flex-col justify-center gap-y-1 px-4 pt-3', props.class)">
    <slot />
  </div>
</template>
