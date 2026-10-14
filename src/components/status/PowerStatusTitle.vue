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
  <div class="mr-10 flex gap-2 items-center">
    {{ power.isCharging ? $t('status.charging_power') : $t('status.system_power') }}
    <span
      v-if="power.isRemote"
      class="mr-1 size-2 rounded-full"
      :class="{
        'bg-success animate-pulse': !rawData.isLocal && !rawData.offline,
        'bg-hue-neutral': !rawData.isLocal && rawData.offline,
      }"
    />
  </div>

  <Skeleton v-if="power.isLoading" class="w-24 h-6" />
  <div
    v-else-if="power.isCharging"
    class="chip chip-accent h-6 truncate px-2"
  >
    <span class="mr-1 font-semibold">{{ power.adapterWatts }}W</span>
    <span class="text-[10px] opacity-70">({{ power.adapterVoltage }}V,{{
      power.adapterAmperage }}A)</span>
  </div>
  <div
    v-else
    class="chip chip-accent h-6 w-20 justify-center truncate px-2 transition-colors hover:bg-primary/20"
    @click.stop="showRemainDuration = !showRemainDuration"
  >
    <span class="mr-1 font-semibold">{{ buttonText }}</span>
    <ArrowUpDown
      class="size-3 opacity-70 transition-transform duration-300"
      :class="{ 'rotate-180': showRemainDuration }"
    />
  </div>
</template>
