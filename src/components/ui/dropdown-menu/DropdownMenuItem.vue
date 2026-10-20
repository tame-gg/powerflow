<script setup lang="ts">
import { cn } from '@/lib/utils'
import { DropdownMenuItem, type DropdownMenuItemProps, useForwardProps } from 'radix-vue'
import { computed, type HTMLAttributes } from 'vue'

const props = defineProps<DropdownMenuItemProps & { class?: HTMLAttributes['class'], inset?: boolean }>()

const delegatedProps = computed(() => {
  const { class: _, ...delegated } = props

  return delegated
})

const forwardedProps = useForwardProps(delegatedProps)
</script>

<template>
  <DropdownMenuItem
    v-bind="forwardedProps"
    :class="cn(
      'relative flex h-7 cursor-default select-none items-center gap-2 rounded px-2 text-xs font-medium text-fg-2 outline-none transition-colors duration-75 focus:bg-hover focus:text-fg data-[disabled]:pointer-events-none data-[disabled]:text-fg-4 [&>svg]:size-3.5 [&>svg]:shrink-0 [&>svg]:text-fg-3',
      inset && 'pl-8',
      props.class,
    )"
  >
    <slot />
  </DropdownMenuItem>
</template>
