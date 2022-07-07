<template>
  <n-upload :custom-request="onUpload">
    <n-upload-dragger>
      <div style="margin-bottom: 12px">
        <n-icon size="48" :depth="3">
          <archive-outline />
        </n-icon>
      </div>
      <n-text style="font-size: 16px"> Click or drag a file to this area to upload </n-text>
      <n-p depth="3" style="margin: 8px 0 0 0">
        Strictly prohibit from uploading sensitive information. For example, your bank card PIN or your credit card
        expiry date.
      </n-p>
    </n-upload-dragger>
  </n-upload>
</template>

<script setup>
import { ArchiveOutline } from "@vicons/ionicons5";
import { useLoadingBar, useMessage } from "naive-ui";
import { useRouter } from "vue-router";

import Simulation from "../../SimulationObjects/Simulation";
import { setSimulationSingleton } from "../../scripts/simulation";
import { persistSimulation } from "../../API/api";

const message = useMessage();
const loadingBar = useLoadingBar();
const router = useRouter();

const onUpload = async (upload) => {
  loadingBar.start();
  const fileReader = new FileReader();
  fileReader.onload = async (event) => {
    const data = JSON.parse(event.target.result);
    persistSimulation(data);
    const simulation = new Simulation(data);
    await simulation.load();
    setSimulationSingleton(simulation);
    await router.push({ name: "dashboard" });
  };
  fileReader.onerror = () => {
    loadingBar.error();
    message.error("Import failed!");
    throw new Error("Import failed!");
  };
  fileReader.readAsText(upload.file.file);
};
</script>

<style scoped></style>
