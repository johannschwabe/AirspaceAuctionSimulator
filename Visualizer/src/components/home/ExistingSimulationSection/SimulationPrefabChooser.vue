<template>
  <n-select filterable v-model:value="selectedModel" :options="prefabs" placeholder="Choose predefined Simulation" />
</template>

<script setup>
import { ref, watch } from "vue";
import { useLoadingBar, useMessage } from "naive-ui";
import { useRouter } from "vue-router";
import { persistSimulation } from "@/API/api";
import Simulation from "@/SimulationObjects/Simulation";
import { setSimulationConfig, setSimulationSingleton } from "@/scripts/simulationSingleton";

const message = useMessage();
const loadingBar = useLoadingBar();
const router = useRouter();

/**
 * List of all available models, grouped by theme or intention. All files referenced here must
 * be placed within the "public" folder of the Visualizer. All simulation files are lazy-loaded
 * when they are used.
 * @type {[{children: [{label: string, value: string}], label: string, type: string, key: string}]}
 */
const prefabs = [
  {
    type: "group",
    label: "Report",
    key: "report",
    children: [
      {
        label: "Report Demo Model",
        value: "report-demo-output",
      },
    ],
  },
];

const selectedModel = ref(null);

watch(selectedModel, () => {
  loadingBar.start();
  fetch(`/models/${selectedModel.value}.json`)
    .then((response) => {
      if (!response.ok) {
        loadingBar.error();
        message.error("Import failed!");
        throw new Error("Import failed!");
      } else {
        return response.json();
      }
    })
    .then(async (data) => {
      await persistSimulation(data);
      const simulation = new Simulation(data.simulation, data.config, data.statistics, data.owner_map);
      await simulation.load();
      setSimulationSingleton(simulation);
      setSimulationConfig(data.config);
      await router.push({ name: "dashboard" });
    });
});
</script>

<style scoped></style>
