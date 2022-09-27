<template>
  <n-form ref="formRef" :model="simulationConfig" :rules="rules">
    <!-- Model Name -->
    <n-form-item path="name">
      <template #label>
        <help v-bind="hName">Model Name</help>
      </template>
      <n-input v-model:value="simulationConfig.name" type="text" placeholder="Unique Model Name" />
    </n-form-item>

    <!-- Model Description -->
    <n-form-item>
      <template #label>
        <help v-bind="hDescription">Model Description</help>
      </template>
      <n-input
        v-model:value="simulationConfig.description"
        type="textarea"
        placeholder="Model description (Metadata)"
      />
    </n-form-item>

    <!-- Model Map -->
    <map-selector />

    <!-- Model Timesteps -->
    <n-form-item>
      <template #label>
        <help v-bind="hTimesteps">Timesteps</help>
      </template>
      <n-slider show-tooltip v-model:value="simulationConfig.map.timesteps" :min="300" :max="4000" :step="10" />
    </n-form-item>

    <n-grid cols="2" x-gap="10">
      <n-gi>
        <!-- Model Allocator -->
        <n-form-item>
          <template #label>
            <help v-bind="hAllocator">Allocator</help>
          </template>
          <n-select
            v-model:value="simulationConfig.allocator"
            :options="simulationConfig.availableAllocatorsOptions"
            placeholder="Select Allocator"
            v-on:update:value="emitAllocatorSwitched"
          />
        </n-form-item>
      </n-gi>
      <n-gi>
        <!-- Model Payment Rule -->
        <n-form-item>
          <template #label>
            <help v-bind="hPaymentRule">Payment Rule</help>
          </template>
          <n-select
            v-model:value="simulationConfig.paymentRule"
            :options="simulationConfig.availablePaymentRulesOptions"
            placeholder="Select Payment Rule"
          />
        </n-form-item>
      </n-gi>
    </n-grid>

    <!-- Model Owners -->
    <n-form-item>
      <template #label>
        <help v-bind="hOwners">Owners</help>
      </template>
      <owner />
    </n-form-item>
  </n-form>

  <!-- Upload and Download of configuration file -->
  <n-grid cols="2" x-gap="10">
    <n-grid-item>
      <n-upload
        :custom-request="uploadConfiguration"
        accept="application/json"
        :on-preview="uploadConfiguration"
        class="upload"
      >
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
      <n-button
        block
        tertiary
        :type="!simulationConfig.isEmpty ? 'primary' : 'tertiary'"
        @click.stop="downloadConfiguration"
      >
        Download Simulation Configuration
        <template #icon>
          <n-icon>
            <cloud-download-outline />
          </n-icon>
        </template>
      </n-button>
    </n-grid-item>
  </n-grid>

  <!-- Overwrite or recover existing simulations -->
  <n-popconfirm
    v-if="canRecoverSimulation"
    negative-text="Download Cached"
    positive-text="Simulate & Overwrite"
    @positive-click="simulate"
    @negative-click="() => downloadSimulation()"
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

  <!-- On finished simulation, download simulation file or go to simulation -->
  <n-grid cols="2" x-gap="10" v-if="finished">
    <n-grid-item>
      <n-button ghost block icon-placement="right" type="primary" @click.stop="() => downloadSimulation()">
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

  <!-- Generic error alert -->
  <n-alert v-if="errorText" title="Invalid Data" type="error">
    {{ errorText }}
  </n-alert>
</template>

<script setup>
import { nextTick, onUnmounted, ref } from "vue";
import { useMessage, useLoadingBar } from "naive-ui";
import { useRouter } from "vue-router";
import { CloudDownloadOutline, ArrowForwardOutline, CloudUploadOutline } from "@vicons/ionicons5";
import { saveAs } from "file-saver";

import Owner from "./OwnerConfig.vue";
import MapSelector from "../../common/map/MapSelector.vue";
import Help from "../../common/help/help.vue";

import Simulation from "../../../SimulationObjects/Simulation.js";

import { postSimulation, downloadSimulation } from "../../../API/api.js";
import {
  canRecoverSimulationSingleton,
  hasSimulationSingleton,
  setSimulationConfig,
  setSimulationSingleton,
} from "@/scripts/simulationSingleton";
import { useSimulationConfigStore } from "@/stores/simulationConfigStore";
import {
  emitConfigLoaded,
  onAllocatorSwitched,
  offAllocatorSwitched,
  emitAllocatorSwitched,
} from "../../../scripts/emitter.js";
import { hName, hDescription, hTimesteps, hAllocator, hPaymentRule, hOwners } from "../../common/help/texts.js";

const simulationConfig = useSimulationConfigStore();
if (!simulationConfig.availableAllocators || simulationConfig.availableAllocators.length === 0) {
  simulationConfig.loadAvailableAllocators();
}
const message = useMessage();
const loadingBar = useLoadingBar();
const router = useRouter();

// Reference to NaiveUI Form for validation
const formRef = ref(null);

// Contains error text IFF error appeared
const errorText = ref(null);

const loading = ref(false);
const loadingForSeconds = ref(0);
const loadingInterval = ref(undefined);
const finished = ref(false);

const canRecoverSimulation = ref(hasSimulationSingleton());
canRecoverSimulationSingleton().then((val) => (canRecoverSimulation.value = canRecoverSimulation.value || val));

const rules = {
  name: [
    {
      required: true,
      trigger: ["input", "blur"],
    },
  ],
};

/**
 * Route to simulation dashboard
 */
const goToSimulation = () => {
  router.push({ name: "dashboard" });
};

/**
 * Start loading indication
 */
const startLoading = () => {
  loading.value = true;
  loadingBar.start();
  loadingInterval.value = setInterval(() => {
    loadingForSeconds.value += 1;
  }, 1000);
};

/**
 * Stop loading indications
 */
const stopLoading = () => {
  loading.value = false;
  loadingForSeconds.value = 0;
  clearInterval(loadingInterval.value);
};

/**
 * Generate and download simulation configurations as JSON-File
 */
const downloadConfiguration = () => {
  const fileToSave = new Blob([JSON.stringify(simulationConfig.generateConfigJson(), undefined, 2)], {
    type: "application/json",
  });

  saveAs(fileToSave, `${simulationConfig.name.toLowerCase().replace(/ /g,"-")}-config.json`);
};
onAllocatorSwitched(() => {
  nextTick(() => {
    simulationConfig.updateSupportedBiddingStrategies();
  });
});
onUnmounted(() => {
  offAllocatorSwitched();
});
/**
 * Upload an existing simulation configuration File
 * @param {UploadCustomRequestOptions} upload
 */
const uploadConfiguration = (upload) => {
  const fileReader = new FileReader();
  fileReader.onload = async (event) => {
    const data = JSON.parse(event.target.result);
    const config = data.config ?? data;
    simulationConfig.overwrite(config);
    emitConfigLoaded();
  };
  fileReader.onerror = () => {
    loadingBar.error();
    message.error("Import failed!");
    throw new Error("Import failed!");
  };
  fileReader.readAsText(upload.file.file);
};

/**
 * Start simulation of new AirspaceAuction Simulation using simulation configurations
 */
const simulate = () => {
  errorText.value = null;
  formRef.value?.validate((errors) => {
    if (!errors) {
      startLoading();
      postSimulation(simulationConfig.generateConfigJson())
        .then((data) => {
          const simulation = new Simulation(data.simulation, data.config, data.statistics);
          setSimulationConfig(data.config);
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
          console.error(e);
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
<style scoped>
.upload :deep(.n-upload-trigger) {
  width: 100%;
}
</style>
