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
import { head, last } from "lodash-es";

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
    name: "Optimal Welfare",
    data: Array(simulationStore.dimensions.t).fill(0),
  },
  {
    name: "Achieved Welfare",
    data: Array(simulationStore.dimensions.t).fill(0),
  },
]);

const updateSeries = () => {
  console.log("Update series");
  series[0].data = Array(simulationStore.dimensions.t).fill(0);
  series[1].data = Array(simulationStore.dimensions.t).fill(0);

  simulationStore.selectedAgents.forEach((agent) => {
    if (agent.paths.length > 0) {
      const lastPath = head(agent.paths); // TODO change to last
      const arrivalTick = head(lastPath.t); // TODO change to last
      if (arrivalTick <= simulationStore.dimensions.t) {
        series[0].data[arrivalTick] += agent.non_colliding_welfare;
        series[1].data[arrivalTick] += agent.welfare;
      }
    }
  });

  for (let i = 1; i < simulationStore.dimensions.t; i++) {
    series[0].data[i] = series[0].data[i - 1] + series[0].data[i];
    series[1].data[i] = series[1].data[i - 1] + series[1].data[i];
  }
};

simulationStore.$subscribe(() => {
  updateSeries();
});

updateSeries();
</script>

<style scoped></style>
