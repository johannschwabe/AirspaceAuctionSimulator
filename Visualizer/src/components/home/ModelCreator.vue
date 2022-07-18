<template>
  <n-form ref="formRef" :model="model" :rules="rules">
    <n-form-item path="name" label="Model Name">
      <n-input v-model:value="model.name" type="text" placeholder="Unique Model Name" />
    </n-form-item>
    <n-form-item path="description" label="Model Description">
      <n-input v-model:value="model.description" type="textarea" placeholder="Model description (Metadata)" />
    </n-form-item>
    <n-form-item path="allocator" label="Allocator">
      <n-select
        v-model:value="selected_allocator"
        :options="allocators"
        placeholder="Select Allocator"
        :on-update-value="getCompatibleOwners"
      />
    </n-form-item>

    <map-selector @dimensionChange="setDimension" @map-change="(map) => (model.map = map)" />

    <n-form-item path="dimension.t" label="Timesteps">
      <n-slider show-tooltip v-model:value="model.dimension.t" :min="10" :max="1000" :step="10" />
    </n-form-item>
    <n-form-item path="owners" label="Owners">
      <owner
        v-if="Object.keys(availableOwners).length > 0"
        ref="ownerRef"
        :dimension="model.dimension"
        :map-info="model.map"
        :availableOwners="availableOwners"
      />
    </n-form-item>
  </n-form>

  <n-popconfirm
    v-if="canRecover"
    negative-text="Download Cached"
    positive-text="Simulate & Overwrite"
    @positive-click="simulate"
    @negative-click="() => api.downloadSimulation()"
  >
    <template #trigger>
      <n-button ghost type="primary" :loading="loading">
        {{ loading ? `Running Simulation... (${loadingForSeconds}s)` : "Simulate" }}
      </n-button>
    </template>
    You do have an old session in your browser cache. It will be overwritten!
  </n-popconfirm>
  <n-button ghost type="primary" @click.stop="simulate" v-else :loading="loading">
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
import { ref, reactive } from "vue";
import { useMessage, useLoadingBar } from "naive-ui";
import { useRouter } from "vue-router";
import { CloudDownloadOutline, ArrowForwardOutline } from "@vicons/ionicons5";

import Owner from "./Owner.vue";
import MapSelector from "./MapSelector.vue";
import Simulation from "../../SimulationObjects/Simulation.js";
import api, { getOwners } from "../../API/api.js";
import {
  canRecoverSimulationSingleton,
  hasSimulationSingleton,
  setSimulationSingleton,
} from "../../scripts/simulation.js";

const message = useMessage();
const loadingBar = useLoadingBar();
const router = useRouter();

const formRef = ref(null);
const ownerRef = ref(null);
const errorText = ref(null);

const loading = ref(false);
const loadingForSeconds = ref(0);
const loadingInterval = ref(undefined);
const finished = ref(false);
const canRecover = ref(hasSimulationSingleton() || canRecoverSimulationSingleton());

const model = reactive({
  name: null,
  description: null,
  map: null,
  dimension: {
    x: 100,
    y: 20,
    z: 100,
    t: 250,
  },
});

const allocators = ref([]);
const selected_allocator = ref("FCFSAllocator");

api.getAllocators().then((_allocators) => {
  allocators.value = _allocators.map((_allocator) => {
    return { label: _allocator, value: _allocator };
  });
});

const owners = ref([]);
let availableOwners = ref({});

const rules = {
  name: [
    {
      required: true,
      trigger: ["input", "blur"],
    },
  ],
};
const getCompatibleOwners = (selection) => {
  getOwners(selection).then((_owners) => {
    availableOwners.value = {};
    _owners.forEach((_owner) => {
      availableOwners.value[_owner.classname] = _owner;
    });
  });
};
getCompatibleOwners(selected_allocator.value);

const setDimension = (dimension) => {
  model.dimension.x = dimension.x;
  model.dimension.y = dimension.y;
  model.dimension.z = dimension.z;
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

const simulate = () => {
  errorText.value = null;
  owners.value = ownerRef.value.getData();
  formRef.value?.validate((errors) => {
    if (!errors) {
      startLoading();
      api
        .postSimulation({
          ...model,
          owners: owners.value,
          allocator: selected_allocator.value,
        })
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
