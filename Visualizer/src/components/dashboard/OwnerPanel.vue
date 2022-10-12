<template>
  <div id="owner-drawer-container">
    <boxplot title="Value" :color="simulation.ownerInFocus.color" :data="simulation.ownerInFocus.valueStatistics" />
    <boxplot title="Utility" :color="simulation.ownerInFocus.color" :data="simulation.ownerInFocus.utilityStatistics" />
    <boxplot title="Payment" :color="simulation.ownerInFocus.color" :data="simulation.ownerInFocus.paymentStatistics" />
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
import {
  FingerPrint,
  Airplane,
  Timer,
  Happy,
  Accessibility,
  Pricetag,
  GitBranch,
  Ban,
  Cash,
  Skull,
  HandRight,
  ColorPalette,
} from "@vicons/ionicons5";
import { isArray, isNull, isUndefined } from "lodash-es";
import PerfectScrollbar from "perfect-scrollbar";

import { useSimulationSingleton } from "@/scripts/simulationSingleton.js";
import { useSimulationConfigStore } from "@/stores/simulationConfigStore.js";
import { useComponentMappingWithRandomMap } from "@/components/common/map/Map.js";

import Boxplot from "./PanelComponents/Boxplot.vue";
import SimpleDataTable from "@/components/dashboard/PanelComponents/SimpleDataTable.vue";
import { FailedAllocationEvent } from "@/SimulationObjects/FlightEvent";

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
      label: "Owner Color",
      value: simulation.ownerInFocus.color,
      icon: ColorPalette,
    },
    {
      label: "Total Value",
      value: simulation.ownerInFocus.valueStatistics.total,
      icon: Pricetag,
    },
    {
      label: "Total Non-Colliding Value",
      value: simulation.ownerInFocus.nonCollidingValueStatistics.total,
      icon: Pricetag,
    },
    {
      label: "Total Utility",
      value: simulation.ownerInFocus.utilityStatistics.total,
      icon: Happy,
    },
    {
      label: "Total Non-Colliding Utility",
      value: simulation.ownerInFocus.nonCollidingUtilityStatistics.total,
      icon: Happy,
    },
    {
      label: "Total Payment",
      value: simulation.ownerInFocus.paymentStatistics.total,
      icon: Cash,
    },
    {
      label: "Agents in Total",
      value: simulation.ownerInFocus.numberOfAgents,
      icon: Airplane,
    },
    {
      label: `Agents in Air (Tick ${simulation.tick})`,
      value: simulation.ownerInFocus.agents.filter((a) => a.isActiveAtTick(simulation.tick)).length,
      icon: Airplane,
    },
    {
      label: "Agents with No-Starts",
      value: simulation.ownerInFocus.agents.filter((a) => a.flyingTicks.length === 0).length,
      color: "info",
      icon: HandRight,
    },
    {
      label: "Agents with Reallocation",
      value: simulation.ownerInFocus.agents.filter((a) => a.reAllocationTimesteps.length > 0).length,
      color: "warning",
      icon: GitBranch,
    },
    {
      label: "Agents with Failed Allocation",
      value: simulation.ownerInFocus.agents.filter((a) => a.events.some((e) => e instanceof FailedAllocationEvent))
        .length,
      color: "error",
      icon: Ban,
    },
    {
      label: "Agents with Violations",
      value: simulation.ownerInFocus.agents.filter((a) => a.totalViolations > 0).length,
      color: "error",
      icon: Skull,
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
