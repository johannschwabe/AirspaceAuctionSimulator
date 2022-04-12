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
import { reactive } from "vue";
import { head, last } from "lodash-es";

import { useSimulationStore } from "../../stores/simulation";
import {useEmitter} from "../../scripts/emitter";

const simulationStore = useSimulationStore();
const emitter = useEmitter();

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

const series = reactive([
  {
    data: [],
  },
]);

const resetState = () => {
  series[0].data = [];
};

const updateState = () => {
  console.log("Welfare: Update State");
  simulationStore.selectedAgents.forEach((agent) => {
    agent.paths.forEach((path) => {
      const start = head(path.t);
      const end = last(path.t);
      series[0].data.push({
        x: agent.name,
        y: [start, end],
        fillColor: agent.owner_color,
      });
    });
  });
  console.log("Welfare: Done");
};

updateState();

emitter.on("new-agents-selected", () => {
  resetState();
  updateState();
});
</script>

<style scoped></style>
