import { defineStore } from "pinia";
import { useStorage } from "@vueuse/core";

export const useOwnerStore = defineStore({
  id: "owner",
  state: () => ({
    selected: false,
    id: useStorage("owner-id", -1),
    name: useStorage("owner-name", "unknown"),
    color: useStorage("owner-color", ""),
    agents: useStorage("owner-agents", []),
    total_time_in_air: useStorage("owner-total-time-in-air", -1),
    total_bid_value: useStorage("owner-total-bid-value", -1),
    mean_bid_value: useStorage("owner-mean-bid-value", -1),
    median_bid_value: useStorage("owner-median-bid-value", -1),
    max_bid_value: useStorage("owner-max-bid-value", -1),
    min_bid_value: useStorage("owner-min-bid-value", -1),
    bid_quantiles: useStorage("owner-bid-quantiles", []),
    bid_outliers: useStorage("owner-bid-outliers", []),
    total_welfare: useStorage("owner-total-welfare", -1),
    mean_welfare: useStorage("owner-mean-welfare", -1),
    median_welfare: useStorage("owner-median-welfare", -1),
    max_welfare: useStorage("owner-max-welfare", -1),
    min_welfare: useStorage("owner-min-welfare", -1),
    welfare_quantiles: useStorage("owner-bid-quantiles", []),
    welfare_outliers: useStorage("owner-bid-outliers", []),
    number_of_agents: useStorage("owner-n-agents", -1),
    number_of_ab_agents: useStorage("owner-n-ab-agents", -1),
    number_of_aba_agents: useStorage("owner-n-aba-agents", -1),
    number_of_abc_agents: useStorage("owner-n-abc-agents", -1),
    number_of_stationary_agents: useStorage("owner-n-stationary-agents", -1),
  }),
  getters: {},
  actions: {
    select(owner) {
      this.selected = true;
      this.id = owner.id;
      this.name = owner.name;
      this.color = owner.color;
      this.agents = owner.agents;
      this.total_time_in_air = owner.total_time_in_air;
      this.total_bid_value = owner.total_bid_value;
      this.mean_bid_value = owner.mean_bid_value;
      this.median_bid_value = owner.median_bid_value;
      this.max_bid_value = owner.max_bid_value;
      this.min_bid_value = owner.min_bid_value;
      this.bid_quantiles = owner.bid_quantiles;
      this.bid_outliers = owner.bid_outliers;
      this.total_welfare = owner.total_welfare;
      this.mean_welfare = owner.mean_welfare;
      this.median_welfare = owner.median_welfare;
      this.max_welfare = owner.max_welfare;
      this.min_welfare = owner.min_welfare;
      this.welfare_quantiles = owner.welfare_quantiles;
      this.welfare_outliers = owner.welfare_outliers;
      this.number_of_agents = owner.number_of_agents;
      this.number_of_ab_agents = owner.number_of_ab_agents;
      this.number_of_aba_agents = owner.number_of_aba_agents;
      this.number_of_abc_agents = owner.number_of_abc_agents;
      this.number_of_stationary_agents = owner.number_of_stationary_agents;
    },
    deselect() {
      this.selected = false;
    },
  },
});
