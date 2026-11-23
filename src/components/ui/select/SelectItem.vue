<script setup lang="ts">
import { cn } from '@/lib/utils'
import { Check } from 'lucide-vue-next'
import {
  SelectItem,
  SelectItemIndicator,
  type SelectItemProps,
  SelectItemText,
  useForwardProps,
} from 'radix-vue'
import { computed, type HTMLAttributes } from 'vue'

const props = defineProps<SelectItemProps & { class?: HTMLAttributes['class'] }>()

const delegatedProps = computed(() => {
  const { class: _, ...delegated } = props

  return delegated
})

const forwardedProps = useForwardProps(delegatedProps)
</script>

<template>
  <SelectItem
    v-bind="forwardedProps"
    :class="
      cn(
        'relative flex h-7 w-full cursor-default select-none items-center rounded py-0 pl-2 pr-8 text-xs text-fg-2 outline-none transition-colors duration-75 focus:bg-hover focus:text-fg data-[state=checked]:text-fg data-[disabled]:pointer-events-none data-[disabled]:text-fg-4 [&_svg]:text-fg-3',
        props.class,
      )
    "
  >
    <span class="absolute right-2 flex h-3.5 w-3.5 items-center justify-center">
      <SelectItemIndicator>
        <Check class="size-3 text-gold" :stroke-width="2" />
      </SelectItemIndicator>
    </span>

    <SelectItemText>
      <slot />
    </SelectItemText>
  </SelectItem>
</template>
