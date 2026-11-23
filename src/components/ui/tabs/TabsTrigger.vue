<script setup lang="ts">
import { cn } from '@/lib/utils'
import { TabsTrigger, type TabsTriggerProps, useForwardProps } from 'radix-vue'
import { computed, type HTMLAttributes } from 'vue'

const props = defineProps<TabsTriggerProps & { class?: HTMLAttributes['class'] }>()

const delegatedProps = computed(() => {
  const { class: _, ...delegated } = props

  return delegated
})

const forwardedProps = useForwardProps(delegatedProps)
</script>

<template>
  <TabsTrigger
    v-bind="forwardedProps"
    :class="cn(
      'z-20 inline-flex items-center justify-center whitespace-nowrap transition-colors duration-75 data-[state=active]:!bg-transparent data-[state=active]:!shadow-none disabled:pointer-events-none disabled:text-fg-4',
      props.class,
    )"
  >
    <span class="flex items-center truncate">
      <slot />
    </span>
  </TabsTrigger>
</template>
