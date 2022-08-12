<template>
  <p>
    <b>{{ ownerProperties.label }} Owner: </b>{{ ownerProperties.description }}
  </p>
  <h3>Stops:</h3>
  <n-dynamic-input
    :value="owner.locations"
    :on-create="onCreate"
    :on-remove="onRemove"
    :min="owner.minLocations"
    :max="owner.maxLocations"
  >
    <template #default="{ index }">
      <owner-stop :owner="owner" :locationIndex="index" />
    </template>
  </n-dynamic-input>
</template>

<script setup>
import { computed } from "vue";
import OwnerStop from "./OwnerStop.vue";
import { useSimulationConfigStore } from "../../../stores/simulationConfig";

const props = defineProps({
  ownerIndex: {
    type: Number,
    required: true,
  },
});

const simulationConfig = useSimulationConfigStore();

const owner = computed(() => simulationConfig.owners[props.ownerIndex]);

/**
 * Returns config of owner of fitting type
 * @type {ComputedRef<OwnerConfig>}
 */
const ownerProperties = computed(() => {
  return simulationConfig.availableOwnersForAllocator.find((o) => o.name === owner.value.type);
});

/**
 * Creates a new random location at given index
 * @param {number} index
 * @returns {LocationConfig}
 */
const onCreate = (index) => {
  const location = simulationConfig.randomLocation();
  owner.value.locations.splice(index, 0, location);
  return location;
};

/**
 * Removes location at given index
 * @param {number} index
 */
const onRemove = (index) => {
  owner.value.locations.splice(index, 1);
};
</script>
