<script setup lang="ts">
import { Battery, CloudLightning, Cpu, Thermometer } from 'lucide-vue-next'

const power = usePower()
</script>

<template>
  <div class="flex-1 grid gap-4 grid-cols-4">
    <Card>
      <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle class="caption">
          {{ $t('temperature') }}
        </CardTitle>
        <Thermometer class="size-3.5 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <div v-if="!power.isLoading" class="readout text-[28px] leading-8">
          {{ power.temperature.toFixed(1) }}°C
        </div>
        <Skeleton v-else class="w-12 h-8" />
        <p class="text-[11px] text-muted-foreground">
          {{ $t('temperature_desc') }}
        </p>
      </CardContent>
    </Card>
    <Card>
      <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle class="caption">
          {{ $t('battery_health') }}
        </CardTitle>
        <Battery class="size-3.5 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <div v-if="!power.isLoading" class="readout text-[28px] leading-8">
          <!-- TODO: typing -->
          {{ (power.maxCapacity / power.designCapacity! * 100).toFixed(1) }}%
        </div>
        <Skeleton v-else class="w-12 h-8" />
        <p class="text-[11px] text-muted-foreground">
          {{ $t('battery_health_desc') }}
        </p>
      </CardContent>
    </Card>
    <Card>
      <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle class="caption">
          {{ $t('cycle_count') }}
        </CardTitle>
        <Cpu class="size-3.5 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <div v-if="!power.isLoading" class="readout text-[28px] leading-8">
          {{ power.cycleCount }} {{ $t('times') }}
        </div>
        <Skeleton v-else class="w-12 h-8" />
        <p class="text-[11px] text-muted-foreground">
          {{ $t('cycle_count_desc') }}
        </p>
      </CardContent>
    </Card>
    <Card>
      <CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle class="caption">
          Energy
        </CardTitle>
        <CloudLightning class="size-3.5 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <div v-if="!power.isLoading" class="readout text-[28px] leading-8">
          {{ power.currentCapacity }}mAh
        </div>
        <Skeleton v-else class="w-12 h-8" />
        <p class="flex gap-2 text-[11px] text-muted-foreground">
          Max Capacity: <span v-if="!power.isLoading">{{
            power.maxCapacity
          }}mAh</span>
          <Skeleton v-else class="w-12 h-4" />
        </p>
      </CardContent>
    </Card>
  </div>
</template>
