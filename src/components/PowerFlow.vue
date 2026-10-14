<script setup lang="tsx">
import { Battery, CloudLightningIcon, Cpu, Laptop, Monitor, Smartphone } from 'lucide-vue-next'
import CommonTooltip from './CommonTooltip.vue'

const formatter = new Intl.NumberFormat('en-US', {
  maximumFractionDigits: 1,
  minimumFractionDigits: 1,
})

type FlowColor = 'gold' | 'teal' | 'steel' | 'violet' | 'lime'

interface FlowItemProps {
  tooltip: string
  icon: Component
  color: FlowColor
}

const colorMap: Record<FlowColor, { icon: string, item: string }> = {
  gold: { icon: 'text-hue-gold', item: 'hover:border-hue-gold/40 hover:bg-hue-gold/10' },
  teal: { icon: 'text-hue-teal', item: 'hover:border-hue-teal/40 hover:bg-hue-teal/10' },
  steel: { icon: 'text-hue-steel', item: 'hover:border-hue-steel/40 hover:bg-hue-steel/10' },
  violet: { icon: 'text-hue-violet', item: 'hover:border-hue-violet/40 hover:bg-hue-violet/10' },
  lime: { icon: 'text-hue-lime', item: 'hover:border-hue-lime/40 hover:bg-hue-lime/10' },
}

const FlowItem: Component = ({ tooltip, icon, color }: FlowItemProps, { slots }) => {
  return (
    <CommonTooltip content={tooltip} as-child>
      <div
        class={`
        w-24 shrink-0 flex justify-center items-center gap-2
        rounded-lg border border-input bg-card bg-surface px-2 py-1.5
        transition-colors ${colorMap[color].item}`}
      >
        { h(icon, { class: `size-3.5 ${colorMap[color].icon}` }) }
        <span class="font-mono text-[11px] font-medium">
          { slots.default?.() }
          <span class="ml-[1px] text-muted-foreground">w</span>
        </span>
      </div>
    </CommonTooltip>
  )
}
const power = usePower()
</script>

<template>
  <Card class="flex-1">
    <CardHeader>
      <CardTitle class="caption">
        {{ $t('power_flow') }}
      </CardTitle>
    </CardHeader>
    <CardContent>
      <Skeleton v-if="power.isLoading" class="w-full h-[120px]" />
      <div
        v-else
        class="flex h-[120px] w-full items-center justify-between rounded-lg border bg-background p-4 text-xs"
        :class="[power.isCharging ? '' : 'flex-row-reverse']"
      >
        <FlowItem
          v-if="power.isCharging"
          :tooltip="$t('flow.adapter_power')"
          :icon="CloudLightningIcon"
          color="teal"
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
          >
            <div class="h-0.5" />
          </Shimmer>
        </CommonTooltip>

        <div class="flex flex-col items-center gap-2 rounded-lg border bg-card p-2">
          <div v-if="!power.isRemote" class="flex gap-4">
            <FlowItem :tooltip="$t('flow.screen_power')" :icon="Monitor" color="steel">
              {{ formatter.format(power.brightnessPower || 0) }}
            </FlowItem>

            <FlowItem :tooltip="$t('flow.heatpipe_power')" :icon="Cpu" color="violet">
              {{ formatter.format(power.heatpipePower || 0) }}
            </FlowItem>
          </div>

          <FlowItem
            :tooltip="$t('flow.system_total')"
            :icon="power.isRemote ? Smartphone : Laptop"
            color="gold"
          >
            {{ formatter.format(power.systemLoad) }}
          </FlowItem>
        </div>

        <Shimmer
          :delay="2000"
          :repeat-delay="1500"
          class="mx-2 w-full rounded-full"
        >
          <div class="h-0.5" />
        </Shimmer>

        <FlowItem :tooltip="power.isCharging ? $t('flow.battery_in') : $t('flow.battery_out')" :icon="Battery" color="lime">
          {{ formatter.format(power.batteryPower) }}
        </FlowItem>
      </div>
    </CardContent>
  </Card>
</template>
