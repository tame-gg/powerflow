<script setup lang="ts">
import { cn } from '@/lib/utils'
import { ChevronsUpDown } from 'lucide-vue-next'
import { SelectIcon, SelectTrigger, type SelectTriggerProps, useForwardProps } from 'radix-vue'
import { computed, type HTMLAttributes } from 'vue'

const props = defineProps<SelectTriggerProps & { class?: HTMLAttributes['class'] }>()

const delegatedProps = computed(() => {
  const { class: _, ...delegated } = props

  return delegated
})

const forwardedProps = useForwardProps(delegatedProps)
</script>

<template>
  <SelectTrigger
    v-bind="forwardedProps"
    :class="cn(
      'btn w-full justify-between gap-2 text-start data-[state=open]:bg-raise-3 data-[placeholder]:text-fg-3 disabled:text-fg-4 [&>span]:truncate [&>span]:flex [&>span]:items-center',
      props.class,
    )"
  >
    <slot />
    <SelectIcon as-child>
      <ChevronsUpDown class="size-3 shrink-0 text-fg-3" :stroke-width="2" />
    </SelectIcon>
  </SelectTrigger>
</template>
