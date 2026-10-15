<script setup lang="ts">
import type { ChargingHistory } from '@/bindings'
import { events } from '@/bindings'
import { useHistory } from '@/composables/useHistory'
import { Info } from 'lucide-vue-next'

const { selectedItem, history: { data, isLoading, update } } = useHistory()

onMounted(() => {
  const unlisten = events.historyRecordedEvent.listen(() => {
    update()
  })

  onScopeDispose(() => unlisten.then(f => f()))
})
</script>

<template>
  <div
    v-if="!isLoading && !data?.length"
    class="flex h-full w-full flex-col items-center justify-center gap-2 text-xs text-muted-foreground"
  >
    <Info class="w-6 h-6" />
    <span class="mb-16">No history recorded yet, charge your device to get started</span>
  </div>
  <div v-else class="flex h-[calc(100vh-80px)]">
    <div class="flex flex-col gap-4 pl-4 ">
      <h2 class="font-serif text-xl leading-none">
        History
      </h2>
      <div v-if="!isLoading && data" class="flex h-full flex-col gap-1 overflow-y-auto pr-4">
        <HistoryListItem
          v-for="item in data as ChargingHistory[]"
          :key="item.id"
          v-bind="item"
          :class="{ 'border-border bg-secondary': selectedItem?.id === item.id }"
          @click="selectedItem = selectedItem?.id === item.id ? null : item"
        />
        <div class="my-4 font-mono" />
      </div>
    </div>
    <Separator orientation="vertical" class="h-auto" />
    <div class="relative grow">
      <HistoryDetail
        v-if="selectedItem?.id"
        v-bind="selectedItem"
        class="h-full"
      />
      <div v-else class="overflow-y-auto h-full flex flex-col items-center justify-center">
        <Info class="size-6 text-muted-foreground" />
        <p class="mb-10 text-xs font-medium text-muted-foreground">
          Select a charging session to view details
        </p>
      </div>
    </div>
  </div>
</template>
