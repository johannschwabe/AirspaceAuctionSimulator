<template>
  <div>
    <vue-apex-charts type="bar" height="75" :options="agentChartOptions" :series="agentSeries" />
    <div style="margin-top: -30px">
      <vue-apex-charts type="bar" height="75" :options="eventChartOptions" :series="eventSeries" />
    </div>
    <div style="padding: 0 15px 0 35px; margin-top: -85px; z-index: 100000">
      <n-slider
        :value="currentTick"
        @update:value="updateTick"
        :min="0"
        :max="maxTick"
        show-tooltip
        placement="bottom"
      />
    </div>
  </div>
</template>

<script setup>
import VueApexCharts from "vue3-apexcharts";
import { reactive, ref } from "vue";

import { onAgentsSelected } from "../../scripts/emitter";
import { useSimulationSingleton } from "../../scripts/simulation";
import { debounce } from "lodash-es";
const simulation = useSimulationSingleton();

const maxTick = ref(simulation.maxTick - 1);

const currentTick = ref(simulation.tick);

const agentChartOptions = {
  chart: {
    height: 75,
    type: "bar",
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

const eventChartOptions = {
  chart: {
    height: 75,
    type: "bar",
    stacked: true,
    background: "transparent",
    toolbar: { show: false },
    zoom: { enabled: false },
    animations: { enabled: false },
  },
  legend: {
    show: false,
  },
  theme: {
    mode: "dark",
  },
  dataLabels: {
    enabled: false,
  },
  tooltip: {
    y: {
      formatter: (t) => Math.abs(t),
    },
  },
  colors: ["#942a2a", "#94762a"],
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

const agentSeries = reactive([
  {
    name: "# Active Agents",
    data: simulation.timeline.map((y, x) => ({ x, y })),
  },
]);

const eventSeries = reactive([
  {
    name: "# Collisions",
    data: simulation.timeline.map((y, x) => ({ x, y: -Math.floor(y / 5) })),
  },
  {
    name: "# Reallocations",
    data: simulation.timeline.map((y, x) => ({ x, y: -Math.floor(y / 4) })),
  },
]);

const updateAgentSeries = () => {
  agentSeries[0].data = simulation.timeline.map((y, x) => ({ x, y }));
};

const updateEventSeries = () => {
  eventSeries[0].data = simulation.timeline.map((y, x) => ({ x, y: -y }));
  eventSeries[1].data = simulation.timeline.map((y, x) => ({ x, y: -y }));
};

function updateTick(t) {
  currentTick.value = t;
  setTick();
}
const setTick = debounce(
  () => {
    simulation.tick = currentTick.value;
  },
  10,
  { leading: false }
);

onAgentsSelected(() => {
  maxTick.value = simulation.maxTick;
  updateAgentSeries();
  updateEventSeries();
});
</script>

<style scoped></style>
