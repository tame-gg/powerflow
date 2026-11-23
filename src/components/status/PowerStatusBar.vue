<script setup lang="ts">
import type { UnwrapRef } from 'vue'
import { useI18n } from 'vue-i18n'

const power = usePower()
const { t } = useI18n()

// Kestrel one-hue-per-reading accents (src/assets/theme.css)
const colors: Record<string, string> = {
  systemTotal: 'var(--system)',
  screen: 'var(--screen)',
  heatpipe: 'var(--soc)',
  systemOther: 'var(--other)',
  batteryIn: 'var(--charge)',
  powerLoss: 'var(--loss)',
}

const localeMap = computed(() => ({
  screen: t('status.screen_power'),
  heatpipe: t('status.heatpipe_power'),
  systemOther: t('status.system_other'),
  batteryIn: t('status.battery_in'),
  systemTotal: t('status.system_total'),
  powerLoss: t('status.power_loss'),
}))

interface BarData {
  parts: [string, {
    value: number
    left: number
    color: string
    locale: string
  }][]
  sum: number
}

const data = ref<BarData>()
const handle = watchEffect(() => {
  const parts: Record<string, number> = {
    systemTotal: power.value.systemLoad,
  }

  if (power.value.isCharging) {
    parts.batteryIn = power.value.systemIn - parts.systemTotal
    parts.powerLoss = power.value.efficiencyLoss
  }

  if (!power.value.isRemote) {
    parts.screen = power.value.brightnessPower
    parts.heatpipe = power.value.heatpipePower
    parts.systemOther = parts.systemTotal - parts.screen - parts.heatpipe
    delete parts.systemTotal
  }

  let current = 0
  const sorted = Object.entries(parts)
    .sort((a, b) => b[1] - a[1])
    .map(([key, value]) => {
      const ret = [key, current] as const
      current += value
      return ret
    })

  const sum = power.value.isCharging
    ? power.value.systemIn + power.value.efficiencyLoss
    : power.value.systemLoad
  data.value = {
    parts: Object.entries(parts)
      .map(([key, value]) =>
        [key, {
          value,
          left: sorted[sorted.findIndex(([k]) => k === key)][1] / sum,
          color: colors[key],
          locale: localeMap.value[key as keyof UnwrapRef<typeof localeMap>],
        }],
      ),
    sum,
  }
})

const hovered = ref<string | null>(null)

watchEffect(() => {
  hovered.value ? handle.pause() : handle.resume()
})
</script>

<template>
  <!-- Charging: total = powerloss + screen + heatpipe + system other + battery in -->
  <!-- Not Charging: total = screen + heatpipe + system other -->
  <!-- Kestrel .prop: proportional segments with 2px gaps, largest first -->
  <div
    v-if="data"
    class="prop"
    @mouseleave="hovered = null"
  >
    <CommonTooltip
      v-for="[key, { value, color, locale }] in [...data.parts].sort((a, b) => a[1].left - b[1].left)"
      :key="key"
      as-child
    >
      <template #popper>
        <span class="text-fg-2">{{ locale }}</span>
        <span class="num ml-2 font-medium">{{ value.toFixed(1) }}W</span>
      </template>
      <i
        :class="[hovered && hovered !== key ? 'opacity-20' : 'opacity-100']"
        :style="{ flexGrow: Math.max(0, value), background: color }"
        @mouseover="hovered = key"
      />
    </CommonTooltip>
  </div>
</template>
