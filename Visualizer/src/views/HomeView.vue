<template>
  <div id="home">
    <n-grid cols="5" :x-gap="24">
      <!-- LEFT PART: UPLOAD EXISTING SIMULATION -->
      <n-grid-item :span="2" style="padding-left: 24px">
        <div class="center">
          <div style="text-align: center; color: white">
            <h1>Upload Simulation</h1>
            <n-text style="font-size: 16px">
              If you already have a valid Airspace-Auction-Simulation .JSON-File, drop it here to visualize it
            </n-text>
          </div>
          <simulation-uploader />
          <simulation-chooser />
        </div>
      </n-grid-item>

      <!-- RIGHT PART: CONFIGURE NEW SIMULATION -->
      <n-grid-item :span="3" style="padding-right: 24px">
        <div class="center">
          <div style="text-align: center; color: white">
            <h1>Simulate Scenario</h1>
            <n-text style="font-size: 16px">
              Configure a model here to create and visualize a new Airspace-Auction-Simulation
            </n-text>
          </div>
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
  </div>
</template>
<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useLoadingBar } from "naive-ui";

import SimulationUploader from "../components/home/ExistingSimulationSection/SimulationUploader.vue";
import ModelCreator from "../components/home/CreateConfigSection/ConfigCreationForm.vue";
import SimulationChooser from "@/components/home/ExistingSimulationSection/SimulationPrefabChooser.vue";

import { canRecoverSimulationSingleton, hasSimulationSingleton } from "@/scripts/simulationSingleton";

const router = useRouter();
const loadingBar = useLoadingBar();

const canRecoverSimulation = ref(hasSimulationSingleton());
canRecoverSimulationSingleton().then((val) => (canRecoverSimulation.value = canRecoverSimulation.value || val));

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
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  row-gap: 25px;
}
#home {
  margin-bottom: 100px;
}
</style>
