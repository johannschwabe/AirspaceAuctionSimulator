<template>
  <vue-apex-charts
    type="rangeBar"
    height="250"
    :options="chartOptions"
    :series="series"
  />
</template>

<script setup>
import VueApexCharts from "vue3-apexcharts";

import { useSimulationStore } from "../../stores/simulation";

const simulationStore = useSimulationStore();

const chartOptions = {
  chart: {
    height: 250,
    type: "rangeBar",
    background: "transparent",
    toolbar: { show: false },
  },
  theme: {
    mode: "dark",
  },
  plotOptions: {
    bar: {
      horizontal: true,
      distributed: true,
    },
  },
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
    data: [],
  },
];

simulationStore.agents.forEach((agent) => {
  if (agent.locations.length > 0) {
    const start = agent.locations[0].t;
    const end = agent.locations[agent.locations.length - 1].t;
    series[0].data.push({
      x: agent.uuid,
      y: [start, end],
      fillColor: agent.owner.color,
    });
  }
});
</script>

<style scoped></style>
