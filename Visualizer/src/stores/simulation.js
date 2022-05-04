import { defineStore } from "pinia";
import { useStorage } from "@vueuse/core";
import { emitAgentsSelectedEvent, emitTickEvent } from "../scripts/emitter";

export const useSimulationStore = defineStore({
  id: "simulation",
  state: () => ({
    selectedAgentIDs: useStorage("simulation-selected-agent-ids", []),
    tick: useStorage("simulation-tick", 0),
  }),
  getters: {
    timeline(state) {
      const timeseries = Array(state.dimensions.t).fill(0);
      this.selectedAgents.forEach((agent) => {
        Object.keys(agent.positions)
          .filter((t) => t <= state.dimensions.t)
          .forEach((t) => {
            timeseries[t] += 1;
          });
      });
      return timeseries;
    },
  },
  actions: {
    updateTick(tick) {
      this.tick = tick;
      emitTickEvent(this.tick);
    },
    setSelectedAgentIDs(selectedIds) {
      this.selectedAgentIDs = [...selectedIds];
      emitAgentsSelectedEvent(selectedIds);
    },
  },
});
