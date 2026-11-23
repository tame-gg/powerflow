<script setup lang="tsx">
import { BatteryMedium, Cpu, Laptop, Monitor, PlugZap, Smartphone } from 'lucide-vue-next'
import CommonTooltip from './CommonTooltip.vue'

const formatter = new Intl.NumberFormat('en-US', {
  maximumFractionDigits: 1,
  minimumFractionDigits: 1,
})

// Kestrel accent per reading (src/assets/theme.css)
type FlowColor = 'system' | 'adapter' | 'screen' | 'soc' | 'charge'

interface FlowItemProps {
  tooltip: string
  icon: Component
  color: FlowColor
}

const FlowItem: Component = ({ tooltip, icon, color }: FlowItemProps, { slots }) => {
  return (
    <CommonTooltip content={tooltip} as-child>
      <div
        class="flex h-7 w-24 shrink-0 items-center justify-center gap-2 rounded border border-line-2 bg-surface transition-colors duration-75 hover:border-accent/40 hover:bg-accent/10"
        style={{ '--accent': `var(--${color})` }}
      >
        { h(icon, { 'size': 12, 'stroke-width': 2, 'class': 'text-accent' }) }
        <span class="num text-[11px] font-medium">
          { slots.default?.() }
          <small class="ml-0.5 font-sans text-fg-3">W</small>
        </span>
      </div>
    </CommonTooltip>
  )
}
const power = usePower()
</script>

<template>
  <section class="flex min-w-0 flex-1 flex-col px-4 pb-4">
    <!-- Kestrel .band header -->
    <header class="flex h-10 items-center">
      <span class="caption">{{ $t('power_flow') }}</span>
    </header>
    <span v-if="power.isLoading" class="scan h-[120px] w-full" />
    <div
      v-else
      class="well flex h-[120px] w-full items-center justify-between p-4"
      :class="[power.isCharging ? '' : 'flex-row-reverse']"
    >
      <FlowItem
        v-if="power.isCharging"
        :tooltip="$t('flow.adapter_power')"
        :icon="PlugZap"
        color="adapter"
      >
        {{ formatter.format(power.systemIn + power.efficiencyLoss / 1000) }}
      </FlowItem>

      <CommonTooltip
        v-if="power.isCharging"
        :content="`${$t('flow.power_loss')}: ${power.efficiencyLoss}mw`"
        as-child
      >
        <Shimmer
          :repeat-delay="1500"
          class="mx-2 w-full rounded-full"
          style="--accent: var(--adapter)"
        >
          <div class="h-px" />
        </Shimmer>
      </CommonTooltip>

      <div class="flex flex-col items-center gap-2 rounded border border-line bg-background p-2">
        <div v-if="!power.isRemote" class="flex gap-2">
          <FlowItem :tooltip="$t('flow.screen_power')" :icon="Monitor" color="screen">
            {{ formatter.format(power.brightnessPower || 0) }}
          </FlowItem>

          <FlowItem :tooltip="$t('flow.heatpipe_power')" :icon="Cpu" color="soc">
            {{ formatter.format(power.heatpipePower || 0) }}
          </FlowItem>
        </div>

        <FlowItem
          :tooltip="$t('flow.system_total')"
          :icon="power.isRemote ? Smartphone : Laptop"
          color="system"
        >
          {{ formatter.format(power.systemLoad) }}
        </FlowItem>
      </div>

      <Shimmer
        :delay="2000"
        :repeat-delay="1500"
        class="mx-2 w-full rounded-full"
        style="--accent: var(--charge)"
      >
        <div class="h-px" />
      </Shimmer>

      <FlowItem :tooltip="power.isCharging ? $t('flow.battery_in') : $t('flow.battery_out')" :icon="BatteryMedium" color="charge">
        {{ formatter.format(power.batteryPower) }}
      </FlowItem>
    </div>
  </section>
</template>
