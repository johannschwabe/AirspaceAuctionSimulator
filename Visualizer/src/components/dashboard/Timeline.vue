<template>
  <div>
    <vue-apex-charts
      type="bar"
      height="75"
      :options="chartOptions"
      :series="series"
    />
    <div style="padding: 0 15px 0 35px; margin-top: -30px">
      <n-slider
        :value="simulationStore.tick"
        @update:value="(t) => simulationStore.updateTick(t)"
        :min="1"
        :max="simulationStore.dimensions.t"
        show-tooltip
        placement="bottom"
      />
    </div>
  </div>
</template>

<script setup>
import VueApexCharts from "vue3-apexcharts";
import { reactive } from "vue";

import { useSimulationStore } from "../../stores/simulation";
import { useEmitter } from "../../scripts/emitter";

const simulationStore = useSimulationStore();
const emitter = useEmitter();

const chartOptions = {
  chart: {
    height: 75,
    type: "bar",
    background: "transparent",
    toolbar: { show: false },
  },
  theme: {
    mode: "dark",
  },
  dataLabels: {
    enabled: false,
  },
  colors: ["#2a947d"],
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
    name: "# Active Agents",
    data: simulationStore.timeline,
  },
]);

emitter.on("new-agents-selected", () => {
  series[0].data = simulationStore.timeline;
});
</script>

<style scoped></style>
