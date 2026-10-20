<script setup lang="ts">
import { addSeconds, format } from 'date-fns'
import { ArrowUpDown } from 'lucide-vue-next'

const power = usePower()
const rawData = usePowerRaw()

const showRemainDuration = ref(true)
const buttonText = computed(() => {
  if (showRemainDuration.value) {
    const minutes = power.value.timeRemain.secs / 60
    const hours = Math.floor(minutes / 60)

    return `${hours}h ${minutes % 60}m`
  }
  return format(
    addSeconds(new Date(), power.value.timeRemain.secs),
    'HH:mm',
  )
})
</script>

<template>
  <div class="caption flex items-center gap-2">
    {{ power.isCharging ? $t('status.charging_power') : $t('status.system_power') }}
    <span
      v-if="power.isRemote"
      class="size-1.5 rounded-full"
      :class="{
        'bg-ok animate-pulse': !rawData.isLocal && !rawData.offline,
        'bg-fg-4': !rawData.isLocal && rawData.offline,
      }"
    />
  </div>

  <span v-if="power.isLoading" class="scan h-[18px] w-24" />
  <span
    v-else-if="power.isCharging"
    class="chip accent num truncate"
    style="--accent: var(--adapter)"
  >
    <b class="font-medium">{{ power.adapterWatts }}W</b>
    <span class="opacity-70">{{ power.adapterVoltage }}V · {{ power.adapterAmperage }}A</span>
  </span>
  <button
    v-else
    class="chip accent num w-[76px] justify-center truncate transition-colors duration-75 hover:bg-accent/20"
    @click.stop="showRemainDuration = !showRemainDuration"
  >
    <b class="font-medium">{{ buttonText }}</b>
    <ArrowUpDown
      :size="10"
      :stroke-width="2"
      class="opacity-70 transition-transform duration-300"
      :class="{ 'rotate-180': showRemainDuration }"
    />
  </button>
</template>
