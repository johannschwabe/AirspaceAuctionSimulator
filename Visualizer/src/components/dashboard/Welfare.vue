<template>
  <vue-apex-charts ref="chart" type="area" height="250" :options="chartOptions" :series="series" />
</template>

<script setup>
import VueApexCharts from "vue3-apexcharts";

import { reactive, ref } from "vue";
import { useSimulationSingleton } from "../../scripts/simulation";
import { onAgentsSelected, onTick } from "../../scripts/emitter";

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
  colors: ["#6381e2", "#63e2b7"],
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
    name: "Optimal Welfare",
    data: [],
  },
  {
    name: "Achieved Welfare",
    data: [],
  },
]);

const updateSeries = () => {
  console.log("Welfare: Update");
  const optimalWelfare = Array(simulation.maxTick + 1).fill(0);
  const achievedWelfare = Array(simulation.maxTick + 1).fill(0);

  simulation.selectedAgents.forEach((agent) => {
    const arrivalTick = agent.combinedPath.lastTick;
    optimalWelfare[arrivalTick] += agent.nonCollidingWelfare;
    achievedWelfare[arrivalTick] += agent.welfare;
    console.log({
      arrivalTick,
      ncw: agent.nonCollidingWelfare,
      w: agent.welfare,
    });
  });

  for (let i = 1; i <= simulation.maxTick; i++) {
    optimalWelfare[i] = optimalWelfare[i - 1] + optimalWelfare[i];
    achievedWelfare[i] = achievedWelfare[i - 1] + achievedWelfare[i];
  }

  series[0].data = optimalWelfare.map((y, x) => ({ x, y }));
  series[1].data = achievedWelfare.map((y, x) => ({ x, y }));
};


onAgentsSelected(() => {
  updateSeries();
});

updateSeries();

</script>

<style scoped></style>
