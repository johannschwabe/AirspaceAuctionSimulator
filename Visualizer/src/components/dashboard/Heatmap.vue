<template>
  <vue-apex-charts
    type="heatmap" height="250" :options="chartOptions" :series="series"
  />
</template>

<script setup>
import VueApexCharts from "vue3-apexcharts";
import { reactive, ref } from "vue";

import { useSimulationStore } from "../../stores/simulation";

const props = defineProps({
  title: String,
  dimX: String,
  dimY: String,
  granularity: { type: Number, default: 10, required: false }
})

const simulationStore = useSimulationStore();

const axisColors = {
  x: 'red',
  y: 'green',
  z: 'blue',
}

const chartOptions = {
  chart: {
    height: 250,
    type: 'heatmap',
    background: 'transparent',
    toolbar: { show: false }
  },
  theme: {
    mode: 'dark'
  },
  title: {
    text: props.title,
  },
  dataLabels: {
    enabled: false
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
    }
  }
}

const series = reactive([]);

// Fill series with zeroes
const dimXlength = Math.floor(simulationStore.dimensions[props.dimX] / props.granularity);
const dimYlength = Math.floor(simulationStore.dimensions[props.dimY] / props.granularity);

for(let dimy = 0; dimy < dimYlength; dimy++) {
  series.push({
    name: `${dimy * props.granularity}`,
    data: Array(dimXlength).fill(0),
  })
}

simulationStore.owners.forEach((owner, i) => {
  owner.agents.forEach((agent) => {
    agent.locations.forEach((loc) => {
      const dim1 = Math.floor(loc[props.dimX] / props.granularity);
      const dim2 = Math.floor(loc[props.dimY] / props.granularity);
      console.log(dim1, dim2);
      series[dim2].data[dim1] += 1;
    })
  })
})
</script>

<style scoped>

</style>
