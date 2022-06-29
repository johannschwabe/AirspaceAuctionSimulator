import { defineStore } from "pinia";
import { useStorage } from "@vueuse/core";
import { emitAgentsSelectedEvent, emitTickEvent } from "../scripts/emitter";

export const useSimulationStore = defineStore({
  id: "simulation",
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
      console.log("UPDATE TICK");
      emitTickEvent(tick);
    },
    setSelectedAgentIDs(selectedIds) {
      this.selectedAgentIDs = [...selectedIds];
      emitAgentsSelectedEvent(selectedIds);
    },
  },
});
