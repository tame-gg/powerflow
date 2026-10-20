<script setup lang="ts">
import type { HTMLAttributes } from 'vue'
import { cn } from '@/lib/utils'
import { SelectLabel, type SelectLabelProps } from 'radix-vue'

const props = defineProps<SelectLabelProps & { class?: HTMLAttributes['class'] }>()
</script>

<template>
  <SelectLabel :class="cn('caption flex h-6 items-center px-2', props.class)">
    <slot />
  </SelectLabel>
</template>
