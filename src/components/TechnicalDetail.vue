<script setup lang="ts">
import { BatteryMedium, RefreshCw, Thermometer, Zap } from 'lucide-vue-next'

const power = usePower()
const health = computed(() => power.value.maxCapacity / power.value.designCapacity! * 100)
</script>

<template>
  <!-- Kestrel .tiles: caption + icon, mono value, sub line, optional meter -->
  <section class="tiles border-t-0">
    <div class="tile" style="--accent: var(--temp)">
      <div class="k caption">
        <Thermometer :size="12" :stroke-width="2" />{{ $t('temperature') }}
      </div>
      <div v-if="!power.isLoading" class="v num">
        {{ power.temperature.toFixed(1) }}°C
      </div>
      <span v-else class="scan h-5 w-16" />
      <div class="s">
        {{ $t('temperature_desc') }}
      </div>
      <Meter :value="power.isLoading ? null : power.temperature / 50 * 100" zones />
    </div>
    <div class="tile" style="--accent: var(--charge)">
      <div class="k caption">
        <BatteryMedium :size="12" :stroke-width="2" />{{ $t('battery_health') }}
      </div>
      <div v-if="!power.isLoading" class="v num">
        <!-- TODO: typing -->
        {{ health.toFixed(1) }}%
      </div>
      <span v-else class="scan h-5 w-16" />
      <div class="s">
        {{ $t('battery_health_desc') }}
      </div>
      <Meter :value="power.isLoading ? null : health" />
    </div>
    <div class="tile" style="--accent: var(--soc)">
      <div class="k caption">
        <RefreshCw :size="12" :stroke-width="2" />{{ $t('cycle_count') }}
      </div>
      <div v-if="!power.isLoading" class="v num">
        {{ power.cycleCount }} <small class="font-sans text-xs font-medium text-fg-3">{{ $t('times') }}</small>
      </div>
      <span v-else class="scan h-5 w-16" />
      <div class="s">
        {{ $t('cycle_count_desc') }}
      </div>
    </div>
    <div class="tile" style="--accent: var(--adapter)">
      <div class="k caption">
        <Zap :size="12" :stroke-width="2" />Energy
      </div>
      <div v-if="!power.isLoading" class="v num">
        {{ power.currentCapacity }} <small class="font-sans text-xs font-medium text-fg-3">mAh</small>
      </div>
      <span v-else class="scan h-5 w-16" />
      <div class="s flex gap-1">
        Max Capacity: <span v-if="!power.isLoading" class="num">{{ power.maxCapacity }} mAh</span>
      </div>
      <Meter :value="power.isLoading ? null : power.currentCapacity / power.maxCapacity * 100" />
    </div>
  </section>
</template>
