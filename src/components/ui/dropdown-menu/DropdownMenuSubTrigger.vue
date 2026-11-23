<script setup lang="ts">
import { cn } from '@/lib/utils'
import { ChevronRight } from 'lucide-vue-next'
import {
  DropdownMenuSubTrigger,
  type DropdownMenuSubTriggerProps,
  useForwardProps,
} from 'radix-vue'
import { computed, type HTMLAttributes } from 'vue'

const props = defineProps<DropdownMenuSubTriggerProps & { class?: HTMLAttributes['class'] }>()

const delegatedProps = computed(() => {
  const { class: _, ...delegated } = props

  return delegated
})

const forwardedProps = useForwardProps(delegatedProps)
</script>

<template>
  <DropdownMenuSubTrigger
    v-bind="forwardedProps"
    :class="cn(
      'flex h-7 cursor-default select-none items-center gap-2 rounded px-2 text-xs text-fg-2 outline-none transition-colors duration-75 focus:bg-hover focus:text-fg data-[state=open]:bg-hover',
      props.class,
    )"
  >
    <slot />
    <ChevronRight class="ml-auto size-3 text-fg-3" :stroke-width="2" />
  </DropdownMenuSubTrigger>
</template>
