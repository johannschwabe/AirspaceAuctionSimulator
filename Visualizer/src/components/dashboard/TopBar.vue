<template>
  <n-page-header :subtitle="description" @back="() => router.push('/')">
    <n-grid :cols="stats.length">
      <n-gi v-for="stat in stats" :key="stat.label">
        <n-statistic :label="stat.label" tabular-nums>
          <template #prefix>
            <n-icon :component="stat.icon" :depth="5" size="20" />
          </template>
          <n-number-animation
            ref="numberAnimationInstRef"
            :from="0.0"
            :to="stat.value"
            :active="true"
            :duration="stat.animate ?? true ? 3000 : 0"
            :precision="0 ?? stat.precision"
          />
        </n-statistic>
      </n-gi>
    </n-grid>

    <template #header>
      <n-breadcrumb>
        <n-breadcrumb-item>Home</n-breadcrumb-item>
        <n-breadcrumb-item>{{ name }}</n-breadcrumb-item>
      </n-breadcrumb>
    </template>

    <template #title>
      <a href="#" style="text-decoration: none; color: inherit">
        {{ name }}
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

const router = useRouter();

const props = defineProps({
  name: String,
  description: String,
  dimensionX: Number,
  dimensionY: Number,
  dimensionZ: Number,
  nOwners: Number,
  nAgents: Number,
  achievedWelfare: Number,
  nCollisions: Number,
  nReallocations: Number,
});

const stats = computed(() => {
  return [
    {
      label: "Dimension X",
      value: props.dimensionX,
      icon: Cube,
      animate: false,
    },
    {
      label: "Dimension Y",
      value: props.dimensionY,
      icon: Cube,
      animate: false,
    },
    {
      label: "Dimension Z",
      value: props.dimensionZ,
      icon: Cube,
      animate: false,
    },
    { label: "Owners", value: props.nOwners, icon: FingerPrint },
    { label: "Agents", value: props.nAgents, icon: Fish },
    {
      label: "Welfare",
      value: props.achievedWelfare,
      precision: 2,
      icon: HappyOutline,
    },
    {
      label: "Collisions",
      value: props.nCollisions,
      icon: GitPullRequest,
    },
    {
      label: "Re-Allocations",
      value: props.nReallocations,
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
