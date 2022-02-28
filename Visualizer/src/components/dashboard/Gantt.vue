<template>
  <vue-apex-charts
    type="rangeBar" height="250" :options="chartOptions" :series="series"
  />
</template>

<script setup>
import VueApexCharts from "vue3-apexcharts";

import {useSimulationStore} from "../../stores/simulation";
import {reactive} from "vue";

const simulationStore = useSimulationStore();

const chartOptions = {
  chart: {
    height: 250,
    type: 'rangeBar',
    background: 'transparent',
    toolbar: {show: false}
  },
  plotOptions: {
    bar: {
      horizontal: true,
      distributed: true,
    }
  },
  stroke: { show: false },
  grid: { show: false },
  yaxis: { show: false },
}

const series =  reactive([{
  name: 'Inflation',
  data: Array(simulationStore.dimensions.t).fill(0),
}])
</script>

<style scoped>

</style>
