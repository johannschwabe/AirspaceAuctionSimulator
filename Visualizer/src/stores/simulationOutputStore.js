import { defineStore } from "pinia";
import { emitAgentsSelectedEvent, emitTickEvent } from "@/scripts/emitter.js";

export const useSimulationOutputStore = defineStore("simulationOutputStore", {
  state: () => ({
    selectedAgentIDs: [],
    agentInFocus: false,
    agentInFocusId: -1,
    ownerInFocusId: -1,
    tick: 0,
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
