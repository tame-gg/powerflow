<script setup lang="ts">
// Kestrel's .lg legend rows (8px swatch, 2px radius), laid out inline.
// Clicking an entry toggles it, like the old chart legend did.
defineProps<{
  items: { name: string, color: string, inactive?: boolean }[]
}>()
const emit = defineEmits<{ toggle: [name: string] }>()
</script>

<template>
  <div class="flex flex-wrap items-center gap-x-4">
    <button
      v-for="item in items"
      :key="item.name"
      class="lg transition-opacity duration-75"
      :class="{ 'opacity-40': item.inactive }"
      @click="emit('toggle', item.name)"
    >
      <i :style="{ background: item.color }" />
      <span class="t">{{ item.name }}</span>
    </button>
  </div>
</template>
