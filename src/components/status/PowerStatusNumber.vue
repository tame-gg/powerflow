<script setup lang="ts">
import NumberFlow from '@number-flow/vue'

const power = usePower()
const { preference, isLoading } = usePreferenceAsync()
const isPopover = inject('isPopover', false)
</script>

<template>
  <!-- Kestrel readout: serif figure, system-font unit in text-3 -->
  <div
    class="readout"
    :class="isPopover
      ? 'text-[32px] leading-9 tracking-[-0.02em] [&_small]:text-xs'
      : 'text-[44px] leading-[48px] tracking-[-0.02em] [&_small]:text-base'"
  >
    <span v-if="power.isLoading || isLoading" class="scan inline-block h-9 w-36 align-middle" />
    <template v-else>
      <NumberFlow
        v-if="preference.animationsEnabled"
        :format="{ maximumFractionDigits: 1, minimumFractionDigits: 1 }"
        :value="power.isCharging ? power.systemIn : power.systemLoad"
      />
      <span v-else>{{ (power.isCharging ? power.systemIn : power.systemLoad).toFixed(1) }}</span>
      <small>W</small>
    </template>
  </div>
</template>
