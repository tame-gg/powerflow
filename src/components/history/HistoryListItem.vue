<script setup lang="ts">
import type { ChargingHistory } from '@/bindings'
import { formatChargingDuration } from '@/lib/format'
import { useTimeAgoOptions } from '@/lib/i18n'
import { ArrowRight, Laptop, Smartphone } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'

const { timestamp, chargingTime, selected } = defineProps<ChargingHistory & { selected?: boolean }>()
const { t } = useI18n()
const timeAgoOptions = useTimeAgoOptions()
const formatedUpdatetime = useTimeAgo(timestamp * 1000 + chargingTime * 1000, timeAgoOptions)
</script>

<template>
  <!-- Kestrel .chan row: icon, label + sub, readout; selected gets raise + accent rail -->
  <button
    class="chan shrink-0 border-b border-line py-2"
    :class="{ on: selected }"
    :aria-selected="selected"
    style="--accent: var(--charge)"
  >
    <Smartphone v-if="isRemote" :size="14" :stroke-width="2" />
    <Laptop v-else :size="14" :stroke-width="2" />
    <span class="flex min-w-0 flex-col gap-0.5">
      <span class="num flex items-center gap-1 text-xs font-medium text-fg">
        {{ fromLevel }}%
        <ArrowRight :size="11" :stroke-width="2" class="text-fg-3" />
        {{ endLevel }}%
      </span>
      <span class="truncate text-[11px] text-fg-3">{{ formatedUpdatetime }}</span>
    </span>
    <span class="num text-[11px] text-fg-2">{{ formatChargingDuration(chargingTime, t) }}</span>
  </button>
</template>
