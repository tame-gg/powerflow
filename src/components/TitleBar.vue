<script setup lang="ts">
import { commands } from '@/bindings'
import { ChevronLeft, History, Laptop, SettingsIcon, Smartphone } from 'lucide-vue-next'

const tab = useTab()
const data = usePowerData()

const {
  tabName,
  tabNameLoading,
} = useTitlebar()
</script>

<template>
  <!-- Kestrel .toolbar: 52px on macOS (traffic lights inset), hairline below -->
  <header
    data-tauri-drag-region
    class="toolbar sticky top-0 z-10 pl-24"
  >
    <button
      v-if="$route.path !== '/'"
      class="winctl"
      aria-label="Back"
      @click="$router.back()"
    >
      <ChevronLeft :size="14" :stroke-width="2" />
    </button>
    <div v-else class="flex min-w-0 items-center gap-3">
      <TabsList aria-label="Device">
        <TransitionGroup
          enter-from-class="w-0"
          leave-to-class="w-0"
          enter-to-class="w-[29px]"
          leave-from-class="w-[29px]"
          enter-active-class="duration-300"
          leave-active-class="duration-300"
        >
          <TabsTrigger
            key="local"
            value="local"
            title="This Mac"
          >
            <Laptop :size="13" :stroke-width="2" :class="[tab === 'local' ? 'text-gold' : '']" />
          </TabsTrigger>

          <TabsTrigger
            v-for="udid in Object.keys(data.remote)"
            :key="udid"
            :value="udid"
            :title="data.remote[udid].name || udid"
          >
            <Smartphone :size="13" :stroke-width="2" :class="[tab === udid ? 'text-gold' : '']" />
          </TabsTrigger>
        </TransitionGroup>
      </TabsList>
      <div data-tauri-drag-region class="title">
        <span v-if="tabNameLoading" class="scan h-4 w-28 self-center" />
        <b v-else data-tauri-drag-region>{{ tabName }}</b>
        <span data-tauri-drag-region>
          {{ tab === 'local' ? 'Local' : Array.from(data.remote[tab].interface || []).join(' and ') || 'offline' }}
        </span>
      </div>
    </div>
    <div
      data-tauri-drag-region
      class="wordmark pointer-events-none absolute left-1/2 -translate-x-1/2"
    >
      Powerflow
    </div>
    <div class="tools" data-tauri-drag-region>
      <CommonTooltip content="History" as-child>
        <button
          class="winctl"
          :class="{ on: $route.path === '/history' }"
          aria-label="History"
          @click="$route.path === '/history' ? $router.back() : $router.push('/history')"
        >
          <History
            :size="14"
            :stroke-width="2"
            class="transition-transform duration-300"
            :class="{ 'rotate-[-360deg]': $route.path === '/history' }"
          />
        </button>
      </CommonTooltip>
      <CommonTooltip content="Settings" as-child>
        <button class="winctl" aria-label="Settings" @click="commands.openSettings()">
          <SettingsIcon :size="14" :stroke-width="2" />
        </button>
      </CommonTooltip>
    </div>
  </header>
</template>
