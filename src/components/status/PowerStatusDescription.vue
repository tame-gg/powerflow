<script setup lang="ts">
import { useTimeAgoOptions } from '@/lib/i18n'

const power = usePower()
const rawData = usePowerRaw()

const timeAgoOptions = useTimeAgoOptions()

const updateTime = computed(() => power.value.lastUpdate * 1000)
const formatedUpdatetime = useTimeAgo(updateTime, timeAgoOptions)
</script>

<template>
  <div v-if="!power.isLoading" class="truncate">
    {{ power.isCharging ? power.adapterName : $t('status.on_battery') }}
    <template v-if="!rawData.isLocal && rawData.offline">
      <span>·</span>
      {{ $t('status.offline') }}
    </template>
    <template v-else-if="!rawData.isLocal">
      <span>·</span>
      {{ power.isRemote ? formatedUpdatetime : '' }}
    </template>
  </div>
  <span v-else class="scan h-3 w-24" />
</template>
