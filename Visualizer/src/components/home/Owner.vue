<template>
  <div>
    <n-dynamic-input v-model:value="config.owners" :on-create="onCreate">
      <template #default="{ value, index }">
        <div style="display: flex; column-gap: 10px; width: 100%">
          <owner-form v-model:owner="value.owner" :options="config.availableOwnersForMechanism" />
          <n-button tertiary circle @click="onOptions(index)">
            <template #icon>
              <n-icon><Options /></n-icon>
            </template>
          </n-button>
        </div>
      </template>
    </n-dynamic-input>
    <n-drawer v-model:show="showOptions" :width="580" placement="left">
      <n-drawer-content v-if="option !== null" :title="`Owner: ${option.name}`">
        <owner-options
          :model-value="option"
          @update:modelValue="updateOwner(optionsIndex, $event)"
        />
      </n-drawer-content>
    </n-drawer>
  </div>
</template>

<script setup>
import { computed, ref, watch, watchEffect } from "vue";
import { Options } from "@vicons/ionicons5";
import OwnerOptions from "./OwnerOptions.vue";
import OwnerForm from "./OwnerForm.vue";
import { createDefaultStop } from "../../scripts/stops";
import * as _ from "lodash-es";
import { useSimulationConfigStore } from "../../stores/simulationConfig";

const config = useSimulationConfigStore();

const defaultOwner = {
  owner: {
    color: "#00559d",
    name: "Digitec",
    agents: 20,
    type: "",
    start: createDefaultStop(),
    target: createDefaultStop(),
    stops: [],
  },
};

function updateOwner(ownerIndex, updatedOwner) {
  if (ownerIndex !== null) {
    const originalOwner = owners.value[ownerIndex];
    if (originalOwner) {
      originalOwner.color = updatedOwner.color;
      originalOwner.name = updatedOwner.name;
      originalOwner.agents = updatedOwner.agents;
      originalOwner.type = updatedOwner.type;
    }
  }
}
watch(
  () => config.availableOwners,
  () => {
    defaultOwner.owner.color = "#" + ((Math.random() * 0xffffff) << 0).toString(16).padStart(6, "0");
    defaultOwner.owner.type = Object.keys(config.availableOwners)[0];
    owners.value = [defaultOwner];
  }
);

const optionsIndex = ref(null);
const showOptions = ref(false);
const option = computed(() => (optionsIndex.value !== null ? owners.value[optionsIndex.value].owner : null));

function onOptions(index) {
  if (optionsIndex.value === index) {
    showOptions.value = false;
    optionsIndex.value = null;
  } else {
    optionsIndex.value = index;
    showOptions.value = true;
  }
}

watchEffect(() => {
  if (showOptions.value === false) {
    optionsIndex.value = null;
  }
});

const onCreate = () => {
  defaultOwner.owner.type = Object.keys(config.availableOwners)[0];
  defaultOwner.owner.color = "#" + ((Math.random() * 0xffffff) << 0).toString(16).padStart(6, "0");
  const _owner = _.cloneDeep(defaultOwner.owner);
  return { owner: _owner };
};
const owners = ref([onCreate()]);
</script>
