<script setup lang="ts">
// Port of kestrel/src/lib/components/Meter.tsx. Colour comes from --accent.
const props = defineProps<{
  value: number | null
  peak?: number
  redline?: boolean
  zones?: boolean
  bridge?: boolean
}>()

const clamp = (v: number) => Math.min(100, Math.max(0, v))
</script>

<template>
  <div class="meter" :class="{ bridge: props.bridge, redline: props.redline, zones: props.zones }">
    <div class="track">
      <i v-if="props.value !== null" :style="{ transform: `scaleX(${clamp(props.value) / 100})` }" />
    </div>
    <b v-if="props.peak !== undefined" class="peak" :style="{ left: `${clamp(props.peak)}%` }" />
  </div>
</template>
