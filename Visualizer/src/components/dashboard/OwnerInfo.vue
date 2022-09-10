<template>
  <boxplot
    title="Utility"
    :color="simulation.ownerInFocus.color"
    :quartiles="simulation.ownerInFocus.utilityQuartiles"
    :outliers="simulation.ownerInFocus.utilityOutliers"
    :min="simulation.ownerInFocus.minUtility"
    :max="simulation.ownerInFocus.maxUtility"
  />
  <boxplot
    title="Non-Colliding Utility"
    :color="simulation.ownerInFocus.color"
    :quartiles="simulation.ownerInFocus.nonCollidingUtilityQuartiles"
    :outliers="simulation.ownerInFocus.nonCollidingUtilityOutliers"
    :min="simulation.ownerInFocus.minNonCollidingUtility"
    :max="simulation.ownerInFocus.maxNonCollidingUtility"
  />
  <n-divider style="margin-top: 6px; margin-bottom: 6px" />
  <simple-data-table title="General Info" :datapoints="datapoints" />
  <h3 v-if="!simulationConfig.isEmpty">Stops</h3>
  <template v-for="(location, index) in locations" :key="index">
    <component :is="componentMap[location.type]" :location="location" :size="200" disabled />
    <n-divider style="margin-top: 6px; margin-bottom: 6px" />
  </template>
</template>

<script setup>
import Boxplot from "./Boxplot.vue";
import { computed } from "vue";
import { FingerPrint, Airplane, Timer, Happy } from "@vicons/ionicons5";

import { useSimulationSingleton } from "@/scripts/simulation";
import { useSimulationConfigStore } from "@/stores/simulationConfig";
import { useComponentMapping } from "@/components/home/map/Map";
import SimpleDataTable from "@/components/dashboard/SimpleDataTable.vue";

const simulation = useSimulationSingleton();
const simulationConfig = useSimulationConfigStore();

const componentMap = useComponentMapping();

const owner = computed(() => {
  return simulationConfig.owners.find((o) => o.id === simulation.ownerInFocus.id);
});

const locations = computed(() => {
  return owner.value?.locations || [];
});

const datapoints = computed(() =>
  [
    { label: "Owner ID", value: simulation.ownerInFocus.id, icon: FingerPrint },
    {
      label: "Utility",
      value: simulation.ownerInFocus.totalUtility,
      icon: Happy,
    },
    {
      label: "Non-Colliding Utility",
      value: simulation.ownerInFocus.totalNonCollidingUtility,
      icon: Happy,
    },
    {
      label: "# Agents in Total",
      value: simulation.ownerInFocus.numberOfAgents,
      icon: Airplane,
    },
    {
      label: `# Agents in Air (Tick ${simulation.tick})`,
      value: simulation.ownerInFocus.agents.filter((a) => a.isActiveAtTick(simulation.tick)).length,
      icon: Airplane,
    },
    {
      label: "Total Time in Air",
      value: simulation.ownerInFocus.totalTimeInAir,
      icon: Timer,
    },
  ].filter(Boolean)
);
</script>

<style scoped></style>
