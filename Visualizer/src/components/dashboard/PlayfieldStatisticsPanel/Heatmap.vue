<template>
  <vue-apex-charts type="heatmap" height="250" :options="chartOptions" :series="series" />
</template>

<script setup>
import VueApexCharts from "vue3-apexcharts";
import { reactive } from "vue";

import { useSimulationSingleton } from "@/scripts/simulationSingleton.js";
import { onAgentsSelected, onTick } from "@/scripts/emitter.js";

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
const dimXlength = (simulation.dimensions[props.dimX] + 1) / props.buckets;
const dimYlength = (simulation.dimensions[props.dimY] + 1) / props.buckets;

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
  simulation.activePathAgents.forEach((agent) => {
    const loc_dimx = agent.combinedPath.at(simulation.tick)[props.dimX];
    const loc_dimy = agent.combinedPath.at(simulation.tick)[props.dimY];
    const dim1 = Math.floor(loc_dimx / dimXlength);
    const dim2 = Math.floor(loc_dimy / dimYlength);
    series[dim2].data[dim1] += 1;
  });
  simulation.activeSpaceAgents.forEach((agent) => {
    agent.combinedSpace[simulation.tick].forEach(({ min, max }) => {
      for (let x = min[props.dimX]; x <= max[props.dimX]; x++) {
        for (let y = min[props.dimY]; y <= max[props.dimY]; y++) {
          const dim1 = Math.floor(x / dimXlength);
          const dim2 = Math.floor(y / dimYlength);
          if (dim2 >= series.length || dim1 >= series[0].data.length || dim2 < 0 || dim1 < 0) {
            continue;
          }
          series[dim2].data[dim1] += 1;
        }
      }
    });
  });
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
