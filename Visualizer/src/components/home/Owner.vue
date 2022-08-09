<template>
  <div>
    <n-dynamic-input :value="simulationConfig.owners" :on-create="onCreate" :on-remove="onRemove" :min="1">
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
    <n-drawer v-model:show="showOptions" :width="580" placement="left">
      <n-drawer-content v-if="optionsIndex !== null" :title="`Owner: ${simulationConfig.owners[optionsIndex].name}`">
        <owner-options :owner-index="optionsIndex" />
      </n-drawer-content>
    </n-drawer>
  </div>
</template>

<script setup>
import { ref, watchEffect } from "vue";
import { Options } from "@vicons/ionicons5";
import OwnerOptions from "./OwnerOptions.vue";
import OwnerForm from "./OwnerForm.vue";
import { useSimulationConfigStore } from "../../stores/simulationConfig";

const simulationConfig = useSimulationConfigStore();

const showOptions = ref(false);
const optionsIndex = ref(null);

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
