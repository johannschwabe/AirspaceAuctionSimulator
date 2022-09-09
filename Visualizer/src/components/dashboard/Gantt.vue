<template>
  <vue-apex-charts ref="chart" type="rangeBar" height="250" :options="chartOptions" :series="series" />
</template>

<script setup>
import VueApexCharts from "vue3-apexcharts";
import { nextTick, onMounted, ref } from "vue";

import { useSimulationSingleton } from "@/scripts/simulation";
import { onAgentsSelected } from "@/scripts/emitter";

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

const series = [
  {
    data: [],
  },
];

const updateSeries = () => {
  const gantt = [];
  simulation.selectedAgents.forEach((agent) => {
    agent.segmentsStartEnd.forEach(([start, end]) => {
      if (start === null || end === null) {
        throw new Error("Invalid start or end of path!");
      }
      gantt.push({
        x: agent.id,
        y: [start, end],
        fillColor: agent.color,
      });
    });
  });
  series[0].data = gantt;
  chart.value.updateSeries(series);
};

onAgentsSelected(() => {
  updateSeries();
});

onMounted(() => {
  nextTick(() => {
    updateSeries();
  });
});
</script>

<style scoped></style>
