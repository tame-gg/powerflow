<script setup lang="ts">
import type { ChartSeries } from '@/components/kestrel/Chart.vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const power = usePower()

// Kestrel accent per reading (src/assets/theme.css)
const colorMap: Record<string, string> = {
  'System Power': 'var(--system)',
  'Screen Power': 'var(--screen)',
  'Heatpipe Power': 'var(--soc)',
  'System In': 'var(--adapter)',
}

const categories = computed(() => {
  const base = ['System Power'] as (keyof StatisticData)[]
  if (!power.value.isRemote) {
    base.push('Screen Power', 'Heatpipe Power')
  }
  if (power.value.isCharging) {
    base.push('System In')
  }
  return base
})

const localeMap = computed<Record<string, string>>(() => ({
  'System Power': t('flow.system_total'),
  'Screen Power': t('flow.screen_power'),
  'Heatpipe Power': t('flow.heatpipe_power'),
  'System In': t('flow.system_in'),
}))

const inactive = ref(new Set<string>())
function toggle(name: string) {
  const next = new Set(inactive.value)
  next.has(name) ? next.delete(name) : next.add(name)
  inactive.value = next
}

const series = computed<ChartSeries[]>(() => categories.value.map(key => ({
  name: localeMap.value[key] || key,
  color: colorMap[key],
  unit: 'W',
  values: power.value.statistics.map(item => Number(item[key] ?? 0)),
  inactive: inactive.value.has(localeMap.value[key] || key),
})))

const labels = computed(() => power.value.statistics.map(item => item.time))
</script>

<template>
  <section class="w-full border-b border-line px-4 pb-3">
    <!-- Kestrel .band header -->
    <header class="flex h-10 items-center justify-between gap-4">
      <span class="caption">{{ $t('power_usage') }}</span>
      <Legend
        v-if="!power.isLoading"
        :items="series"
        @toggle="toggle"
      />
    </header>
    <span v-if="power.isLoading" class="scan block h-[240px] w-full" />
    <Chart
      v-else
      class="h-[240px] w-full"
      :series="series"
      :labels="labels"
      :format="(v: number) => `${v.toFixed(v >= 10 ? 0 : 1)}W`"
    />
  </section>
</template>
