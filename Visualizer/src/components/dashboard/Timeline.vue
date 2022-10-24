<template>
  <div class="content">
    <div class="flex">
      <div class="flex">
        <n-button quaternary circle v-for="control in controls" @click="control.action">
          <template #icon>
            <n-icon :component="control.icon" />
          </template>
        </n-button>
        <n-input-number
          round
          size="small"
          :show-button="false"
          :min="0"
          :max="maxTick + 1"
          :value="currentTick"
          @update:value="updateTick"
          style="max-width: 50px"
        />
      </div>
      <div style="flex-grow: 1">
        <vue-apex-charts
          ref="timelineChart"
          type="bar"
          height="75"
          :options="agentChartOptions"
          :series="agentSeries"
          style="margin-left: 10px; margin-right: 10px"
        />
        <div style="margin-top: -30px">
          <vue-apex-charts
            ref="collisionsChart"
            type="bar"
            height="75"
            :options="eventChartOptions"
            :series="eventSeries"
          />
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
    </div>
  </div>
</template>

<script setup>
import VueApexCharts from "vue3-apexcharts";
import { reactive, ref, computed } from "vue";
import { debounce } from "lodash-es";

import { onAgentsSelected, onFocusOffAgent, onFocusOnAgent, onTick } from "@/scripts/emitter.js";
import { useSimulationSingleton } from "@/scripts/simulationSingleton.js";

import {
  PlayOutline,
  PauseOutline,
  PlaySkipForwardOutline,
  PlaySkipBackOutline,
  PlayBackOutline,
  PlayForwardOutline,
} from "@vicons/ionicons5";
import { FailedAllocationEvent, ReallocationEvent } from "@/SimulationObjects/FlightEvent.js";

const simulation = useSimulationSingleton();

const timelineChart = ref(null);

const maxTick = ref(simulation.maxTick);
const currentTick = ref(simulation.tick);

let interval;

const playing = ref(false);
const controls = computed(() => [
  {
    icon: PlaySkipBackOutline,
    action: firstTick,
  },
  {
    icon: PlayBackOutline,
    action: previousTick,
  },
  {
    icon: playing.value ? PauseOutline : PlayOutline,
    action: playing.value ? pause : play,
  },
  {
    icon: PlayForwardOutline,
    action: nextTick,
  },
  {
    icon: PlaySkipForwardOutline,
    action: lastTick,
  },
]);

const agentChartOptions = {
  chart: {
    height: 75,
    type: "bar",
    background: "transparent",
    toolbar: { show: false },
    zoom: { enabled: false },
    animations: { enabled: false },
  },
  plotOptions: {
    bar: {
      distributed: true, // this line is mandatory
    },
  },
  theme: {
    mode: "dark",
  },
  dataLabels: {
    enabled: false,
  },
  colors: getBaselineColor(),
  stroke: { show: false },
  grid: { show: false },
  legend: { show: false },
  xaxis: {
    min: 0,
    max: simulation.maxTick,
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
  colors: ["#942a2a", "#94762a", "#bd249a"],
  stroke: { show: false },
  grid: { show: false },
  legend: { show: false },
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
    name: "# Violations",
    data: simulation.timelineViolations.map((y, x) => ({ x, y: -y })),
  },
  {
    name: "# Reallocations",
    data: simulation.timelineReAllocations.map((y, x) => ({ x, y: -y })),
  },
  {
    name: "# Blocker violations",
    data: simulation.timelineBlockerViolations.map((y, x) => ({ x, y: -y })),
  },
]);

const updateAgentSeries = () => {
  agentSeries[0].data = simulation.timeline.map((y, x) => ({ x, y }));
};

const updateEventSeries = () => {
  eventSeries[0].data = simulation.timelineViolations.map((y, x) => ({ x, y: -y }));
  eventSeries[1].data = simulation.timelineReAllocations.map((y, x) => ({ x, y: -y }));
  eventSeries[2].data = simulation.timelineBlockerViolations.map((y, x) => ({ x, y: -y }));
};

const agentFocussedEventSeries = () => {
  const timelineViolations = Array(simulation.maxTick).fill(0);
  simulation.agentInFocus.violationsTimesteps.forEach((tick) => {
    timelineViolations[tick] += 1;
  });
  const timelineReAllocations = Array(simulation.maxTick).fill(0);
  simulation.agentInFocus.events.forEach((event) => {
    if (event instanceof ReallocationEvent || event instanceof FailedAllocationEvent) {
      timelineReAllocations[event.tick] += 1;
    }
  });
  const timelineBlockerViolations = Array(simulation.maxTick).fill(0);
  simulation.agentInFocus.blockerViolationsTimesteps.forEach((tick) => {
    timelineBlockerViolations[tick] += 1;
  });
  eventSeries[0].data = timelineViolations.map((y, x) => ({ x, y: -y }));
  eventSeries[1].data = timelineReAllocations.map((y, x) => ({ x, y: -y }));
  eventSeries[2].data = timelineBlockerViolations.map((y, x) => ({ x, y: -y }));
};

const setTick = debounce(
  () => {
    simulation.tick = currentTick.value;
  },
  10,
  { leading: false }
);

function updateTick(t) {
  currentTick.value = t;
  setTick();
}

function firstTick() {
  currentTick.value = 0;
  setTick();
}

function lastTick() {
  currentTick.value = simulation.maxTick - 1;
  setTick();
}

function previousTick() {
  if (currentTick.value >= 0) {
    currentTick.value = simulation.tick - 1;
    setTick();
  }
}

function nextTick() {
  if (currentTick.value < simulation.maxTick) {
    currentTick.value = simulation.tick + 1;
    setTick();
  }
}

function play() {
  playing.value = true;
  interval = setInterval(() => {
    nextTick();
    if (currentTick.value === simulation.maxTick) {
      pause();
    }
  }, 500);
}

function pause() {
  playing.value = false;
  clearInterval(interval);
}

onAgentsSelected(() => {
  maxTick.value = simulation.maxTick;
  updateAgentSeries();
  updateEventSeries();
});

function getTimelineColors(lightColor, darkColor) {
  return Array.from({ length: simulation.timeline.length }).map((_, i) => {
    if (simulation.agentInFocus)
      for (const element of simulation.agentInFocus.segmentsStartEnd) {
        const [start, end] = element;
        if (i > start && i < end) return lightColor;
      }
    return darkColor;
  });
}
function getBaselineColor() {
  return Array.from({ length: simulation.timeline.length }).map((_) => "#2a947d");
}

function updateChartColor() {
  timelineChart.value.updateOptions({
    colors: getTimelineColors("#2a947d", "#0f332a"),
  });
}
function baselineChartColor() {
  timelineChart.value.updateOptions({
    colors: getBaselineColor(),
  });
}
onTick(() => {
  currentTick.value = simulation.tick;
});
onFocusOnAgent(() => {
  updateChartColor();
  agentFocussedEventSeries();
});
onFocusOffAgent(() => {
  baselineChartColor();
  updateEventSeries();
});
</script>

<style scoped>
.flex {
  display: flex;
  flex-direction: row;
  align-items: end;
  justify-content: center;
}
</style>
