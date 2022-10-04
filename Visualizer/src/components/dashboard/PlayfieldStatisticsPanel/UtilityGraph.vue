<template>
  <vue-apex-charts ref="chart" type="area" height="250" :options="chartOptions" :series="series" />
</template>

<script setup>
import VueApexCharts from "vue3-apexcharts";

import { reactive, ref } from "vue";
import { useSimulationSingleton } from "@/scripts/simulationSingleton.js";
import { onAgentsSelected } from "@/scripts/emitter.js";

const simulation = useSimulationSingleton();

const chart = ref(null);

const chartOptions = reactive({
  chart: {
    height: 250,
    type: "area",
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
  stroke: {
    curve: "smooth",
  },
  colors: ["#63e2b7", "#6381e2"],
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

const series = reactive([
  {
    name: "Achieved Utility",
    data: [],
  },
  {
    name: "Non-Colliding Utility",
    data: [],
  },
]);

const updateSeries = () => {
  const nonCollidingUtility = Array(simulation.maxTick + 1).fill(0);
  const utility = Array(simulation.maxTick + 1).fill(0);

  simulation.selectedAgents.forEach((agent) => {
    const arrivalTick = agent.veryLastTick;
    if (arrivalTick) {
      utility[arrivalTick] += agent.utility;
      nonCollidingUtility[arrivalTick] += agent.nonCollidingUtility;
    }
  });

  for (let i = 1; i <= simulation.maxTick; i++) {
    utility[i] = utility[i - 1] + utility[i];
    nonCollidingUtility[i] = nonCollidingUtility[i - 1] + nonCollidingUtility[i];
  }

  series[0].data = utility.map((y, x) => ({ x, y }));
  series[1].data = nonCollidingUtility.map((y, x) => ({ x, y }));
};

onAgentsSelected(() => {
  updateSeries();
});

updateSeries();
</script>

<style scoped></style>
