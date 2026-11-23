<script setup lang="ts">
import type { ChargingHistory } from '@/bindings'
import { events } from '@/bindings'
import { useHistory } from '@/composables/useHistory'
import { History } from 'lucide-vue-next'

const { selectedItem, history: { data, isLoading, update } } = useHistory()

onMounted(() => {
  const unlisten = events.historyRecordedEvent.listen(() => {
    update()
  })

  onScopeDispose(() => unlisten.then(f => f()))
})
</script>

<template>
  <!-- Kestrel .empty-state -->
  <div
    v-if="!isLoading && !data?.length"
    class="empty-state pb-16"
  >
    <History :size="24" :stroke-width="1.6" />
    <span class="wordmark nosig">No history</span>
    <p>No history recorded yet, charge your device to get started</p>
  </div>
  <div v-else class="flex h-full">
    <div class="flex w-72 shrink-0 flex-col border-r border-line">
      <div class="th caption grid-cols-[minmax(0,1fr)_auto]">
        <span>History</span>
        <span v-if="data" class="num">{{ data.length }}</span>
      </div>
      <div v-if="!isLoading && data" class="flex h-full flex-col overflow-y-auto">
        <HistoryListItem
          v-for="item in data as ChargingHistory[]"
          :key="item.id"
          v-bind="item"
          :selected="selectedItem?.id === item.id"
          @click="selectedItem = selectedItem?.id === item.id ? null : item"
        />
      </div>
    </div>
    <div class="relative min-w-0 grow">
      <HistoryDetail
        v-if="selectedItem?.id"
        v-bind="selectedItem"
        class="h-full"
      />
      <div v-else class="empty-state pb-10">
        <History :size="24" :stroke-width="1.6" />
        <span class="wordmark nosig">Nothing selected</span>
        <p>Select a charging session to view details</p>
      </div>
    </div>
  </div>
</template>
