<template>
  <n-page-header :subtitle="simulation.description" @back="() => router.push('/')">
    <n-grid :cols="stats.length">
      <n-gi v-for="stat in stats" :key="stat.label">
        <n-statistic :label="stat.label" tabular-nums>
          <template #prefix>
            <n-icon :component="stat.icon" :depth="5" size="20" />
          </template>
          {{ stat.value }}
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
            <cloud-download-outline />
          </n-icon>
        </template>
        Download
      </n-button>
    </template>
  </n-page-header>
</template>

<script setup>
import logo from "../../assets/drone.png";
import { Cube, FingerPrint, Fish, HappyOutline, GitBranch, CloudDownloadOutline, Skull } from "@vicons/ionicons5";

import { computed } from "vue";
import { useRouter } from "vue-router";

import { downloadSimulation } from "@/API/api.js";
import { useSimulationSingleton } from "@/scripts/simulationSingleton.js";

const router = useRouter();
const simulation = useSimulationSingleton();

const dim = computed(() => {
  const { x, y, z } = simulation.dimensions;
  return `${x.toFixed(1)}/${y.toFixed(1)}/${z.toFixed(1)}`;
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
      value: simulation.dimensions.t,
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
      label: "Re-Allocations",
      value: simulation.statistics.totalNumberOfReallocations,
      icon: GitBranch,
    },
    {
      label: "Violations",
      value: simulation.statistics.totalNumberOfViolations,
      icon: Skull,
    },
    {
      label: "Utility",
      value: Math.round(simulation.statistics.totalValue * 100) / 100,
      icon: HappyOutline,
    },
    {
      label: "Non-Colliding Utility",
      value: Math.round(simulation.statistics.totalNonCollidingValue * 100) / 100,
      icon: HappyOutline,
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
