<script setup lang="ts">
import type { ChargingHistory } from '@/bindings'
import { formatChargingDuration } from '@/lib/format'
import { useTimeAgoOptions } from '@/lib/i18n'
import { MobileIcon } from '@radix-icons/vue'
import { ChevronRight, LaptopIcon } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'

const { timestamp, chargingTime } = defineProps<ChargingHistory>()
const { t } = useI18n()
const timeAgoOptions = useTimeAgoOptions()
const formatedUpdatetime = useTimeAgo(timestamp * 1000 + chargingTime * 1000, timeAgoOptions)
</script>

<template>
  <div class="flex items-center justify-between rounded-lg border border-transparent px-3 py-2 transition-colors hover:bg-muted/50">
    <div class="flex items-center">
      <div class="py-2 h-min">
        <MobileIcon v-if="isRemote" class="size-4 text-muted-foreground" />
        <LaptopIcon v-else class="size-4 text-muted-foreground" />
      </div>
      <div class="flex flex-col ml-4">
        <span class="flex gap-2 relative font-mono items-baseline">
          <span class="flex items-baseline text-[13px] font-medium">
            {{ fromLevel }}
            <span class="text-xs ml-[2px]">%</span>
            <ChevronRight class="mx-1 size-3.5 self-center text-muted-foreground" />
            {{ endLevel }}
            <span class="text-xs ml-[2px]">%</span>
          </span>
          <div class="text-muted-foreground font-mono text-xs truncate">
            {{ formatChargingDuration(chargingTime, t) }}
          </div>
        </span>

        <span class="text-muted-foreground font-mono text-xs truncate">{{ formatedUpdatetime }}</span>
      </div>
    </div>

    <div class="w-24" />

    <div class="flex items-center gap-4">
      <div class="p-2">
        <ChevronRight class="size-4 text-muted-foreground" />
      </div>
    </div>
  </div>
</template>
