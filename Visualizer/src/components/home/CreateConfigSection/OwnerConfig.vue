<template>
  <!-- Simple one-line display of Owner -->
  <n-dynamic-input :value="simulationConfig.owners" :on-create="onCreate" :on-remove="onRemove" :min="1" style="margin-top: 24px;">
    <template #default="{ index }">
      <div style="display: flex; column-gap: 10px; width: 100%">
        <owner-form :owner-index="index" />
        <n-button tertiary circle @click="onOptions(index)">
          <template #icon>
            <n-icon>
              <Options />
            </n-icon>
          </template>
        </n-button>
      </div>
    </template>
  </n-dynamic-input>

  <!-- Modal that offers more in-depth owner configuration -->
  <n-drawer v-model:show="showOptions" :width="580" placement="left">
    <n-drawer-content v-if="optionsIndex !== null" :title="`Owner: ${simulationConfig.owners[optionsIndex].name}`">
      <owner-options :owner-index="optionsIndex" />
    </n-drawer-content>
  </n-drawer>
</template>

<script setup>
import { ref, watchEffect } from "vue";
import { Options } from "@vicons/ionicons5";

import OwnerOptions from "./OwnerOptionsModal.vue";
import OwnerForm from "./OwnerForm.vue";

import { useSimulationConfigStore } from "@/stores/simulationConfigStore";

const simulationConfig = useSimulationConfigStore();

// Controls open-close status of options modal
const showOptions = ref(false);

// Holds index of selected owner - relevant for modal
const optionsIndex = ref(null);

/**
 * Creates a new Owner at the given index
 * @param {number} index
 * @returns {}
 */
const onCreate = (index) => {
  const owner = simulationConfig.generateOwner();
  simulationConfig.owners.splice(index, 0, owner);
  return owner;
};

const onRemove = (index) => {
  simulationConfig.owners.splice(index, 1);
};

function onOptions(index) {
  if (optionsIndex.value === index) {
    showOptions.value = false;
    optionsIndex.value = null;
  } else {
    showOptions.value = true;
    optionsIndex.value = index;
  }
}

watchEffect(() => {
  if (showOptions.value === false) {
    optionsIndex.value = null;
  }
});
</script>
