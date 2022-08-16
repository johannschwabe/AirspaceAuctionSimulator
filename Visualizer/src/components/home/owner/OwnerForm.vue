<template>
  <!-- Inputs for color, name and number of agents -->
  <n-color-picker :modes="['hex']" :show-alpha="false" v-model:value="owner.color" />
  <n-input v-model:value="owner.name" type="text" placeholder="Owner Name" />
  <n-input-number v-model:value="owner.agents" :min="1" :max="100" style="min-width: 130px" placeholder="Nr. Agents" />
  <!-- Dropdown selection for owner type -->
  <n-select
    v-model:value="owner.type"
    :options="simulationConfig.availableOwnersForAllocator"
    label-field="label"
    value-field="name"
    placeholder="Type"
    @update:value="updateLocationsForOwner"
  />
</template>

<script setup>
import { computed } from "vue";
import { useSimulationConfigStore } from "@/stores/simulationConfig";

const props = defineProps({
  ownerIndex: {
    type: Number,
    required: true,
  },
});

const simulationConfig = useSimulationConfigStore();

const owner = computed(() => simulationConfig.owners[props.ownerIndex]);

const ownerProperties = computed(() => {
  return simulationConfig.availableOwnersForAllocator.find((o) => o.name === owner.value.type);
});

/**
 * Whenever the selected ownerType changes, make sure the requirements for minimum
 * and maximum number of locations are met
 */
const updateLocationsForOwner = () => {
  owner.value.meta = ownerProperties.value.meta;
  owner.value.minLocations = ownerProperties.value.minLocations;
  owner.value.maxLocations = ownerProperties.value.maxLocations;
  if (owner.value.locations > owner.value.maxLocations) {
    owner.value.locations = owner.value.locations.slice(0, owner.value.maxLocations);
  }
  while (owner.value.locations < owner.value.minLocations) {
    owner.value.locations.push(simulationConfig.randomLocation());
  }
};
</script>

<style scoped></style>
