<template>
  <div>
    <n-dynamic-input v-model:value="owners" :on-create="onCreate">
      <template #default="{ value, index }">
        <div style="display: flex; column-gap: 10px; width: 100%">
          <owner-form :model-value="value" @update:modelValue="updateOwner(index, $event)" />
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
          :map-info="mapInfo"
          :dimension="dimension"
        />
      </n-drawer-content>
    </n-drawer>
  </div>
</template>

<script setup>
import { computed, ref, watchEffect } from "vue";
import { Options } from "@vicons/ionicons5";
import OwnerOptions from "./OwnerOptions.vue";
import OwnerForm from "./OwnerForm.vue";

defineProps({
  dimension: {
    type: Object,
    required: true,
  },
  mapInfo: {
    type: Object,
    required: false,
    default: null,
  },
});

function updateOwner(ownerIndex, updatedOwner) {
  if (ownerIndex !== null) {
    const originalOwner = owners.value[ownerIndex];
    originalOwner.color = updatedOwner.color;
    originalOwner.name = updatedOwner.name;
    originalOwner.agents = updatedOwner.agents;
    originalOwner.type = updatedOwner.type;
  }
}

const optionsIndex = ref(null);
const showOptions = ref(false);
const option = computed(() => (optionsIndex.value !== null ? owners.value[optionsIndex.value] : null));

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

const defaultStop = {
  type: "random",
  position: null,
  heatmap: {},
};

const owners = ref([
  {
    color: "#00559d",
    name: "Digitec",
    agents: 20,
    type: "aba",
    start: { ...defaultStop },
    target: { ...defaultStop },
    stops: [],
  },
]);

const onCreate = () => {
  return {
    color: "#63e2b7",
    name: null,
    agents: null,
    type: "ab",
    start: { ...defaultStop },
    target: { ...defaultStop },
    stops: [],
  };
};

defineExpose({
  owners,
});
</script>

<style scoped></style>
