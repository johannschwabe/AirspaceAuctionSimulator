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
  </n-page-header>
</template>

<script setup>
import logo from "../../assets/drone.png";
import { Cube, FingerPrint, Fish, HappyOutline, GitBranch, GitPullRequest } from "@vicons/ionicons5";

import { computed } from "vue";
import { useRouter } from "vue-router";
import { useSimulationSingleton } from "../../scripts/simulation";

const router = useRouter();
const simulation = useSimulationSingleton();

const stats = computed(() => {
  return [
    {
      label: "Dimension X",
      value: simulation.dimensions.x,
      icon: Cube,
    },
    {
      label: "Dimension Y",
      value: simulation.dimensions.y,
      icon: Cube,
    },
    {
      label: "Dimension Z",
      value: simulation.dimensions.z,
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
      label: "Welfare",
      value: simulation.statistics.totalAchievedWelfare,
      icon: HappyOutline,
    },
    {
      label: "Collisions",
      value: simulation.statistics.totalNumberOfCollisions,
      icon: GitPullRequest,
    },
    {
      label: "Re-Allocations",
      value: simulation.statistics.totalNumberOfReallocations,
      icon: GitBranch,
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
