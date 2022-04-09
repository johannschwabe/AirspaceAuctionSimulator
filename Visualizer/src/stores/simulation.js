import { defineStore } from "pinia";
import { saveAs } from "file-saver";
import { useStorage } from "@vueuse/core";

export const useSimulationStore = defineStore({
  id: "simulation",
  state: () => ({
    loaded: false,
    name: useStorage("simulation-name", ""),
    description: useStorage("simulation-description", ""),
    owners: useStorage("simulation-owners", []),
    dimensions: useStorage("simulation-dimensions", {}),
    environment: useStorage("simulation-environment", {}),
    statistics: useStorage("simulation-statistics", {}),
    selectedAgentIDs: useStorage("simulation-selected-agent-ids", []),
    tick: useStorage("simulation-tick", 0),
    agentsCache: undefined,
  }),
  getters: {
    containsData(state) {
      return state.name && state.owners.length > 0;
    },
    agents(state) {
      if (state.agentsCache) {
        return state.agentsCache;
      }
      const agents = [];
      state.owners.forEach((owner) => {
        owner.agents.forEach((agent) => {
          agents.push({
            owner,
            ...agent,
          });
        });
      });
      agents.sort((a, b) => (a.paths[0].t[0] < b.paths[0].t[0] ? -1 : 1));
      state.agentsCache = agents;
      return agents;
    },
    selectedAgents(state) {
      return this.agents.filter((agent) =>
        state.selectedAgentIDs.includes(agent.id)
      );
    },
    activeAgents(state) {
      return this.selectedAgents.filter((agent) => {
        return agent.paths.some((path) => {
          const has_started = path.t.some((t) => t <= state.tick);
          const has_not_landed = path.t.some((t) => t >= state.tick);
          return has_started && has_not_landed;
        });
      });
    },
    activeAgentIDs() {
      return this.activeAgents.map((agent) => agent.id);
    },
    activeBlockers(state) {
      return state.environment.blockers.filter((blocker) =>
        blocker.t.includes(state.tick)
      );
    },
    activeBlockerIDs() {
      return this.activeBlockers.map((blocker) => blocker.id);
    },
    timeline(state) {
      const timeseries = Array(state.dimensions.t).fill(0);
      this.agents.forEach((agent) => {
        agent.paths.forEach((path) => {
          path.t
            .filter((t) => t <= state.dimensions.t)
            .forEach((t) => {
              timeseries[t] += 1;
            });
        });
      });
      return timeseries;
    },
  },
  actions: {
    setSelectedAgentIDs(selectedIds) {
      this.selectedAgentIDs = [...selectedIds];
    },
    setSimulation(simulation) {
      this.loaded = true;
      this.selectedAgentIDs = [];
      this.tick = 0;
      this.name = simulation.name;
      this.description = simulation.description;
      this.owners = simulation.owners;
      this.environment = simulation.environment;
      this.dimensions = simulation.environment.dimensions;
      this.statistics = simulation.statistics;
    },
    download() {
      const fileToSave = new Blob([JSON.stringify(this, undefined, 2)], {
        type: "application/json",
      });
      saveAs(fileToSave, `${this.name}.json`);
    },
  },
});
