<script setup lang="ts">
import { formatChargingDuration } from '@/lib/format'
import { BatteryCharging, BatteryFull, BatteryLow, BatteryMedium } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'

const power = usePower()
const { t } = useI18n()
</script>

<template>
  <div class="flex flex-col gap-2" style="--accent: var(--charge)">
    <div class="flex h-5 items-center justify-between gap-3">
      <div v-if="!power.isLoading" class="flex items-center gap-2">
        <BatteryCharging
          v-if="power.isCharging"
          :size="14"
          :stroke-width="2"
          class="text-accent"
        />
        <BatteryFull
          v-else-if="power.batteryLevel > 66"
          :size="14"
          :stroke-width="2"
          class="text-fg-3"
        />
        <BatteryMedium
          v-else-if="power.batteryLevel > 33"
          :size="14"
          :stroke-width="2"
          class="text-fg-3"
        />
        <BatteryLow
          v-else
          :size="14"
          :stroke-width="2"
          :class="power.batteryLevel < 10 ? 'text-danger' : 'text-fg-3'"
        />
        <span class="num text-[13px] font-medium">{{ power.batteryLevel.toFixed(2) }}%</span>
      </div>
      <span v-else class="scan h-4 w-20" />

      <div
        v-if="!power.isLoading"
        class="truncate text-[11px]"
        :class="power.isCharging ? 'text-fg-2' : 'text-fg-3'"
      >
        <span v-if="power.isCharging && power.batteryLevel === 100" class="text-ok">{{ $t('status.fully_charged') }}</span>
        <template v-else>
          <b class="font-medium text-fg">{{ formatChargingDuration(power.timeRemain.secs, t) }}</b>
          {{ ' ' }}
          <span>{{ power.isCharging ? $t('status.to_full') : $t('status.to_empty') }}</span>
        </template>
      </div>
      <span v-else class="scan h-4 w-28" />
    </div>
    <PowerStatusBar v-if="!power.isLoading" />
    <span v-else class="scan h-2 w-full" />
  </div>
</template>
