<template>
  <n-page-header :subtitle="simulation.description" @back="() => router.push('/')">
    <n-grid :cols="8" class="stats-grid">
      <n-gi v-for="stat in stats" :key="stat.label">
        <n-statistic :label="stat.label" tabular-nums>
          <template #prefix>
            <n-icon v-if="stat.icon" :component="stat.icon" :depth="5" size="20" />
          </template>
          <component :is="stat.component" v-if="stat.component" v-bind="stat.props"></component>
          <n-text :type="stat.color ?? 'default'" v-else>
            {{ stat.value }}
          </n-text>
        </n-statistic>
      </n-gi>
    </n-grid>

    <template #header>
      <n-breadcrumb>
        <n-breadcrumb-item @click="() => router.push('/')"> Home </n-breadcrumb-item>
        <n-breadcrumb-item>{{ simulation.name }}</n-breadcrumb-item>
      </n-breadcrumb>
    </template>

    <template #title>
      <a href="#" style="text-decoration: none; color: inherit">
        {{ simulation.name }}
      </a>
    </template>

    <template #avatar>
      <n-avatar :src="logo" color="transparent" />
    </template>

    <template #extra>
      <n-button icon-placement="right" style="margin-right: 15px" @click="downloadSimulation">
        <template #icon>
          <n-icon>
            <cloud-download />
          </n-icon>
        </template>
        Download
      </n-button>
    </template>
  </n-page-header>
</template>

<script setup>
import logo from "../../assets/drone.png";
import {
  Cube,
  HappyOutline,
  GitBranch,
  CloudDownload,
  Home,
  Ban,
  HandRight,
  Pricetag,
  Skull,
  Airplane,
} from "@vicons/ionicons5";
import Boxplot from "./PanelComponents/Boxplot.vue";

import { computed } from "vue";
import { useRouter } from "vue-router";

import { downloadSimulation } from "@/API/api.js";
import { useSimulationSingleton } from "@/scripts/simulationSingleton.js";
import { FailedAllocationEvent } from "@/SimulationObjects/FlightEvent";

const router = useRouter();
const simulation = useSimulationSingleton();

const dim = computed(() => {
  const { x, y, z } = simulation.dimensions;
  return `${x.toFixed(0)}/${y.toFixed(0)}/${z.toFixed(0)}`;
});

const stats = computed(() => {
  return [
    {
      label: "Dimensions",
      value: dim.value,
      icon: Cube,
    },
    {
      label: "Timesteps",
      value: simulation.maxTick,
      icon: Cube,
    },
    {
      label: "Owners",
      value: simulation.statistics.totalNumberOfOwners,
      icon: Home,
    },
    {
      label: "Agents",
      value: simulation.statistics.totalNumberOfAgents,
      icon: Airplane,
    },

    {
      label: "Total Value",
      value: Math.round(simulation.statistics.value.total * 100) / 100,
      icon: Pricetag,
    },
    {
      label: "Total Non-Colliding Value",
      value: Math.round(simulation.statistics.totalNonCollidingValue * 100) / 100,
      icon: Pricetag,
    },
    {
      label: "Mean Value",
      value: Math.round(simulation.statistics.value.mean * 100) / 100,
      icon: Pricetag,
    },
    {
      label: "Value Boxplot",
      component: Boxplot,
      props: {
        title: "",
        color: "#2a947d",
        data: simulation.statistics.value,
      },
    },

    {
      label: "No-Starts",
      value: simulation.agents.filter((a) => a.flyingTicks.length === 0).length,
      color: "info",
      icon: HandRight,
    },
    {
      label: "Reallocations",
      value: simulation.agents.filter((a) => a.reAllocationTimesteps.length > 0).length,
      color: "warning",
      icon: GitBranch,
    },
    {
      label: "Violations",
      value: simulation.agents.filter((a) => a.totalViolations > 0).length,
      color: "error",
      icon: Skull,
    },
    {
      label: "Failed Allocations",
      value: simulation.agents.filter(
        (a) => a.events.some((e) => e instanceof FailedAllocationEvent) && a.time_in_air > 0
      ).length,
      icon: Ban,
    },

    {
      label: "Total Utility",
      value: Math.round(simulation.statistics.utility.total * 100) / 100,
      icon: HappyOutline,
    },
    {
      label: "Total Non-Colliding Utility",
      value: Math.round(simulation.statistics.totalNonCollidingUtility * 100) / 100,
      icon: HappyOutline,
    },
    {
      label: "Mean Utility",
      value: Math.round(simulation.statistics.utility.mean * 100) / 100,
      icon: HappyOutline,
    },
    {
      label: "Utility Boxplot",
      component: Boxplot,
      props: {
        title: "",
        color: "#2a947d",
        data: simulation.statistics.utility,
      },
    },
  ];
});
</script>

<style scoped>
.topbar {
  display: flex;
  flex-direction: row;
}
.stats-grid > div {
  overflow: hidden;
  max-height: 80px;
  position: relative;
}
.stats-grid > div:nth-child(-n + 8) {
  border-bottom: 1px solid rgba(255, 255, 255, 0.09);
  margin-top: 5px;
}
.stats-grid > div:nth-child(n + 9) {
  padding-top: 10px;
}
.stats-grid > div:nth-child(4)::after,
.stats-grid > div:nth-child(12)::after {
  content: " ";
  height: 100px;
  width: 1px;
  position: absolute;
  right: 20px;
  top: -5px;
  background-color: rgba(255, 255, 255, 0.09);
}
</style>
