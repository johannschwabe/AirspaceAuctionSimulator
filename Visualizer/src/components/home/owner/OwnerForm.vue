<template>
  <!-- Inputs for color, name and number of agents -->
  <n-color-picker :modes="['hex']" :show-alpha="false" v-model:value="owner.color" />
  <n-input v-model:value="owner.name" type="text" placeholder="Owner Name" />
  <n-input-number v-model:value="owner.agents" :min="1" :max="100" style="min-width: 130px" placeholder="Nr. Agents" />
  <!-- Dropdown selection for owner type -->
  <n-select
    v-model:value="owner.biddingStrategy"
    :options="simulationConfig.availableBiddingStrategiesOptions"
    placeholder="Type"
    @update:value="updateLocationsForOwner"
  />
  <!-- Dropdown selection for owner type -->
  <n-select v-model:value="owner.valueFunction" :options="compatibleValueFunctions" placeholder="Type" />
</template>

<script setup>
import { computed, ref, watch, watchEffect } from "vue";
import { useSimulationConfigStore } from "../../../stores/simulationConfig.js";
import { getSupportedValueFunctions } from "../../../API/api";

const props = defineProps({
  ownerIndex: {
    type: Number,
    required: true,
  },
});

const simulationConfig = useSimulationConfigStore();

const owner = computed(() => simulationConfig.owners[props.ownerIndex]);
loadCompatibleValueFunctions();
/**
 * Whenever the selected ownerType changes, make sure the requirements for minimum
 * and maximum number of locations are met
 */
const updateLocationsForOwner = () => {
  // owner.value.meta = ownerProperties.value.meta;
  // owner.value.minLocations = ownerProperties.value.minLocations;
  // owner.value.maxLocations = ownerProperties.value.maxLocations;
  // if (owner.value.locations.length > owner.value.maxLocations) {
  //   owner.value.locations = owner.value.locations.slice(0, owner.value.maxLocations);
  // }
  // while (owner.value.locations.length < owner.value.minLocations) {
  //   owner.value.locations.push(simulationConfig.randomLocation());
  // }
};
const compatibleValueFunctions = ref([]);
watch(
  () => owner.value.biddingStrategy.classname,
  () => {
    loadCompatibleValueFunctions();
  }
);
function loadCompatibleValueFunctions() {
  getSupportedValueFunctions(simulationConfig.allocator, owner.value.biddingStrategy.classname).then((res) => {
    compatibleValueFunctions.value = res.map((a) => ({ label: a["label"], value: a["classname"] }));
    owner.value.valueFunction = compatibleValueFunctions.value[0].value;
  });
}
</script>

<style scoped></style>
