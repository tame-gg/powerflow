<script setup lang="ts">
// Port of kestrel/src/lib/components/Chart.tsx: a well behind the plot,
// 6 column grid with ticks, quarter rules, a glow-backed 1.5px trace with a
// faint gradient under the first series, a last-value flag on the right and
// a crosshair cursor on hover. Extended to draw several series at once.
import { smoothPath } from './path'

export interface ChartSeries {
  name: string
  color: string
  values: number[]
  unit?: string
  inactive?: boolean
}

const props = withDefaults(defineProps<{
  series: ChartSeries[]
  labels?: string[]
  format?: (v: number) => string
  max?: number
}>(), {
  labels: () => [],
  format: (v: number) => v.toFixed(1),
})

const el = useTemplateRef<HTMLDivElement>('el')
const { width, height } = useElementSize(el)
const hover = ref<number | null>(null)
const id = `g${Math.random().toString(36).slice(2, 8)}`

const padR = 50
const padT = 8
const padB = 18

function niceMax(v: number): number {
  if (v <= 0)
    return 1
  const p = 10 ** Math.floor(Math.log10(v))
  const m = v / p
  const n = m <= 1 ? 1 : m <= 2 ? 2 : m <= 2.5 ? 2.5 : m <= 5 ? 5 : 10
  return n * p
}

const px = (v: number) => Math.round(v) + 0.5

const W = computed(() => Math.max(0, width.value - padR))
const H = computed(() => height.value - padB)
const n = computed(() => Math.max(2, ...props.series.map(s => s.values.length)))
const top = computed(() => props.max ?? niceMax(Math.max(0, ...props.series.flatMap(s => s.inactive ? [] : s.values)) * 1.1))
const x = (i: number, len: number) => ((i + (n.value - len)) / (n.value - 1)) * W.value
const y = (v: number) => padT + (1 - Math.min(1, Math.max(0, v) / top.value)) * (H.value - padT)
const pts = (s: number[]) => s.map((v, i) => [x(i, s.length), y(v)] as [number, number])

const main = computed(() => props.series[0]?.values ?? [])
const paths = computed(() => props.series.map(s => smoothPath(pts(s.values), padT, H.value)))
const lastY = computed(() => main.value.length > 1 ? y(main.value[main.value.length - 1]) : null)
const cols = computed(() => [0, 1, 2, 3, 4, 5, 6].map(k => px((W.value * k) / 6)))
const rules = [0, 0.25, 0.5, 0.75, 1]

const hv = computed(() => {
  if (hover.value === null)
    return null
  const idx = Math.round((hover.value / W.value) * (n.value - 1)) - (n.value - main.value.length)
  return idx >= 0 && idx < main.value.length ? idx : null
})

function label(k: number) {
  return props.labels[k - (n.value - props.labels.length)] ?? ''
}

function onMove(e: MouseEvent) {
  hover.value = e.clientX - (e.currentTarget as SVGElement).getBoundingClientRect().left
}
</script>

