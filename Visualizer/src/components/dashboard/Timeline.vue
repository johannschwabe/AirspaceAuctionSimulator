<template>
  <div>
    <vue-apex-charts type="bar" height="75" :options="chartOptions" :series="series" />
    <div style="padding: 0 15px 0 35px; margin-top: -30px">
      <n-slider
        :value="simulation.tick"
        @update:value="(t) => (simulation.tick = t)"
        :min="0"
        :max="simulation.maxTick - 1"
        show-tooltip
        placement="bottom"
      />
    </div>
  </div>
</template>

<script setup>
import VueApexCharts from "vue3-apexcharts";
import { reactive } from "vue";

import { onAgentsSelected } from "../../scripts/emitter";
import { useSimulationSingleton } from "../../scripts/simulation";

const simulation = useSimulationSingleton();

const chartOptions = {
  chart: {
    height: 75,
    type: "bar",
    background: "transparent",
    toolbar: { show: false },
    zoom: { enabled: false },
    animations: { enabled: false },
  },
  theme: {
    mode: "dark",
  },
  dataLabels: {
    enabled: false,
  },
  colors: ["#2a947d"],
  stroke: { show: false },
  grid: { show: false },
  xaxis: {
    labels: { show: false },
    axisTicks: { show: false },
    axisBorder: { show: false },
  },
  yaxis: {
    labels: { show: false },
    axisTicks: { show: false },
    axisBorder: { show: false },
  },
};

const series = reactive([
  {
    name: "# Active Agents",
    data: simulation.timeline,
  },
]);

onAgentsSelected(() => {
  series[0].data = simulation.timeline;
});
</script>

<style scoped></style>
