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
    tick: useStorage("simulation-tick", 1),
  }),
  getters: {
    agents(state) {
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
    // activeAgentIDs() {
    //   return this.activeAgents.map((agent) => agent.id);
    // },
    // timeline(state) {
    //   const timeseries = Array(state.dimensions.t).fill(0);
    //   this.agents.forEach((agent) => {
    //     agent.paths.forEach((path) => {
    //       path.t.forEach((t) => {
    //         timeseries[t] += 1;
    //       });
    //     });
    //   });
    //   return timeseries;
    // },
    // locations() {
    //   const locations = [];
    //   this.agents.forEach((agent) => {
    //     agent.paths.forEach((path) => {
    //       for (let i = 0; i < path.t.length; i++) {
    //         locations.push({
    //           agent,
    //           x: path.x[i],
    //           y: path.y[i],
    //           z: path.z[i],
    //         });
    //       }
    //     });
    //   });
    //   return locations;
    // },
    // pastLocations(state) {
    //   return this.locations.filter((loc) => loc.t <= state.tick);
    // },
    // currentLocations(state) {
    //   const locations = [];
    //   this.activeAgents.forEach((agent) => {
    //     const currentPath = agent.paths.find((path) =>
    //       path.t.includes(state.tick)
    //     );
    //     const i = currentPath.t.indexOf(state.tick);
    //     const location = {
    //       x: currentPath.x[i],
    //       y: currentPath.y[i],
    //       z: currentPath.z[i],
    //     };
    //     locations.push({
    //       agent,
    //       ...location,
    //     });
    //   });
    //   locations.sort((a, b) => (a.t < b.t ? -1 : 1));
    //   return locations;
    // },
  },
  actions: {
    setSelectedAgentIDs(selectedIds) {
      this.selectedAgentIDs = [...selectedIds];
    },
    setSimulation(simulation) {
      this.loaded = true;
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
