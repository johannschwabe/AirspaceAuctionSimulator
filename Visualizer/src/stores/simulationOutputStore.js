import { defineStore } from "pinia";
import { useStorage } from "@vueuse/core";
import { emitAgentsSelectedEvent, emitTickEvent } from "@/scripts/emitter.js";

export const useSimulationOutputStore = defineStore({
  id: "simulationOutputStore",
  state: () => ({
    selectedAgentIDs: useStorage("simulation-selected-agent-ids", []),
    agentInFocus: false,
    agentInFocusId: -1,
    ownerInFocusId: -1,
    tick: useStorage("simulation-tick", 0),
  }),
  actions: {
    updateTick(tick) {
      this.tick = tick;
      emitTickEvent(tick);
    },
    setSelectedAgentIDs(selectedIds) {
      this.selectedAgentIDs = [...selectedIds];
      emitAgentsSelectedEvent(selectedIds);
    },
  },
});
