<template>
  <n-select filterable v-model:value="selectedModel" :options="options" placeholder="Choose predefined Simulation" />
</template>

<script setup>
import { ref, watch } from "vue";
import { useLoadingBar, useMessage } from "naive-ui";
import { useRouter } from "vue-router";
import { persistSimulation } from "@/API/api";
import Simulation from "@/SimulationObjects/Simulation";
import { setSimulationConfig, setSimulationSingleton } from "@/scripts/simulation";

const message = useMessage();
const loadingBar = useLoadingBar();
const router = useRouter();

const options = [
  {
    type: "group",
    label: "Ports",
    key: "ports",
    children: [
      {
        label: "Barcelona Port",
        value: "barcelona-port",
      },
    ],
  },
  {
    type: "group",
    label: "UBS",
    key: "ubs",
    children: [
      {
        label: "UBS Paradeplatz",
        value: "UBS",
      },
    ],
  },
  {
    type: "group",
    label: "Grossmünster",
    key: "GB",
    children: [
      {
        label: "Grossmünster",
        value: "Grossmünster",
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
      persistSimulation(data);
      const simulation = new Simulation(data);
      await simulation.load();
      setSimulationSingleton(simulation);
      setSimulationConfig(simulation);
      await router.push({ name: "dashboard" });
    });
});
</script>

<style scoped></style>
