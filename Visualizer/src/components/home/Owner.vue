<template>
  <div>
    <n-dynamic-input v-model:value="owners" :on-create="onCreate">
      <template #default="{ value, index }">
        <div style="display: flex; column-gap: 10px; width: 100%">
          <owner-form v-model="value.owner" :options="availableOwners" />
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
          :options="availableOwners"
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

const props = defineProps({
  dimension: {
    type: Object,
    required: true,
  },
  mapInfo: {
    type: Object,
    required: false,
    default: null,
  },
  availableOwners: {
    type: Object,
    required: true,
  },
});

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
  () => props.availableOwners,
  () => {
    defaultOwner.owner.color = "#" + ((Math.random() * 0xffffff) << 0).toString(16).padStart(6, "0");
    defaultOwner.owner.type = Object.keys(props.availableOwners)[0];
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

function getData() {
  return owners.value.map((owner) => {
    const stops = [owner.owner.start, ...owner.owner.stops, owner.owner.target];
    const cleanedStops = stops.map((stop) => {
      const cleanStop = { type: stop.stop.type };
      const heatmap = {};

      switch (stop.stop.type) {
        case "heatmap":
          Object.entries(stop.stop.heatmap.keys).forEach(([key, value]) => {
            const stringValue = `${value}`.replace(".", "_");
            if (heatmap[stringValue] === undefined) {
              heatmap[stringValue] = [key];
            } else {
              heatmap[stringValue].push(key);
            }
          });
          cleanStop.heatmap = heatmap;
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
  defaultOwner.owner.type = Object.keys(props.availableOwners)[0];
  defaultOwner.owner.color = "#" + ((Math.random() * 0xffffff) << 0).toString(16).padStart(6, "0");
  return { owner: { ...defaultOwner.owner } };
};
const owners = ref([onCreate()]);

defineExpose({
  getData,
});
</script>
