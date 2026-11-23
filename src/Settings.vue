<script setup lang="tsx">
import type { Component, SetupContext } from 'vue'
import { Label } from '@/components/ui/label'
import {
  NumberField,
  NumberFieldContent,
  NumberFieldDecrement,
  NumberFieldIncrement,
  NumberFieldInput,
} from '@/components/ui/number-field'
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Switch } from '@/components/ui/switch'
import { open } from '@tauri-apps/plugin-shell'
import { Activity, BadgeInfo, BatteryCharging, CircleDashed, ExternalLink, Eye, Gauge, Info, Languages, Moon, Palette, RotateCw, Sun, SunMoon } from 'lucide-vue-next'
import { storeToRefs } from 'pinia'
import { h, ref, watch } from 'vue'
import { version } from '../package.json'
import { events } from './bindings'
import { Skeleton } from './components/ui/skeleton'
import { usePreference } from './stores/preference'

const commitHash = __COMMIT_HASH__

useSetup()

const loading = ref(true)
const preference = usePreference()

preference.$tauri.start().then(async () => {
  const refs = storeToRefs(preference)

  for (const key in refs) {
    // TODO: fix types
    const ref = refs[key as keyof typeof refs]
    watch(ref, () => {
      events.preferenceEvent.emit({
        [key as keyof typeof refs]: ref.value,
      } as any)
    })
  }

  loading.value = false
})

interface SettingsItemProps {
  name: string
  description: string
  icon: Component
}

// Kestrel row: 16px icon column, label over an 11px text-3 line, control right
function SettingsItem(props: SettingsItemProps, { slots }: SetupContext) {
  return (
    <div class="grid min-h-14 grid-cols-[16px_minmax(0,1fr)_auto] items-center gap-x-3 border-b border-line px-4 py-2.5 transition-colors duration-75 hover:bg-hover">
      { h(props.icon, { 'size': 14, 'stroke-width': 2, 'class': 'self-start mt-px text-fg-3' }) }
      <div class="flex min-w-0 flex-col gap-0.5">
        <Label>{props.name}</Label>
        <span class="mr-4 text-[11px] text-fg-3">
          {props.description}
        </span>
      </div>
      {slots.default ? slots.default() : null}
    </div>
  )
}

interface SettingsSectionProps {
  title: string
  icon: Component
}

// Kestrel .group header: sticky 28px strip, accent icon, 11px semibold label
function SettingsSection(props: SettingsSectionProps) {
  return (
    <div class="group-head">
      {h(props.icon, { 'size': 12, 'stroke-width': 2 })}
      <b>{props.title}</b>
    </div>
  )
}
</script>

