import { defineStore } from 'pinia'
import { saveAs } from 'file-saver';
import { useStorage } from '@vueuse/core'

export const useSimulationStore = defineStore({
  id: 'simulation',
  state: () => ({
    loaded: false,
    name: useStorage('simulation-name', ''),
    description: useStorage('simulation-description', ''),
    owners: useStorage('simulation-owners', []),
    dimensions: useStorage('simulation-dimensions', {}),
    tick: useStorage('simulation-tick', 1),
  }),
  getters: {
    agents(state) {
      const agents = [];
      state.owners.forEach((owner) => {
        owner.agents.forEach((agent) => {
          agents.push({
            owner,
            ...agent,
          })
        })
      })
      agents.sort((a, b) => a.locations[0].t < b.locations[0].t ? -1 : 1)
      return agents;
    },
    activeAgents(state) {
      return this.agents.filter((agent) => {
        const has_started = agent.locations.some((loc) => loc.t <= state.tick);
        const has_not_landed = agent.locations.some((loc) => loc.t >= state.tick);
        return has_started && has_not_landed;
      })
    },
    activeAgentUUIDs(state) {
      return this.activeAgents.map((agent) => agent.uuid);
    },
    locations(state) {
      const locations = [];
      this.agents.forEach((agent) => {
        agent.locations.forEach((loc) => {
          locations.push({
            agent,
            ...loc,
          })
        })
      })
      locations.sort((a, b) => a.t < b.t ? -1 : 1);
      return locations;
    },
    pastLocations(state) {
      return this.locations.filter((loc) => loc.t <= state.tick);
    },
    currentLocations(state) {
      const locations = [];
      this.activeAgents.forEach((agent) => {
        const current_loc = agent.locations.find((loc) => loc.t === state.tick);
        locations.push({
          agent,
          ...current_loc,
        })
      })
      locations.sort((a, b) => a.t < b.t ? -1 : 1);
      return locations;
    },
  },
  actions: {
    setSimulation(simulation) {
      this.loaded = true;
      this.name = simulation.name;
      this.description = simulation.description;
      this.owners = simulation.owners;
      this.dimensions = simulation.dimensions;
    },
    download() {
      const fileToSave = new Blob([JSON.stringify(this,undefined,2)], {
        type: 'application/json'
      });
      saveAs(fileToSave, `${this.name}.json`);
    }
  }
})
