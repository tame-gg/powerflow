<script setup lang="ts">
import { cn } from '@/lib/utils'
import { Check } from 'lucide-vue-next'
import {
  DropdownMenuCheckboxItem,
  type DropdownMenuCheckboxItemEmits,
  type DropdownMenuCheckboxItemProps,
  DropdownMenuItemIndicator,
  useForwardPropsEmits,
} from 'radix-vue'
import { computed, type HTMLAttributes } from 'vue'

const props = defineProps<DropdownMenuCheckboxItemProps & { class?: HTMLAttributes['class'] }>()
const emits = defineEmits<DropdownMenuCheckboxItemEmits>()

const delegatedProps = computed(() => {
  const { class: _, ...delegated } = props

  return delegated
})

const forwarded = useForwardPropsEmits(delegatedProps, emits)
</script>

<template>
  <DropdownMenuCheckboxItem
    v-bind="forwarded"
    :class=" cn(
      'relative flex h-7 cursor-default select-none items-center rounded py-0 pl-8 pr-2 text-xs text-fg-2 outline-none transition-colors duration-75 focus:bg-hover focus:text-fg data-[disabled]:pointer-events-none data-[disabled]:text-fg-4',
      props.class,
    )"
  >
    <span class="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
      <DropdownMenuItemIndicator>
        <Check class="size-3" :stroke-width="2" />
      </DropdownMenuItemIndicator>
    </span>
    <slot />
  </DropdownMenuCheckboxItem>
</template>
