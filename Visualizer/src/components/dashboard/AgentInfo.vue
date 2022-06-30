<template>
  <n-timeline>
    <n-timeline-item
      v-for="(event, i) in simulation.agentInFocus.events"
      :key="`${simulation.agentInFocus.id}-${i}`"
      v-bind="event"
    >
      <template #icon>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
          <path :d="event.icon" :fill="fillColor(event)" />
        </svg>
      </template>
    </n-timeline-item>
  </n-timeline>

  <n-divider style="margin-bottom: 6px" />

  <div v-for="datapoint in datapoints" :key="datapoint.label">
    <div style="display: flex">
      <div style="display: flex; flex-direction: column; justify-content: center; margin-right: 10px">
        <n-icon :component="datapoint.icon" :depth="5" size="25" />
      </div>
      <div>
        <div style="color: rgba(255, 255, 255, 0.52); font-size: 12px">
          {{ datapoint.label }}
        </div>
        <div>
          {{ datapoint.value }}
        </div>
      </div>
    </div>
    <n-divider style="margin-top: 6px; margin-bottom: 6px" />
  </div>
</template>

<script setup>
import { computed } from "vue";
import {
  FingerPrint,
  Airplane,
  BatteryHalf,
  Wallet,
  Speedometer,
  Happy,
  Timer,
  RemoveCircle,
  AlertCircle,
  InformationCircle,
} from "@vicons/ionicons5";
import { useSimulationSingleton } from "../../scripts/simulation";

const simulation = useSimulationSingleton();
const datapoints = computed(() => [
  { label: "Agent ID", value: simulation.agentInFocus.id, icon: FingerPrint },
  { label: "Type", value: simulation.agentInFocus.agentType, icon: Airplane },
  { label: "Battery", value: simulation.agentInFocus.battery, icon: BatteryHalf },
  ...Object.entries(simulation.agentInFocus.bid)
    .filter(([key, _]) => key !== "!value")
    .map(([key, value]) => {
      return {
        label: key,
        value: value,
        icon: Wallet,
      };
    }),
  { label: "Speed", value: simulation.agentInFocus.speed, icon: Speedometer },
  { label: "Welfare", value: simulation.agentInFocus.welfare, icon: Happy },
  { label: "Time in Air", value: simulation.agentInFocus.timeInAir, icon: Timer },
  {
    label: "Near Field Radius",
    value: simulation.agentInFocus.nearRadius,
    icon: InformationCircle,
  },
  {
    label: "Near Field Intersections",
    value: simulation.agentInFocus.nearFieldIntersections,
    icon: AlertCircle,
  },
  {
    label: "Near Field Violations",
    value: simulation.agentInFocus.nearFieldViolations,
    icon: RemoveCircle,
  },
  {
    label: "Far Field Radius",
    value: simulation.agentInFocus.farRadius,
    icon: InformationCircle,
  },
  {
    label: "Far Field Intersections",
    value: simulation.agentInFocus.farFieldIntersections,
    icon: AlertCircle,
  },
  {
    label: "Far Field Violations",
    value: simulation.agentInFocus.farFieldViolations,
    icon: RemoveCircle,
  },
]);

const fillColor = (event) => {
  return {
    default: "#a8a8a8",
    success: "#048a00",
    info: "#00408a",
    warning: "#cb7500",
    error: "#b90000",
  }[event.type];
};
</script>

<style scoped></style>
