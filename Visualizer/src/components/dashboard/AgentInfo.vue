<template>
  <n-timeline>
    <n-timeline-item
      v-for="(event, i) in agentStore.events"
      :key="`${agentStore.id}-${i}`"
      v-bind="event"
    >
      <template #icon>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
          <path :d="event.icon" :fill="fillColor(event)" />
        </svg>
      </template>
    </n-timeline-item>
  </n-timeline>

  <n-divider />

  <div v-for="datapoint in datapoints" :key="datapoint.label">
    <div style="display: flex">
      <div
        style="
          display: flex;
          flex-direction: column;
          justify-content: center;
          margin-right: 10px;
        "
      >
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
import { useAgentStore } from "../../stores/agent";
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

const agentStore = useAgentStore();

const datapoints = computed(() => [
  { label: "Agent ID", value: agentStore.id, icon: FingerPrint },
  { label: "Owner ID", value: agentStore.owner_id, icon: FingerPrint },
  { label: "Type", value: agentStore.agent_type, icon: Airplane },
  { label: "Battery", value: agentStore.battery, icon: BatteryHalf },
  { label: "Bid", value: agentStore.bid, icon: Wallet },
  { label: "Speed", value: agentStore.speed, icon: Speedometer },
  { label: "Welfare", value: agentStore.welfare, icon: Happy },
  { label: "Time in Air", value: agentStore.time_in_air, icon: Timer },
  {
    label: "Near Field Radius",
    value: agentStore.near_radius,
    icon: InformationCircle,
  },
  {
    label: "Near Field Intersections",
    value: agentStore.near_field_intersections,
    icon: AlertCircle,
  },
  {
    label: "Near Field Violations",
    value: agentStore.near_field_violations,
    icon: RemoveCircle,
  },
  {
    label: "Far Field Radius",
    value: agentStore.far_radius,
    icon: InformationCircle,
  },
  {
    label: "Far Field Intersections",
    value: agentStore.far_field_intersections,
    icon: AlertCircle,
  },
  {
    label: "Far Field Violations",
    value: agentStore.far_field_violations,
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
