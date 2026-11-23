<script setup lang="ts">
import { cn } from '@/lib/utils'
import {
  SwitchRoot,
  type SwitchRootEmits,
  type SwitchRootProps,
  SwitchThumb,
  useForwardPropsEmits,
} from 'radix-vue'
import { computed, type HTMLAttributes } from 'vue'

const props = defineProps<SwitchRootProps & { class?: HTMLAttributes['class'] }>()

const emits = defineEmits<SwitchRootEmits>()

const delegatedProps = computed(() => {
  const { class: _, ...delegated } = props

  return delegated
})

const forwarded = useForwardPropsEmits(delegatedProps, emits)
</script>

<template>
  <SwitchRoot
    v-bind="forwarded"
    :class="cn(
      'peer inline-flex h-[18px] w-8 shrink-0 items-center rounded-full border border-line-2 p-px transition-colors duration-75 disabled:opacity-50 data-[state=checked]:border-transparent data-[state=checked]:bg-ok/90 data-[state=unchecked]:bg-well',
      props.class,
    )"
  >
    <SwitchThumb
      :class="cn('pointer-events-none block size-3.5 rounded-full shadow-none ring-0 transition-transform duration-200 ease-kestrel data-[state=checked]:translate-x-3.5 data-[state=checked]:bg-background data-[state=unchecked]:translate-x-0 data-[state=unchecked]:bg-fg-3')"
    >
      <slot name="thumb" />
    </SwitchThumb>
  </SwitchRoot>
</template>
