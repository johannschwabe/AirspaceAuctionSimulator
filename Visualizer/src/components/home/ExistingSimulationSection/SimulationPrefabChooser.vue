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
    label: "Python Demos",
    key: "report",
    children: [
      {
        label: "HowTo Demo",
        value: "1_python_demo_howto-output",
      },
      {
        label: "Reallocations Demo",
        value: "2_python_demo_reallocations-output",
      },
      {
        label: "Collisions Demo",
        value: "3_python_demo_collisions-output",
      },
      {
        label: "Fast Demo",
        value: "4_python_demo_fast-output",
      },
      {
        label: "Weather Demo",
        value: "5_python_demo_weather-output",
      },
    ],
  },
  {
    type: "group",
    label: "Python Comparison Demos",
    key: "comparison",
    children: [
      {
        label: "Compare FCSF Demo",
        value: "6_python_demo_comparison_fcfsallocator-output",
      },
      {
        label: "Compare Priority Demo",
        value: "6_python_demo_comparison_priorityallocator-output",
      },
    ],
  },
  {
    type: "group",
    label: "Web Demos",
    key: "web",
    children: [
      {
        label: "Long Paths Demo",
        value: "7_web_demo_long_paths-output",
      },
      {
        label: "Flat Terrain Demo",
        value: "8_web_demo_flat_terrain-output",
      },
      {
        label: "University Hospital Zurich",
        value: "9_web_demo_university_hospital_zurich-output",
      },
    ],
  },
  {
    type: "group",
    label: "CLI Demos",
    key: "cli",
    children: [
      {
        label: "Tel Aviv Demo",
        value: "10_cli_demo_tel_aviv-output",
      },
      {
        label: "New York Demo",
        value: "11_cli_demo_new_york-output",
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
