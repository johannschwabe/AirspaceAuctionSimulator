<template>
  <n-page-header :subtitle="simulation.description" @back="() => router.push('/')">
    <n-grid :cols="8">
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
        <n-divider />
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
import { Cube, Stopwatch, FingerPrint, Fish, HappyOutline, GitBranch, CloudDownload, Skull } from "@vicons/ionicons5";
import Boxplot from "./PanelComponents/Boxplot.vue";

import { computed } from "vue";
import { useRouter } from "vue-router";

import { downloadSimulation } from "@/API/api.js";
import { useSimulationSingleton } from "@/scripts/simulationSingleton.js";
import { formatComputeTime } from "@/scripts/format";
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
      icon: FingerPrint,
    },
    {
      label: "Agents",
      value: simulation.statistics.totalNumberOfAgents,
      icon: Fish,
    },

    {
      label: "Total Value",
      value: Math.round(simulation.statistics.value.total * 100) / 100,
      icon: HappyOutline,
    },
    {
      label: "Total Non-Colliding Value",
      value: Math.round(simulation.statistics.totalNonCollidingValue * 100) / 100,
      icon: HappyOutline,
    },
    {
      label: "Mean Value",
      value: Math.round(simulation.statistics.value.mean * 100) / 100,
      icon: HappyOutline,
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
      value: simulation.agents.filter((a) => a.flyingTicks === 0).length,
      color: "info",
      icon: Fish,
    },
    {
      label: "Re-Allocations",
      value: simulation.agents.filter((a) => a.reAllocationTimesteps.length > 0).length,
      color: "warning",
      icon: Fish,
    },
    {
      label: "Violations",
      value: simulation.agents.filter((a) => a.totalViolations > 0).length,
      color: "error",
      icon: Fish,
    },
    {
      label: "Failed Allocations",
      value: simulation.agents.filter((a) => a.events.some((e) => e instanceof FailedAllocationEvent)).length,
      color: "error",
      icon: GitBranch,
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
</style>
