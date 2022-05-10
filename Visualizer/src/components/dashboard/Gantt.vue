<template>
  <vue-apex-charts type="rangeBar" height="250" :options="chartOptions" :series="series" />
</template>

<script setup>
import VueApexCharts from "vue3-apexcharts";
import { reactive } from "vue";

import { useSimulationSingleton } from "../../scripts/simulation";
import { onAgentsSelected } from "../../scripts/emitter";

const simulation = useSimulationSingleton();

const chartOptions = {
  chart: {
    height: 250,
    type: "rangeBar",
    background: "transparent",
    toolbar: { show: false },
    zoom: { enabled: false },
    animations: { enabled: false },
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

const series = reactive([
  {
    data: [],
  },
]);

const updateState = () => {
  const gantt = [];
  console.log("Welfare: Update State");
  simulation.selectedAgents.forEach((agent) => {
    agent.paths.forEach((path) => {
      const start = path.firstTick;
      const end = path.lastTick;
      gantt.push({
        x: agent.name,
        y: [start, end],
        fillColor: agent.color,
      });
    });
  });
  series[0].data = gantt;
  console.log("Welfare: Done");
};

updateState();

onAgentsSelected(() => {
  updateState();
});
</script>

<style scoped></style>
