<script setup lang="ts">
import { commands } from '@/bindings'
import { LaptopIcon, MobileIcon } from '@radix-icons/vue'
import { ChevronLeft, History, SettingsIcon } from 'lucide-vue-next'

const tab = useTab()
const data = usePowerData()

const {
  tabName,
  tabNameLoading,
  shouldDisplayShadow,
} = useTitlebar()
</script>

<template>
  <div
    data-tauri-drag-region
    class="sticky top-0 z-10 flex h-[52px] items-center justify-between border-b bg-background pr-3 transition-colors"
    :class="shouldDisplayShadow ? 'border-border' : 'border-transparent'"
  >
    <div class="ml-[6rem] flex items-center gap-2">
      <div
        v-if="$route.path !== '/'"
        class="rounded-lg p-1 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
        @click="$router.back()"
      >
        <ChevronLeft class="size-5 -translate-x-px" />
      </div>
      <div v-else class="flex items-center gap-3">
        <TabsList>
          <TransitionGroup
            enter-from-class="w-0"
            leave-to-class="w-0"
            enter-to-class="w-[40px]"
            leave-from-class="w-[40px]"
            enter-active-class="duration-500"
            leave-active-class="duration-500"
          >
            <TabsTrigger key="local" class="px-0" value="local">
              <LaptopIcon class="mx-3 size-4" :class="[tab === 'local' ? 'text-primary' : 'text-muted-foreground']" />
            </TabsTrigger>

            <TabsTrigger
              v-for="udid in Object.keys(data.remote)"
              :key="udid"
              class="px-0"
              :value="udid"
            >
              <MobileIcon class="mx-3 size-4" :class="[tab === udid ? 'text-primary' : 'text-muted-foreground']" />
            </TabsTrigger>
          </TransitionGroup>
        </TabsList>
        <div class="flex flex-col gap-0.5">
          <Skeleton v-if="tabNameLoading" class="h-4 w-32" />
          <span v-else class="text-[13px] font-semibold leading-4">{{ tabName }}</span>
          <span class="caption">
            {{ tab === 'local' ? 'Local' : Array.from(data.remote[tab].interface || []).join(' and ') || 'offline' }}
          </span>
        </div>
      </div>
    </div>
    <div
      data-tauri-drag-region
      class="wordmark pointer-events-none absolute left-1/2 -translate-x-1/2"
    >
      Powerflow
    </div>
    <div class="flex gap-1">
      <div
        class="rounded-lg p-2 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
        @click="$route.path === '/history' ? $router.back() : $router.push('/history')"
      >
        <CommonTooltip content="History" as-child>
          <History
            :stroke-width="1.8"
            class="size-4 transition-transform duration-300"
            :class="{ 'text-foreground rotate-[-360deg]': $route.path === '/history' }"
          />
        </CommonTooltip>
      </div>
      <div
        class="rounded-lg p-2 text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
        @click="commands.openSettings()"
      >
        <CommonTooltip content="Settings" as-child>
          <SettingsIcon
            :stroke-width="1.8"
            class="size-4"
          />
        </CommonTooltip>
      </div>
    </div>
  </div>
</template>
