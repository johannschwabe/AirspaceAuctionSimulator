<template>
  <n-page-header
    :subtitle="simulationStore.description"
    @back="() => router.push('/')"
  >
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
        <n-breadcrumb-item @click="() => router.push('/')">
          Home
        </n-breadcrumb-item>
        <n-breadcrumb-item>{{ simulationStore.name }}</n-breadcrumb-item>
      </n-breadcrumb>
    </template>

    <template #title>
      <a href="#" style="text-decoration: none; color: inherit">
        {{ simulationStore.name }}
      </a>
    </template>

    <template #avatar>
      <n-avatar :src="logo" color="transparent" />
    </template>
  </n-page-header>
</template>

<script setup>
import logo from "../../assets/drone.png";
import {
  Cube,
  FingerPrint,
  Fish,
  HappyOutline,
  GitBranch,
  GitPullRequest,
} from "@vicons/ionicons5";

import { computed } from "vue";
import { useRouter } from "vue-router";
import { useSimulationStore } from "../../stores/simulation";

const router = useRouter();
const simulationStore = useSimulationStore();

const stats = computed(() => {
  return [
    {
      label: "Dimension X",
      value: simulationStore.dimensions.x,
      icon: Cube,
    },
    {
      label: "Dimension Y",
      value: simulationStore.dimensions.y,
      icon: Cube,
    },
    {
      label: "Dimension Z",
      value: simulationStore.dimensions.z,
      icon: Cube,
    },
    {
      label: "Owners",
      value: simulationStore.statistics.total_number_of_owners,
      icon: FingerPrint,
    },
    {
      label: "Agents",
      value: simulationStore.statistics.total_number_of_agents,
      icon: Fish,
    },
    {
      label: "Welfare",
      value: simulationStore.statistics.total_achieved_welfare,
      icon: HappyOutline,
    },
    {
      label: "Collisions",
      value: simulationStore.statistics.total_number_of_collisions,
      icon: GitPullRequest,
    },
    {
      label: "Re-Allocations",
      value: simulationStore.statistics.total_number_of_reallocations,
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
