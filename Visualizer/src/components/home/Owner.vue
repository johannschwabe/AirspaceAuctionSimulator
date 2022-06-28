<template>
  <div>
    <n-dynamic-input v-model:value="owners" :on-create="onCreate">
      <template #default="{ value, index }">
        <div style="display: flex; column-gap: 10px; width: 100%">
          <owner-form v-model="value.owner" />
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
import { createDefaultStop } from "../../scripts/stops";

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
    if (originalOwner) {
      originalOwner.color = updatedOwner.color;
      originalOwner.name = updatedOwner.name;
      originalOwner.agents = updatedOwner.agents;
      originalOwner.type = updatedOwner.type;
    }
  }
}

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

const owners = ref([
  {
    owner: {
      color: "#00559d",
      name: "Digitec",
      agents: 20,
      type: "aba",
      start: createDefaultStop(),
      target: createDefaultStop(),
      stops: [],
    },
  },
]);

function getData() {
  return owners.value.map((owner) => {
    const stops = [owner.owner.start, ...owner.owner.stops, owner.owner.target];
    const cleanedStops = stops.map((stop) => {
      const cleanStop = { type: stop.stop.type };
      switch (stop.stop.type) {
        case "heatmap":
          cleanStop.heatmap = { ...stop.stop.heatmap.keys };
          break;
        case "position":
          cleanStop.position = stop.stop.position.key;
          break;
        case "random":
        default:
          break;
      }
      return cleanStop;
    });
    return {
      color: owner.owner.color,
      name: owner.owner.name,
      agents: owner.owner.agents,
      type: owner.owner.type,
      stops: cleanedStops,
    };
  });
}

const onCreate = () => {
  return {
    owner: {
      color: "#63e2b7",
      name: null,
      agents: null,
      type: "ab",
      start: createDefaultStop(),
      target: createDefaultStop(),
      stops: [],
    },
  };
};

defineExpose({
  getData,
});
</script>
