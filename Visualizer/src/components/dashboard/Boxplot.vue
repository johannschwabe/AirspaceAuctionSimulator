<template>
  <vue-apex-charts type="boxPlot" height="100" :options="chartOptions" :series="series" />
</template>

<script setup>
import VueApexCharts from "vue3-apexcharts";
import { lightenColor } from "@/scripts/color";
import { reactive } from "vue";

const props = defineProps({
  title: String,
  color: String,
  quantiles: Array,
  outliers: Array,
  min: Number,
  max: Number,
});

const chartOptions = {
  chart: {
    height: 100,
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
  grid: { show: false },
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
        y: [props.min, ...props.quantiles, props.max],
      },
    ],
  },
  // {
  //   type: "scatter",
  //   data: props.outliers.map((outlier) => ({ x: props.title, y: outlier })),
  // },
]);
</script>

<style scoped></style>
