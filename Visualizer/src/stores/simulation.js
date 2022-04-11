import { defineStore } from "pinia";
import { saveAs } from "file-saver";
import { useStorage } from "@vueuse/core";
import { useEmitter } from "../scripts/emitter";
import { first } from "lodash-es";

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
    activeAgentsCache: undefined,
    activeBlockersCache: undefined,
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
          const positions = {};
          agent.paths.forEach((path) => {
            path.t.forEach((t, i) => {
              positions[t] = [path.x[i], path.y[i], path.z[i]];
            });
          });
          agents.push({
            positions,
            owner_color: owner.color,
            ...agent,
          });
        });
      });
      agents.sort((a, b) =>
        first(Object.keys(a.positions)) < first(Object.keys(b.positions))
          ? -1
          : 1
      );
      state.agentsCache = agents;
      return agents;
    },
    selectedAgents(state) {
      return this.agents.filter((agent) =>
        state.selectedAgentIDs.includes(agent.id)
      );
    },
    activeAgents(state) {
      this.updateActiveAgentsCache();
      const currentActiveAgents = this.activeAgentsCache[this.tick] || [];
      return currentActiveAgents.filter((agent) => {
        return state.selectedAgentIDs.includes(agent.id);
      });
    },
    activeAgentIDs() {
      return this.activeAgents.map((agent) => agent.id);
    },
    activeBlockers(state) {
      this.updateActiveBlockersCache();
      return state.activeBlockersCache[state.tick] || [];
    },
    activeBlockerIDs() {
      return this.activeBlockers.map((blocker) => blocker.id);
    },
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
      const emitter = useEmitter();
      emitter.emit("tick", this.tick);
    },
    setSelectedAgentIDs(selectedIds) {
      this.selectedAgentIDs = [...selectedIds];
      const emitter = useEmitter();
      emitter.emit("new-agents-selected", this.tick);
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

      this.updateActiveAgentsCache();
      this.updateActiveBlockersCache();
    },
    updateActiveAgentsCache() {
      if (this.activeAgentsCache) {
        return;
      }
      this.activeAgentsCache = {};
      this.agents.forEach((agent) => {
        Object.keys(agent.positions).forEach((t) => {
          if (!(t in this.activeAgentsCache)) {
            this.activeAgentsCache[t] = [];
          }
          this.activeAgentsCache[t].push(agent);
        });
      });
    },
    updateActiveBlockersCache() {
      if (this.activeBlockersCache) {
        return;
      }
      this.activeBlockersCache = {};
      this.environment.blockers.forEach((blocker) => {
        blocker.t.forEach((t) => {
          if (!(t in this.activeBlockersCache)) {
            this.activeBlockersCache[t] = [];
          }
          this.activeBlockersCache[t].push(blocker);
        });
      });
    },
    download() {
      const fileToSave = new Blob([JSON.stringify(this, undefined, 2)], {
        type: "application/json",
      });
      saveAs(fileToSave, `${this.name}.json`);
    },
  },
});
