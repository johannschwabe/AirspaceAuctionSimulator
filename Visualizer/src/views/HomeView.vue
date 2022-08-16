<template>
  <n-grid cols="2" :x-gap="24">
    <!-- LEFT PART: UPLOAD EXISTING SIMULATION -->
    <n-grid-item span="1">
      <div class="center">
        <section-text
          title="Upload Simulation"
          text="If you already have a valid Airspace-Auction-Simulation .JSON-File, drop it here to visualize it"
        />
        <simulation-uploader />
        <simulation-chooser />
      </div>
    </n-grid-item>

    <!-- RIGHT PART: CONFIGURE NEW SIMULATION -->
    <n-grid-item span="1">
      <div class="center">
        <section-text
          title="Simulate Scenario"
          text="Configure a model here to create and visualize a new Airspace-Auction-Simulation"
        />
        <model-creator />
      </div>
    </n-grid-item>
  </n-grid>
  <!-- Modal that pops up when an existing simulation is found in localStorage -->
  <n-modal
    v-model:show="canRecoverSimulation"
    :mask-closable="false"
    preset="dialog"
    title="Recover Simulation"
    content="You have an old session in your browser cache. Do you want to recover it?"
    positive-text="Recover"
    negative-text="Ignore"
    @positive-click="recoverSession"
    @negative-click="ignoreRecoverableSession"
  />
</template>
<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useLoadingBar } from "naive-ui";

import SimulationUploader from "../components/home/SimulationUploader.vue";
import ModelCreator from "../components/home/ModelCreator.vue";
import SectionText from "../components/home/SectionText.vue";
import SimulationChooser from "@/components/home/SimulationChooser.vue";

import { canRecoverSimulationSingleton, hasSimulationSingleton } from "@/scripts/simulation";

const router = useRouter();
const loadingBar = useLoadingBar();

const canRecoverSimulation = ref(hasSimulationSingleton() || canRecoverSimulationSingleton());

// The dashboard will recover the simulationt that can be recovered through localStorage
const recoverSession = () => {
  loadingBar.start();
  router.push({ name: "dashboard" });
};

const ignoreRecoverableSession = () => {
  canRecoverSimulation.value = false;
};
</script>
<style>
.center {
  width: 100%;
  max-width: 750px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  row-gap: 25px;
}
</style>
