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
</template>

<script setup>
import { useAgentStore } from "../../stores/agent";

const agentStore = useAgentStore();

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
