<template>
  <vue-apex-charts type="boxPlot" height="50" :options="chartOptions" :series="series" />
</template>

<script setup>
import VueApexCharts from "vue3-apexcharts";
import { lightenColor } from "@/scripts/color";
import { reactive } from "vue";

const props = defineProps({
  title: String,
  color: String,
  data: Object,
});

const chartOptions = {
  chart: {
    height: 50,
    type: "boxPlot",
    background: "transparent",
    toolbar: { show: false },
  },
  plotOptions: {
    bar: {
      horizontal: true,
    },
    boxPlot: {
      colors: {
        upper: lightenColor(props.color, 10),
        lower: props.color,
      },
    },
  },
  stroke: {
    colors: ["#8d8d8d"],
  },
  theme: {
    mode: "dark",
  },
  title: {
    show: false,
  },
  legend: {
    show: false,
  },
  grid: {
    show: false,
    padding: {
      top: -25,
    },
  },
  xaxis: {
    labels: { show: false },
    axisTicks: { show: false },
    axisBorder: {
      show: false,
    },
  },
};

const series = reactive([
  {
    type: "boxPlot",
    data: [
      {
        x: props.title,
        y: [props.data.min, ...props.data.quartiles, props.data.max],
      },
    ],
  },
]);
</script>

<style scoped></style>
