<template>
  <vue-apex-charts
    type="area"
    height="250"
    :options="chartOptions"
    :series="series"
  />
</template>

<script setup>
import VueApexCharts from "vue3-apexcharts";

import { useSimulationStore } from "../../stores/simulation";
import { reactive } from "vue";

const simulationStore = useSimulationStore();

const chartOptions = reactive({
  chart: {
    height: 250,
    type: "area",
    background: "transparent",
    toolbar: { show: false },
  },
  theme: {
    mode: "dark",
  },
  title: {
    text: "Welfare over Time",
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    curve: "smooth",
  },
  colors: ["#63e2b7", "#6381e2"],
  annotations: {
    xaxis: [
      {
        x: simulationStore.tick * 5,
      },
    ],
  },
  xaxis: {
    labels: { show: false },
    axisTicks: { show: false },
    axisBorder: { show: false },
  },
  yaxis: {
    labels: {
      formatter: (value) => {
        return Math.round(value);
      },
    },
  },
});

simulationStore.$subscribe(() => {
  console.log("Updating annotation");
  chartOptions.annotations.xaxis[0].x = simulationStore.tick * 5;
});

const series = reactive([
  {
    name: "Optimal Welfare",
    data: Array(simulationStore.dimensions.t).fill(0),
  },
  {
    name: "Achieved Welfare",
    data: Array(simulationStore.dimensions.t).fill(0),
  },
]);

simulationStore.agents.forEach((agent) => {
  if (agent.locations.length > 0) {
    const arrivalTick = agent.locations[-1].t;
    series[0].data[arrivalTick] += agent.optimal_welfare;
    series[1].data[arrivalTick] += agent.achieved_welfare;
  }
});

for (let i = 1; i < simulationStore.dimensions.t; i++) {
  series[0].data[i] = series[0].data[i - 1] + series[0].data[i];
  series[1].data[i] = series[1].data[i - 1] + series[1].data[i];
}
</script>

<style scoped></style>
