<template>
  <div>
    <boxplot
      title="Welfare"
      :color="simulation.ownerInFocus.color"
      :quantiles="simulation.ownerInFocus.welfareQuantiles"
      :outliers="simulation.ownerInFocus.welfareOutliers"
      :min="simulation.ownerInFocus.minWelfare"
      :max="simulation.ownerInFocus.maxWelfare"
    />
    <n-divider style="margin-top: 6px; margin-bottom: 6px" />
    <boxplot
      title="Bids"
      :color="simulation.ownerInFocus.color"
      :quantiles="simulation.ownerInFocus.bidQuantiles"
      :outliers="simulation.ownerInFocus.bidOutliers"
      :min="simulation.ownerInFocus.minBidValue"
      :max="simulation.ownerInFocus.maxBidValue"
    />
    <n-divider style="margin-top: 6px; margin-bottom: 6px" />
    <div v-for="datapoint in datapoints" :key="datapoint.label">
      <div style="display: flex">
        <div
          style="
            display: flex;
            flex-direction: column;
            justify-content: center;
            margin-right: 10px;
          "
        >
          <n-icon :component="datapoint.icon" :depth="5" size="25" />
        </div>
        <div>
          <div style="color: rgba(255, 255, 255, 0.52); font-size: 12px">
            {{ datapoint.label }}
          </div>
          <div>
            {{ datapoint.value }}
          </div>
        </div>
      </div>
      <n-divider style="margin-top: 6px; margin-bottom: 6px" />
    </div>
  </div>
</template>

<script setup>
import Boxplot from "./Boxplot.vue";
import { computed } from "vue";
import { FingerPrint, Airplane, Wallet, Timer } from "@vicons/ionicons5";
import { useSimulationSingleton } from "../../scripts/simulation";

const simulation = useSimulationSingleton();

const datapoints = computed(() =>
  [
    { label: "Owner ID", value: simulation.ownerInFocus.id, icon: FingerPrint },
    {
      label: "# Agents in Total",
      value: simulation.ownerInFocus.numberOfAgents,
      icon: Airplane,
    },
    simulation.ownerInFocus.numberOfABAgents && {
      label: "# AB Agents",
      value: simulation.ownerInFocus.numberOfABAgents,
      icon: Airplane,
    },
    simulation.ownerInFocus.numberOfABAAgents && {
      label: "# ABA Agents",
      value: simulation.ownerInFocus.numberOfABAAgents,
      icon: Airplane,
    },
    simulation.ownerInFocus.numberOfABCAgents && {
      label: "# ABC Agents",
      value: simulation.ownerInFocus.numberOfABCAgents,
      icon: Airplane,
    },
    simulation.ownerInFocus.numberOfStationaryAgents && {
      label: "# Stationary Agents",
      value: simulation.ownerInFocus.numberOfStationaryAgents,
      icon: Airplane,
    },
    {
      label: "Total Time in Air",
      value: simulation.ownerInFocus.totalTimeInAir,
      icon: Timer,
    },
    {
      label: "Total Bid Value",
      value: simulation.ownerInFocus.totalBidValue,
      icon: Wallet,
    },
  ].filter(Boolean)
);
</script>

<style scoped></style>
