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
    tick: useStorage('simulation-tick', 100),
  }),
  getters: {
    getAgents: (state) => [],
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
