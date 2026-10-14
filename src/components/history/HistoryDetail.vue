<script setup lang="ts">
import type { ChargingHistory, ChargingHistoryDetail } from '@/bindings'
import { commands } from '@/bindings'
import CustomChartTooltip from '@/components/chart/CustomChartTooltip.vue'
import { useHistory } from '@/composables/useHistory'
import { shortEnDistanceLocale } from '@/lib/format'
import { save } from '@tauri-apps/plugin-dialog'
import { create } from '@tauri-apps/plugin-fs'
import { error as logerror } from '@tauri-apps/plugin-log'
import { format, formatDuration, intervalToDuration } from 'date-fns'
import { Download, EllipsisVertical, Loader2, Trash2 } from 'lucide-vue-next'

const props = defineProps<ChargingHistory>()
const { selectedItem, history } = useHistory()

const isLoading = ref(true)
const error = ref()
const data = asyncComputed(
  () => commands.getDetailById(props.id)
    .then((r) => {
      if (r.status === 'error') {
        error.value = r.error
        logerror(r.error)
        return {} as ChargingHistoryDetail
      }
      return r.data
    }),
  {} as ChargingHistoryDetail,
  isLoading,
)

async function exportData() {
  const path = await save({
    title: 'Export Data',
    filters: [
      {
        name: 'Json Filter',
        extensions: ['json'],
      },
    ],
  })

  if (path) {
    const file = await create(path)
    await file.write(new TextEncoder().encode(JSON.stringify(data.value)))
    await file.close()
  }
}
</script>

<template>
  <div class="h-full overflow-y-auto">
    <div v-if="isLoading" class="w-full h-full flex items-center justify-center">
      <Loader2 class="animate-spin text-muted-foreground" />
    </div>
    <div v-else-if="error" class="flex h-full w-full items-center justify-center text-destructive">
      {{ error }}
    </div>
    <div v-else class="px-6 pb-8">
      <div class="flex justify-between items-center">
        <div>
          <h1 class="font-serif text-2xl leading-none">
            {{ name || 'Unknown' }}
          </h1>
          <h2 class="mt-1.5 text-xs text-muted-foreground">
            with {{ adapterName }}
          </h2>
        </div>
        <div>
          <DropdownMenu>
            <DropdownMenuTrigger class="rounded-lg p-2 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground">
              <EllipsisVertical class="size-4" />
            </DropdownMenuTrigger>
            <DropdownMenuContent
              :side-offset="10"
              align="end"
            >
              <DropdownMenuItem
                @click="exportData"
              >
                <Download />
                Export Data
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                class="text-destructive focus:bg-destructive/10 focus:text-destructive [&>svg]:text-destructive"
                @click="() => {
                  commands.deleteHistoryById(id)
                  selectedItem = null
                  history.update()
                }"
              >
                <Trash2 />
                Delete
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
      <div class="mt-4 grid gap-4 grid-cols-3">
        <div class="space-y-2">
          <div class="caption">
            Duration
          </div>
          <div class="readout text-[28px] leading-8">
            {{ formatDuration(
              intervalToDuration({
                start: timestamp * 1000,
                end: timestamp * 1000 + chargingTime * 1000,
              }),
              { format: ['hours', 'minutes'], locale: shortEnDistanceLocale },
            )
            }}
          </div>
          <div class="text-[11px] text-muted-foreground">
            {{ format(timestamp * 1000, 'yyyy-MM-dd HH:mm') }}
          </div>
        </div>
        <div class="space-y-2">
          <div class="caption">
            Avg Power
          </div>
          <div class="readout text-[28px] leading-8">
            {{ data.avg.adapterPower.toFixed(1) }}W
          </div>
          <div class="text-[11px] text-muted-foreground">
            Peak: {{ data.peak.adapterPower.toFixed(1) }}W
          </div>
        </div>
        <div class="space-y-2">
          <div class="caption">
            Charging rate
          </div>
          <div class="readout text-[28px] leading-8">
            {{ ((endLevel - fromLevel) / chargingTime * 60).toFixed(2) }}%/min
          </div>
          <div class="text-[11px] text-muted-foreground">
            Avg Temp: {{ data.avg.temperature.toFixed(1) }}°C
          </div>
        </div>
      </div>

      <h2 class="caption mt-8">
        Charging Curve
      </h2>
      <LineChart
        class="mt-8 max-h-[220px]"
        index="lastUpdate"
        :data="data.curve.map(d => ({ ...d, lastUpdate: new Date(d.lastUpdate * 1000).toLocaleTimeString() }))"
        :categories="['systemIn', 'batteryPower', 'systemLoad', 'absoluteBatteryLevel']"
        :custom-tooltip="CustomChartTooltip"
        :show-legend="false"
      />

      <h2 class="caption mt-8">
        Additional Detail
      </h2>
      <div class="mt-3 grid gap-4 text-xs">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <div class="text-muted-foreground">
              Temperature Peak
            </div>
            <div class="font-mono">
              {{ data.peak.temperature.toFixed(1) }}°C
            </div>
          </div>
          <div>
            <div class="text-muted-foreground">
              Adapter Power Peak
            </div>
            <div class="font-mono">
              {{ data.peak.adapterPower.toFixed(1) }}W
            </div>
          </div>
          <div>
            <div class="text-muted-foreground">
              Adapter Watts
            </div>
            <div class="font-mono">
              {{ data.peak.adapterWatts }}W({{ data.peak.adapterVoltage }}V, {{ data.peak.adapterAmperage }}A)
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
