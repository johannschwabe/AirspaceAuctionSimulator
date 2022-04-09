<template>
  <div>
    <boxplot
      title="Welfare"
      :color="ownerStore.color"
      :quantiles="ownerStore.welfare_quantiles"
      :outliers="ownerStore.welfare_outliers"
      :min="ownerStore.min_welfare"
      :max="ownerStore.max_welfare"
    />
    <n-divider style="margin-top: 6px; margin-bottom: 6px" />
    <boxplot
      title="Bids"
      :color="ownerStore.color"
      :quantiles="ownerStore.bid_quantiles"
      :outliers="ownerStore.bid_outliers"
      :min="ownerStore.min_bid_value"
      :max="ownerStore.max_bid_value"
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
import { useOwnerStore } from "../../stores/owner";
import { FingerPrint, Airplane, Wallet, Timer } from "@vicons/ionicons5";

const ownerStore = useOwnerStore();

const datapoints = computed(() =>
  [
    { label: "Owner ID", value: ownerStore.id, icon: FingerPrint },
    {
      label: "# Agents in Total",
      value: ownerStore.number_of_agents,
      icon: Airplane,
    },
    ownerStore.number_of_ab_agents && {
      label: "# AB Agents",
      value: ownerStore.number_of_ab_agents,
      icon: Airplane,
    },
    ownerStore.number_of_aba_agents && {
      label: "# ABA Agents",
      value: ownerStore.number_of_aba_agents,
      icon: Airplane,
    },
    ownerStore.number_of_abc_agents && {
      label: "# ABC Agents",
      value: ownerStore.number_of_abc_agents,
      icon: Airplane,
    },
    ownerStore.number_of_stationary_agents && {
      label: "# Stationary Agents",
      value: ownerStore.number_of_stationary_agents,
      icon: Airplane,
    },
    {
      label: "Total Time in Air",
      value: ownerStore.total_time_in_air,
      icon: Timer,
    },
    {
      label: "Total Bid Value",
      value: ownerStore.total_bid_value,
      icon: Wallet,
    },
  ].filter(Boolean)
);
</script>

<style scoped></style>