<template>
  <div ref="el" class="relative h-full min-h-[160px]">
    <template v-if="width > 0 && height > 0">
      <div class="well pointer-events-none absolute left-0" :style="{ top: `${padT}px`, width: `${W}px`, height: `${H - padT}px` }" />
      <svg
        class="absolute left-0 top-0 overflow-visible"
        :width="width"
        :height="height"
        @mousemove="onMove"
        @mouseleave="hover = null"
      >
        <defs>
          <linearGradient
            :id="id"
            x1="0"
            y1="0"
            x2="0"
            y2="1"
          >
            <stop offset="0" :stop-color="series[0]?.color" stop-opacity="0.10" />
            <stop offset="1" :stop-color="series[0]?.color" stop-opacity="0" />
          </linearGradient>
        </defs>
        <g v-for="cx in cols" :key="cx">
          <line
            :x1="cx"
            :x2="cx"
            :y1="padT"
            :y2="H"
            stroke="var(--grid)"
          />
          <line
            :x1="cx"
            :x2="cx"
            :y1="H"
            :y2="H + 4"
            stroke="var(--tick)"
          />
        </g>
        <g v-for="t in rules" :key="t">
          <line
            :x1="0"
            :x2="W"
            :y1="px(y(top * t))"
            :y2="px(y(top * t))"
            :stroke="t === 0 || t === 0.5 ? 'var(--tick)' : 'var(--grid)'"
          />
          <text
            v-if="(t === 0.5 || t === 1) && (lastY === null || Math.abs(y(top * t) - lastY) >= 12)"
            :x="W + 8"
            :y="y(top * t) + 3.5"
            font-size="10"
            fill="var(--text-3)"
            class="num"
          >{{ format(top * t) }}</text>
        </g>
        <path
          v-if="main.length > 1 && !series[0].inactive"
          :d="`${paths[0]}L${W},${H}L${x(0, main.length)},${H}Z`"
          :fill="`url(#${id})`"
        />
        <g
          v-for="(s, i) in series"
          :key="s.name"
          class="transition-opacity duration-200"
          :opacity="s.inactive ? 0.15 : 1"
        >
          <template v-if="s.values.length > 1">
            <path
              :d="paths[i]"
              fill="none"
              :stroke="s.color"
              stroke-opacity="0.18"
              stroke-width="4"
              stroke-linejoin="round"
            />
            <path
              :d="paths[i]"
              fill="none"
              :stroke="s.color"
              stroke-width="1.5"
              stroke-linejoin="round"
            />
          </template>
        </g>
        <template v-if="lastY !== null && series[0]">
          <polygon :points="`${W},${lastY} ${W + 6},${lastY - 4} ${W + 6},${lastY + 4}`" :fill="series[0].color" />
          <text
            :x="W + 10"
            :y="lastY + 3.5"
            font-size="10"
            font-weight="600"
            :fill="series[0].color"
            class="num"
          >{{ format(main[main.length - 1]) }}</text>
        </template>
        <text
          v-for="f in [0, 1 / 3, 2 / 3, 1]"
          :key="f"
          :x="f * W"
          :y="height - 4"
          font-size="10"
          fill="var(--text-3)"
          class="num"
          :text-anchor="f === 0 ? 'start' : f === 1 ? 'end' : 'middle'"
        >{{ label(Math.round(f * (n - 1))) }}</text>
        <g v-if="hv !== null">
          <line
            :x1="px(x(hv, main.length))"
            :x2="px(x(hv, main.length))"
            :y1="padT"
            :y2="H"
            stroke="var(--line-2)"
          />
          <line
            :x1="0"
            :x2="W"
            :y1="px(y(main[hv]))"
            :y2="px(y(main[hv]))"
            stroke="var(--line-2)"
          />
          <template v-for="s in series" :key="s.name">
            <circle
              v-if="!s.inactive && s.values[hv - (main.length - s.values.length)] !== undefined"
              :cx="x(hv, main.length)"
              :cy="y(s.values[hv - (main.length - s.values.length)])"
              r="3"
              :fill="s.color"
              stroke="var(--well)"
              stroke-width="1.5"
            />
          </template>
        </g>
      </svg>
      <div
        v-if="hv !== null"
        class="flag pointer-events-none absolute flex flex-col gap-0.5 px-2 py-1 text-[11px] leading-4 animate-fade"
        :style="{ top: `${padT + 8}px`, ...(hover! > W / 2 ? { left: '8px' } : { right: `${padR + 8}px` }) }"
      >
        <span class="num t3">{{ label(hv + (n - main.length)) }}</span>
        <template v-for="s in series" :key="s.name">
          <span v-if="!s.inactive && s.values[hv - (main.length - s.values.length)] !== undefined" class="flex items-center gap-2 whitespace-nowrap">
            <i class="size-2 rounded-[2px]" :style="{ background: s.color }" />
            <span class="t2 flex-1">{{ s.name }}</span>
            <b class="num ml-3 font-medium">{{ format(s.values[hv - (main.length - s.values.length)]) }}{{ s.unit ?? '' }}</b>
          </span>
        </template>
      </div>
    </template>
  </div>
</template>
