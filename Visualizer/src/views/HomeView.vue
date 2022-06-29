<template>
  <n-grid cols="2" :x-gap="24">
    <n-grid-item span="1">
      <div class="center">
        <section-text
          title="Upload Simulation"
          text="If you already have a valid Airspace-Auction-Simulation .AAS-File, drop it here to visualize it"
        />
        <history-uploader />
      </div>
    </n-grid-item>
    <n-grid-item span="1">
      <div class="center">
        <section-text
          title="Simulate Scenario"
          text="Configure a model here to create and visualize a new Airspace-Auction-Simulation (AAS)"
        />
        <model-creator />
      </div>
    </n-grid-item>
  </n-grid>
  <n-modal
    v-model:show="canRecover"
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

<style>
.full-height {
  height: 100vh;
  width: 100%;
  display: flex;
  justify-content: center;
}
.center {
  width: 100%;
  max-width: 750px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  row-gap: 25px;
}
</style>
<script setup>
import HistoryUploader from "../components/home/HistoryUploader.vue";
import ModelCreator from "../components/home/ModelCreator.vue";
import SectionText from "../components/home/SectionText.vue";
import { canRecoverSimulationSingleton, hasSimulationSingleton } from "../scripts/simulation";
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useLoadingBar } from "naive-ui";

const router = useRouter();
const loadingBar = useLoadingBar();

const canRecover = ref(hasSimulationSingleton() || canRecoverSimulationSingleton());

const recoverSession = () => {
  loadingBar.start();
  router.push({ name: 'dashboard' });
};

const ignoreRecoverableSession = () => {
  canRecover.value = false;
};
</script>
