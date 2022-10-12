<template>
  <n-h2 style="padding-left: 50px">Gannt Chart</n-h2>
  <div class="gant-container">
    <vue-apex-charts
      ref="ganttChart"
      type="rangeBar"
      height="250"
      :options="chartOptions"
      :series="series"
      @dataPointSelection="dataPointSelection"
      @dataPointMouseEnter="dataPointMouseEnter"
    />
  </div>
</template>

<script setup>
import VueApexCharts from "vue3-apexcharts";
import { nextTick, onMounted, ref } from "vue";

import { useSimulationSingleton } from "@/scripts/simulationSingleton.js";
import { onAgentsSelected, onFocusOffAgent, onFocusOnAgent } from "@/scripts/emitter.js";

const simulation = useSimulationSingleton();

const ganttChart = ref(null);

const chartOptions = {
  chart: {
    height: 250,
    type: "rangeBar",
    background: "transparent",
    toolbar: { show: false },
    zoom: { enabled: false },
    animations: { enabled: false },
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
  tooltip: {
    shared: false,
    x: {
      formatter: (val) => {
        return `Tick ${val}`;
      },
    },
    y: {
      formatter: (val) => {
        return `Agent ${val}`;
      },
    },
  },
  // stroke: { show: false },
  grid: { show: false },
  xaxis: {
    min: 0,
    max: simulation.maxTick,
    axisBorder: {
      color: "rgba(255, 255, 255, 0.09)",
    },
    axisTicks: {
      color: "rgba(255, 255, 255, 0.09)",
    },
    labels: {
      style: {
        colors: "rgba(255, 255, 255, 0.19)",
      },
    },
  },
  yaxis: {
    labels: { show: false },
    axisTicks: { show: false },
    axisBorder: { show: false },
  },
};

const series = [
  {
    data: [],
  },
];

function dataPointSelection(event, chartContext, config) {
  const { dataPointIndex } = config;
  const agentId = chartContext.data.twoDSeriesX[dataPointIndex];
  const agent = simulation.agents.find((a) => a.id === agentId);
  simulation.focusOnAgent(agent);
}

function dataPointMouseEnter(event) {
  event.target.style.cursor = "pointer";
}

const updateSeries = (noFocus = false) => {
  const gantt = [];
  simulation.selectedAgents.forEach((agent) => {
    agent.segmentsStartEnd.forEach(([start, end]) => {
      gantt.push({
        x: agent.id,
        y: [start, end],
        fillColor:
          noFocus || !simulation.agentInFocus || simulation.agentInFocus?.id === agent.id ? agent.color : "#5b5b5b",
      });
    });
  });
  ganttChart.value.updateSeries([{ data: gantt }]);
};

onAgentsSelected(() => {
  updateSeries();
});
onFocusOnAgent(() => {
  updateSeries();
});
onFocusOffAgent(() => {
  updateSeries(true);
});

onMounted(() => {
  nextTick(() => {
    updateSeries();
  });
});
</script>

<style scoped>
.gant-container {
  margin-left: 215px;
  margin-right: -15px;
}
</style>
