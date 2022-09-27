<template>
  <div id="owner-drawer-container">
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
    <h3 v-if="!simulationConfig.isEmpty && locations.length > 0">Stops</h3>
    <template v-for="(location, index) in locations" :key="index">
      <component
        :is="componentMap[location.type]"
        :location="location"
        :width="180"
        :locationIndex="index"
        :owner-index="ownerIndex"
        subselection
        disabled
      >
        <p>Map type: {{ location.type }}</p>
      </component>
      <n-divider style="margin-top: 6px; margin-bottom: 6px" />
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted } from "vue";
import { FingerPrint, Airplane, Timer, Happy, Accessibility, } from "@vicons/ionicons5";
import { isArray, isNull, isUndefined } from "lodash-es";
import PerfectScrollbar from "perfect-scrollbar";

import { useSimulationSingleton } from "@/scripts/simulationSingleton.js";
import { useSimulationConfigStore } from "@/stores/simulationConfigStore.js";
import { useComponentMappingWithRandomMap } from "@/components/common/help/map/Map.js";

import Boxplot from "./PanelComponents/Boxplot.vue";
import SimpleDataTable from "@/components/dashboard/PanelComponents/SimpleDataTable.vue";

const simulation = useSimulationSingleton();
const simulationConfig = useSimulationConfigStore();

const componentMap = useComponentMappingWithRandomMap();

let ownerScroller;
onMounted(() => {
  const container = document.querySelector("#owner-drawer-container");
  ownerScroller = new PerfectScrollbar(container);
});
onUnmounted(() => {
  ownerScroller.destroy();
  ownerScroller = null;
});

const owner = computed(() => {
  return simulationConfig.owners.find((o) => o.name === simulation.ownerInFocus.name);
});

const ownerIndex = computed(() => {
  return simulationConfig.owners.findIndex((o) => o.name === simulation.ownerInFocus.name);
});

const locations = computed(() => {
  return owner.value?.locations || [];
});

const datapoints = computed(() =>
  [
    {
      label: "Owner ID",
      value: simulation.ownerInFocus.id,
      icon: FingerPrint,
    },
    {
      label: "Owner Name",
      value: simulation.ownerInFocus.name,
      icon: Accessibility,
    },
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
  ].filter((d) => !isUndefined(d.value) && !isNull(d.value) && (!isArray(d.value) || d.value.length > 0))
);
</script>

<style scoped>
#owner-drawer-container {
  position: relative;
  height: 950px;
  width: 200px;
  padding-right: 24px;
  overflow: hidden;
}
</style>
