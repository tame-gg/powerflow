<script setup lang="ts">
import { cn } from '@/lib/utils'
import {
  ProgressIndicator,
  ProgressRoot,
  type ProgressRootProps,
} from 'radix-vue'
import { computed, type HTMLAttributes } from 'vue'

const props = withDefaults(
  defineProps<ProgressRootProps & { class?: HTMLAttributes['class'] }>(),
  {
    modelValue: 0,
  },
)

const delegatedProps = computed(() => {
  const { class: _, ...delegated } = props

  return delegated
})
</script>

<template>
  <!-- Kestrel meter: segmented track, accent fill -->
  <ProgressRoot
    v-bind="delegatedProps"
    :class="cn('meter w-full', props.class)"
  >
    <div class="track">
      <ProgressIndicator
        as="i"
        :style="{ transform: `scaleX(${Math.min(100, Math.max(0, props.modelValue ?? 0)) / 100})` }"
      />
    </div>
  </ProgressRoot>
</template>
