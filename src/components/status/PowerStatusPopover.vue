<script setup lang="ts">
import { commands } from '@/bindings'

const target = useTemplateRef<HTMLElement>('target')

provide('isPopover', true)
</script>

<template>
  <!-- Kestrel .mini: solid canvas, line-2 hairline, 12px window radius -->
  <div
    ref="target"
    class="h-screen w-full overflow-hidden rounded-window border border-line-2 bg-background"
    @click="commands.openApp()"
  >
    <slot is-popover />
  </div>
</template>
