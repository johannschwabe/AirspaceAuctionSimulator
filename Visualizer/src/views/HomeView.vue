<template>
  <n-grid cols="2" :x-gap="24">
    <n-grid-item span="1" class="full-height">

      <div class="center">
        <section-text
          title="Upload Simulation"
          text="If you already have a valid Airspace-Auction-Simulation .AAS-File, drop it here to visualize it"
        />
        <history-uploader />
      </div>

    </n-grid-item>
    <n-grid-item span="1" class="full-height">

      <div class="center">
        <section-text
            title="Simulate Scenario"
            text="Configure a model here to create and visualize a new Airspace-Auction-Simulation (AAS)"
        />
        <model-creator />
      </div>

    </n-grid-item>
  </n-grid>
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
  display: flex;
  flex-direction: column;
  row-gap: 25px;
}
</style>
<script setup>
import HistoryUploader from "../components/home/HistoryUploader.vue";
import ModelCreator from "../components/home/ModelCreator.vue";
import SectionText from "../components/home/SectionText.vue";
</script>
