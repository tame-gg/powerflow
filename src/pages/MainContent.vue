<template>
  <!-- Kestrel panels: flat sections divided by hairlines, no cards -->
  <div class="min-w-min">
    <div class="flex border-b border-line">
      <PowerStatus class="w-80 shrink-0 border-r border-line" />
      <PowerFlow />
    </div>
    <PowerUsageChart />
    <TechnicalDetail />
  </div>
</template>
