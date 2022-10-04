<template>
  <div
    style="color: rgba(255, 255, 255, 0.52); font-size: 12px; padding-left: 35px;"
  >{{ label }}</div>
  <vue-apex-charts ref="chart" type="area" height="150" :options="chartOptions" :series="series" />
</template>

<script setup>
import VueApexCharts from "vue3-apexcharts";
import { reactive } from "vue";

const props = defineProps({
  label: { type: String, required: false },
  color: { type: String, required: false, default: "#6381e2" },
  data: { type: Array, required: true },
});

const chartOptions = reactive({
  chart: {
    height: 150,
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
  colors: [props.color],
  xaxis: {
    labels: { show: false },
    axisTicks: { show: false },
    axisBorder: { show: false },
  },
});

const series = reactive([
  {
    name: "Height profile",
    data: props.data,
  },
]);
</script>

<style scoped></style>