<template>
  <div data-tauri-drag-region class="h-7 border-b border-line" />
  <div class="h-[calc(100dvh-28px)] overflow-y-auto bg-background" style="--accent: var(--gold)">
    <!-- Appearance Section -->
    <SettingsSection :title="$t('settings.appearance')" :icon="Eye" />
    <div>
      <SettingsItem
        :name="$t('settings.theme')"
        :description="$t('settings.theme_desc')"
        :icon="Palette"
      >
        <Select v-model="preference.theme">
          <SelectTrigger class="w-[130px]">
            <SelectValue placeholder="Select a theme" />
          </SelectTrigger>
          <SelectContent>
            <SelectGroup>
              <SelectItem value="system">
                <div class="flex items-center gap-2">
                  <SunMoon :size="12" :stroke-width="2" />
                  {{ $t('settings.theme_system') }}
                </div>
              </SelectItem>
              <SelectItem class="flex" value="light">
                <div class="flex items-center gap-2">
                  <Sun :size="12" :stroke-width="2" />
                  {{ $t('settings.theme_light') }}
                </div>
              </SelectItem>
              <SelectItem class="flex" value="dark">
                <div class="flex items-center gap-2">
                  <Moon :size="12" :stroke-width="2" />
                  {{ $t('settings.theme_dark') }}
                </div>
              </SelectItem>
            </SelectGroup>
          </SelectContent>
        </Select>
      </SettingsItem>

      <SettingsItem
        :name="$t('settings.language')"
        :description="$t('settings.language_desc')"
        :icon="Languages"
      >
        <Select v-model="preference.language" default-value="en">
          <SelectTrigger class="w-[120px]">
            <SelectValue placeholder="Select a language" />
          </SelectTrigger>
          <SelectContent>
            <SelectGroup>
              <SelectItem value="en">
                English
              </SelectItem>
              <SelectItem value="zh-CN">
                简体中文
              </SelectItem>
            </SelectGroup>
          </SelectContent>
        </Select>
      </SettingsItem>

      <SettingsItem
        :name="$t('settings.animations')"
        :description="$t('settings.animations_desc')"
        :icon="CircleDashed"
      >
        <Skeleton v-if="loading" class="h-[18px] w-8 rounded-full" />
        <Switch
          v-else
          id="animations"
          v-model:checked="preference.animationsEnabled"
        />
      </SettingsItem>
    </div>

    <!-- Updates & Monitoring Section -->
    <SettingsSection
      :title="$t('settings.update_and_monitoring')"
      :icon="RotateCw"
    />
    <div>
      <SettingsItem
        :name="$t('settings.update_frequency')"
        :description="$t('settings.update_frequency_desc')"
        :icon="Gauge"
      >
        <NumberField
          v-model="preference.updateInterval"
          :format-options="{
            useGrouping: false,
            style: 'unit',
            unit: 'millisecond',
            unitDisplay: 'short',
          }"
          locale="en-US"
          :min="500"
          :step="500"
          class="w-32"
        >
          <NumberFieldContent>
            <NumberFieldDecrement />
            <NumberFieldInput />
            <NumberFieldIncrement />
          </NumberFieldContent>
        </NumberField>
      </SettingsItem>

      <SettingsItem
        :name="$t('settings.background_monitoring')"
        :description="$t('settings.background_monitoring_desc')"
        :icon="Activity"
      >
        <Switch
          id="background-monitoring"
          disabled
          checked
        />
      </SettingsItem>

      <SettingsItem
        :name="$t('settings.status_bar')"
        :description="$t('settings.status_bar_desc')"
        :icon="BadgeInfo"
      >
        <Select v-model="preference.statusBarItem" default-value="system">
          <SelectTrigger class="w-[150px]">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectGroup>
              <SelectItem value="system">
                {{ $t('settings.system_total') }}
              </SelectItem>
              <SelectItem value="screen">
                {{ $t('settings.screen_power') }}
              </SelectItem>
              <SelectItem value="heatpipe">
                {{ $t('settings.heatpipe_power') }}
              </SelectItem>
            </SelectGroup>
          </SelectContent>
        </Select>
      </SettingsItem>

      <SettingsItem
        :name="$t('settings.show_charging_power')"
        :description="$t('settings.show_charging_power_desc')"
        :icon="BatteryCharging"
      >
        <Switch v-model:checked="preference.statusBarShowCharging" />
      </SettingsItem>
    </div>

    <!-- <Separator /> -->

    <!-- <section class="space-y-8">
      <SettingsSection title="Paired Devices" :icon="MobileIcon" />
      <div class="space-y-6">
        <SettingsItem
          name="iPhone 13 Pro"
          description="00000000-0000-0000-0000-000000000000"
          :icon="MobileIcon"
        >
          <Skeleton v-if="loading" class="w-12 h-6" />
          <Button
            variant="outline"
            size="sm"
            class="
          text-red-500 hover:text-red-600
          border-red-500/20 hover:border-red-500/50
          hover:bg-red-500/10
            "
          >
            Delete
          </Button>
        </SettingsItem>
      </div>
    </section> -->

    <!-- About Section: Kestrel About window layout -->
    <SettingsSection :title="$t('settings.about')" :icon="Info" />
    <div class="flex flex-col items-center gap-1 border-b border-line px-4 pb-4 pt-6 text-center">
      <span class="readout text-[28px] leading-8">Powerflow</span>
      <p class="max-w-sm text-[11px] text-fg-3">
        A tame.gg project. Based on
        <a
          class="text-gold underline-offset-2 hover:underline"
          @click="open('https://github.com/lzt1008/powerflow')"
        >Powerflow by lzt1008</a>, MIT license.
      </p>
    </div>
    <dl class="m-0 grid grid-cols-2 border-b border-line text-center [&>div+div]:border-l [&>div:nth-child(3)]:border-l-0 [&>div:nth-child(n+3)]:border-t [&>div]:border-line [&>div]:py-3">
      <div>
        <dt class="caption">
          {{ $t('settings.version') }}
        </dt>
        <dd class="num m-0 mt-1 text-[13px]">
          {{ version }}
        </dd>
      </div>
      <div>
        <dt class="caption">
          {{ $t('settings.build') }}
        </dt>
        <dd class="m-0 mt-1 flex items-center justify-center gap-2 text-[13px]">
          <span class="num">{{ commitHash.slice(0, 7) }}</span>
          <a
            class="flex items-center gap-1 text-[11px] text-gold underline-offset-2 hover:underline"
            @click="open(`https://github.com/tame-gg/powerflow/commit/${commitHash}`)"
          >
            View on GitHub
            <ExternalLink :size="11" :stroke-width="2" />
          </a>
        </dd>
      </div>
      <div>
        <dt class="caption">
          {{ $t('settings.license') }}
        </dt>
        <dd class="m-0 mt-1 text-[13px]">
          MIT License
        </dd>
      </div>
      <div>
        <dt class="caption">
          {{ $t('settings.author') }}
        </dt>
        <dd class="m-0 mt-1 text-[13px]">
          tame-gg
        </dd>
      </div>
    </dl>
    <footer class="flex flex-col items-center gap-0.5 py-6">
      <span class="font-serif text-xl leading-6">tame<em class="not-italic text-gold">.gg</em></span>
      <small class="text-[11px] text-fg-3">© 2026 tame.gg</small>
    </footer>
  </div>
</template>
