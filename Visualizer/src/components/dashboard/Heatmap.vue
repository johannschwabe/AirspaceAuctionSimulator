<template>
  <vue-apex-charts type="heatmap" height="250" :options="chartOptions" :series="series" />
</template>

<script setup>
import VueApexCharts from "vue3-apexcharts";
import { reactive } from "vue";

import { useSimulationSingleton } from "../../scripts/simulation";
import { onAgentsSelected, onTick } from "../../scripts/emitter";

const props = defineProps({
  title: String,
  dimX: String,
  dimY: String,
  buckets: { type: Number, default: 10, required: false },
});

const simulation = useSimulationSingleton();

const axisColors = {
  x: "red",
  y: "green",
  z: "blue",
};

const chartOptions = {
  chart: {
    height: 250,
    type: "heatmap",
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
  colors: ["#2a947d"],
  stroke: { show: false },
  heatmap: {
    radius: -1,
  },
  grid: { show: false },
  xaxis: {
    title: {
      text: props.dimX,
      offsetY: -15,
    },
    labels: { show: false },
    axisTicks: { show: false },
    axisBorder: {
      show: true,
      color: axisColors[props.dimX],
    },
  },
  yaxis: {
    title: {
      text: props.dimY,
      rotate: 0,
      offsetX: 15,
    },
    labels: { show: false },
    axisTicks: { show: false },
    axisBorder: {
      show: true,
      color: axisColors[props.dimY],
    },
  },
};

const series = reactive([]);

// Fill series with zeroes
const dimXlength = simulation.dimensions[props.dimX] / props.buckets;
const dimYlength = simulation.dimensions[props.dimY] / props.buckets;

for (let bucket = 0; bucket < props.buckets; bucket++) {
  series.push({
    name: `${Math.floor(bucket * dimXlength)}`,
    data: Array(props.buckets).fill(0),
  });
}

const resetState = () => {
  for (let bucket = 0; bucket < props.buckets; bucket++) {
    series[bucket].data = Array(props.buckets).fill(0);
  }
};

const updateState = () => {
  console.log("Heatmap: Update state");
  simulation.activeAgents.forEach((agent) => {
    const loc_dimx = agent.combinedPath.at(simulation.tick)[props.dimX];
    const loc_dimy = agent.combinedPath.at(simulation.tick)[props.dimY];
    const dim1 = Math.floor(loc_dimx / dimXlength);
    const dim2 = Math.floor(loc_dimy / dimYlength);
    series[dim2].data[dim1] += 1;
  });
  console.log("Heatmap: Done");
};

updateState();

onTick(() => {
  resetState();
  updateState();
});

onAgentsSelected(() => {
  resetState();
  updateState();
});
</script>

<style scoped></style>
