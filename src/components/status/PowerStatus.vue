<script setup lang="ts">
const isPopover = inject('isPopover', false)
</script>

<template>
  <!-- Kestrel .read (main window) / .mini-read (popover) -->
  <section
    class="flex min-w-0 flex-col"
    :class="isPopover ? 'h-full gap-2 px-3 pb-3 pt-2.5' : 'gap-2 p-4'"
  >
    <div class="flex h-6 items-center justify-between gap-2">
      <PowerStatusTitle />
    </div>
    <div class="-mt-1 flex items-center gap-[3px] truncate text-[11px] text-fg-3">
      <PowerStatusDescription />
    </div>
    <PowerStatusNumber />
    <PowerStatusFooter class="mt-auto" />
  </section>
</template>
