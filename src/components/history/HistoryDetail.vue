<script setup lang="ts">
import type { ChargingHistory, ChargingHistoryDetail } from '@/bindings'
import type { ChartSeries } from '@/components/kestrel/Chart.vue'
import { commands } from '@/bindings'
import { useHistory } from '@/composables/useHistory'
import { shortEnDistanceLocale } from '@/lib/format'
import { save } from '@tauri-apps/plugin-dialog'
import { create } from '@tauri-apps/plugin-fs'
import { error as logerror } from '@tauri-apps/plugin-log'
import { format, formatDuration, intervalToDuration } from 'date-fns'
import { Download, Ellipsis, Gauge, Thermometer, Timer, Trash2 } from 'lucide-vue-next'

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

const inactive = ref(new Set<string>())
function toggle(name: string) {
  const next = new Set(inactive.value)
  next.has(name) ? next.delete(name) : next.add(name)
  inactive.value = next
}

// Kestrel accent per reading (src/assets/theme.css)
const curveSeries = computed<ChartSeries[]>(() => {
  const curve = data.value.curve ?? []
  return [
    { name: 'System In', key: 'systemIn', color: 'var(--adapter)', unit: 'W' },
    { name: 'Battery Power', key: 'batteryPower', color: 'var(--charge)', unit: 'W' },
    { name: 'System Load', key: 'systemLoad', color: 'var(--system)', unit: 'W' },
    { name: 'Battery Level', key: 'absoluteBatteryLevel', color: 'var(--screen)', unit: '%' },
  ].map(({ key, ...s }) => ({
    ...s,
    values: curve.map(d => d[key as keyof typeof d] as number),
    inactive: inactive.value.has(s.name),
  }))
})
const curveLabels = computed(() => (data.value.curve ?? []).map(d => format(d.lastUpdate * 1000, 'HH:mm')))
</script>

<template>
  <div class="h-full overflow-y-auto">
    <div v-if="isLoading" class="grid h-full w-full place-items-center">
      <span class="scan h-px w-40" />
    </div>
    <div v-else-if="error" class="empty-state">
      <span class="wordmark nosig">Error</span>
      <p class="text-danger">
        {{ error }}
      </p>
    </div>
    <div v-else class="pb-6">
      <!-- Kestrel .read header -->
      <header class="flex items-start justify-between gap-4 px-4 pb-3 pt-4">
        <div class="min-w-0">
          <h1 class="readout truncate text-[28px] leading-8">
            {{ name || 'Unknown' }}
          </h1>
          <h2 class="mt-1 truncate text-[11px] text-fg-3">
            with {{ adapterName }}
          </h2>
        </div>
        <DropdownMenu>
          <DropdownMenuTrigger class="winctl" aria-label="More">
            <Ellipsis :size="14" :stroke-width="2" />
          </DropdownMenuTrigger>
          <DropdownMenuContent
            :side-offset="6"
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
              class="text-danger focus:bg-danger/10 focus:text-danger [&>svg]:text-danger"
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
      </header>

      <!-- Kestrel .tiles -->
      <section class="tiles" style="--cols: 3">
        <div class="tile" style="--accent: var(--charge)">
          <div class="k caption">
            <Timer :size="12" :stroke-width="2" />Duration
          </div>
          <div class="v num">
            {{ formatDuration(
              intervalToDuration({
                start: timestamp * 1000,
                end: timestamp * 1000 + chargingTime * 1000,
              }),
              { format: ['hours', 'minutes'], locale: shortEnDistanceLocale },
            )
            }}
          </div>
          <div class="s num">
            {{ format(timestamp * 1000, 'yyyy-MM-dd HH:mm') }}
          </div>
        </div>
        <div class="tile" style="--accent: var(--adapter)">
          <div class="k caption">
            <Gauge :size="12" :stroke-width="2" />Avg Power
          </div>
          <div class="v num">
            {{ data.avg.adapterPower.toFixed(1) }}W
          </div>
          <div class="s">
            Peak <span class="num">{{ data.peak.adapterPower.toFixed(1) }}W</span>
          </div>
        </div>
        <div class="tile" style="--accent: var(--temp)">
          <div class="k caption">
            <Thermometer :size="12" :stroke-width="2" />Charging rate
          </div>
          <div class="v num">
            {{ ((endLevel - fromLevel) / chargingTime * 60).toFixed(2) }}%/min
          </div>
          <div class="s">
            Avg Temp <span class="num">{{ data.avg.temperature.toFixed(1) }}°C</span>
          </div>
        </div>
      </section>

      <section class="border-b border-line px-4 pb-3">
        <header class="flex h-10 items-center justify-between gap-4">
          <span class="caption">Charging Curve</span>
          <Legend :items="curveSeries" @toggle="toggle" />
        </header>
        <Chart
          class="h-[220px]"
          :series="curveSeries"
          :labels="curveLabels"
          :format="(v: number) => v.toFixed(0)"
        />
      </section>

      <section class="px-4">
        <header class="flex h-10 items-center">
          <span class="caption">Additional Detail</span>
        </header>
        <!-- Kestrel .facts with dotted leaders -->
        <dl class="facts max-w-sm text-xs">
          <div>
            <dt>Temperature Peak</dt>
            <dd class="num">
              {{ data.peak.temperature.toFixed(1) }}°C
            </dd>
          </div>
          <div>
            <dt>Adapter Power Peak</dt>
            <dd class="num">
              {{ data.peak.adapterPower.toFixed(1) }}W
            </dd>
          </div>
          <div>
            <dt>Adapter Watts</dt>
            <dd class="num">
              {{ data.peak.adapterWatts }}W ({{ data.peak.adapterVoltage }}V, {{ data.peak.adapterAmperage }}A)
            </dd>
          </div>
        </dl>
      </section>
    </div>
  </div>
</template>
