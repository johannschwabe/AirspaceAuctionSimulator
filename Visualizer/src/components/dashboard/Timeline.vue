<template>
  <div>
    <vue-apex-charts
      type="bar"
      height="75"
      :options="chartOptions"
      :series="series"
    />
    <div style="padding: 0 15px 0 35px; margin-top: -30px">
      <n-slider
        v-model:value="simulationStore.tick"
        :min="1"
        :max="simulationStore.dimensions.t"
        show-tooltip
        placement="bottom"
      />
    </div>
  </div>
</template>

<script setup>
import VueApexCharts from "vue3-apexcharts";

import { useSimulationStore } from "../../stores/simulation";

const simulationStore = useSimulationStore();

const chartOptions = {
  chart: {
    height: 75,
    type: "bar",
    background: "transparent",
    toolbar: { show: false },
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

const series = [
  {
    name: "# Active Agents",
    data: Array(simulationStore.dimensions.t).fill(0),
  },
];

simulationStore.locations.forEach((loc) => {
  series[0].data[loc.t] += 1;
});
</script>

<style scoped></style>
