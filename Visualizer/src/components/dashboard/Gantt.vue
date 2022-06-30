<template>
  <vue-apex-charts ref="chart" type="rangeBar" height="250" :options="chartOptions" :series="series" />
</template>

<script setup>
import VueApexCharts from "vue3-apexcharts";
import { reactive, ref } from "vue";

import { useSimulationSingleton } from "../../scripts/simulation";
import { onAgentsSelected } from "../../scripts/emitter";

const simulation = useSimulationSingleton();

const chart = ref(null);

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

const updateSeries = () => {
  const gantt = [];
  simulation.selectedAgents.forEach((agent) => {
    agent.paths.forEach((path) => {
      const start = path.firstTick;
      const end = path.lastTick;
      if (start === null || end === null) {
        console.log("failure");
      }
      gantt.push({
        x: agent.name,
        y: [start, end],
        fillColor: agent.color,
        // fillColor: "#259721",
      });
    });
  });
  series[0].data = gantt;
  console.log("Welfare: Done");
};

onAgentsSelected(() => {
  updateSeries();
});

updateSeries();
</script>

<style scoped></style>
