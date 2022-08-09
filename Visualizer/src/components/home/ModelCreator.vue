<template>
  <n-form ref="formRef" :model="simulationConfig" :rules="rules">
    <n-form-item path="name" label="Model Name">
      <n-input v-model:value="simulationConfig.name" type="text" placeholder="Unique Model Name" />
    </n-form-item>
    <n-form-item path="description" label="Model Description">
      <n-input v-model:value="simulationConfig.description" type="textarea" placeholder="Model description (Metadata)" />
    </n-form-item>

    <map-selector ref="mapRef" />

<!--    <n-form-item path="dimension.t" label="Timesteps">-->
<!--      <n-slider show-tooltip v-model:value="config.dimension.t" :min="300" :max="4000" :step="10" />-->
<!--    </n-form-item>-->

<!--    <n-form-item path="allocator" label="Mechanism">-->
<!--      <n-select v-model:value="config.mechanism" placeholder="Select Allocator" />-->
<!--    </n-form-item>-->

<!--    <n-form-item path="owners" label="Owners">-->
<!--      <owner-->
<!--        v-if="Object.keys(config.availableOwnersForMechanism).length > 0"-->
<!--        ref="ownerRef"-->
<!--        :dimension="config.dimension"-->
<!--        :map-info="model.map"-->
<!--        :availableOwners="availableOwners"-->
<!--      />-->
<!--    </n-form-item>-->
  </n-form>

  <n-grid cols="2" x-gap="10">
    <n-grid-item>
      <n-upload :custom-request="uploadConfiguration" accept="application/json" :on-preview="uploadConfiguration">
        <n-button block tertiary :type="simulationConfig.isEmpty ? 'primary' : 'tertiary'">
          Upload Simulation Configuration
          <template #icon>
            <n-icon>
              <cloud-upload-outline />
            </n-icon>
          </template>
        </n-button>
      </n-upload>
    </n-grid-item>
    <n-grid-item>
      <n-button block tertiary :type="!simulationConfig.isEmpty ? 'primary' : 'tertiary'" @click.stop="downloadConfiguration">
        Download Simulation Configuration
        <template #icon>
          <n-icon>
            <cloud-download-outline />
          </n-icon>
        </template>
      </n-button>
    </n-grid-item>
  </n-grid>

  <n-popconfirm
    v-if="canRecover"
    negative-text="Download Cached"
    positive-text="Simulate & Overwrite"
    @positive-click="simulate"
    @negative-click="() => api.downloadSimulation()"
  >
    <template #trigger>
      <n-button type="primary" :loading="loading">
        {{ loading ? `Running Simulation... (${loadingForSeconds}s)` : "Simulate" }}
      </n-button>
    </template>
    You do have an old session in your browser cache. It will be overwritten!
  </n-popconfirm>
  <n-button type="primary" @click.stop="simulate" v-else :loading="loading">
    {{ loading ? `Running Simulation... (${loadingForSeconds}s)` : "Simulate" }}
  </n-button>

  <n-grid cols="2" x-gap="10" v-if="finished">
    <n-grid-item>
      <n-button ghost block icon-placement="right" type="primary" @click.stop="() => api.downloadSimulation()">
        Download Simulation
        <template #icon>
          <n-icon>
            <cloud-download-outline />
          </n-icon>
        </template>
      </n-button>
    </n-grid-item>
    <n-grid-item>
      <n-button block icon-placement="right" type="primary" @click.stop="goToSimulation">
        Go to Simulation
        <template #icon>
          <n-icon>
            <arrow-forward-outline />
          </n-icon>
        </template>
      </n-button>
    </n-grid-item>
  </n-grid>

  <n-alert v-if="errorText" title="Invalid Data" type="error">
    {{ errorText }}
  </n-alert>
</template>

<script setup>
import { ref, computed } from "vue";
import { useMessage, useLoadingBar } from "naive-ui";
import { useRouter } from "vue-router";
import { CloudDownloadOutline, ArrowForwardOutline, CloudUploadOutline } from "@vicons/ionicons5";
import { saveAs } from "file-saver";

import Owner from "./Owner.vue";
import MapSelector from "./MapSelector.vue";
import Simulation from "../../SimulationObjects/Simulation.js";
import api from "../../API/api.js";
import {
  canRecoverSimulationSingleton,
  hasSimulationSingleton,
  setSimulationSingleton,
} from "../../scripts/simulation.js";
import { useSimulationConfigStore } from "../../stores/simulationConfig";

const simulationConfig = useSimulationConfigStore();

const message = useMessage();
const loadingBar = useLoadingBar();
const router = useRouter();

const formRef = ref(null);
const ownerRef = ref(null);
const mapRef = ref(null);
const errorText = ref(null);

const loading = ref(false);
const loadingForSeconds = ref(0);
const loadingInterval = ref(undefined);
const finished = ref(false);
const canRecover = ref(hasSimulationSingleton() || canRecoverSimulationSingleton());

const rules = {
  name: [
    {
      required: true,
      trigger: ["input", "blur"],
    },
  ],
};

const goToSimulation = () => {
  router.push({ name: "dashboard" });
};

const startLoading = () => {
  loading.value = true;
  loadingBar.start();
  loadingInterval.value = setInterval(() => {
    loadingForSeconds.value += 1;
  }, 1000);
};

const stopLoading = () => {
  loading.value = false;
  loadingForSeconds.value = 0;
  clearInterval(loadingInterval.value);
};

const downloadConfiguration = () => {
  const fileToSave = new Blob([JSON.stringify(simulationConfig.generateConfigJson(), undefined, 2)], {
    type: "application/json",
  });
  saveAs(fileToSave, `${simulationConfig.name}-config.json`);
};

const uploadConfiguration = (upload) => {
  const fileReader = new FileReader();
  fileReader.onload = async (event) => {
    const data = JSON.parse(event.target.result);
    simulationConfig.overwrite(data);
  };
  fileReader.onerror = () => {
    loadingBar.error();
    message.error("Import failed!");
    throw new Error("Import failed!");
  };
  fileReader.readAsText(upload.file.file);
};

const simulate = () => {
  errorText.value = null;
  formRef.value?.validate((errors) => {
    if (!errors) {
      startLoading();
      api
        .postSimulation(simulationConfig.generateConfigJson())
        .then((data) => {
          const simulation = new Simulation(data);
          return simulation.load();
        })
        .then((simulation) => {
          setSimulationSingleton(simulation);
          loadingBar.finish();
          message.success("Simulation Created!");
          finished.value = true;
        })
        .catch((e) => {
          loadingBar.error();
          message.error(e.message);
          errorText.value = e.message;
          throw new Error(e);
        })
        .finally(() => {
          stopLoading();
        });
    } else {
      errorText.value = "Some Form fields are not Valid";
    }
  });
};
</script>

<style scoped></style>
