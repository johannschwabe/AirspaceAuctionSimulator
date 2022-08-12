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

const ownerProperties = computed(() => {
  return simulationConfig.availableOwnersForAllocator.find((o) => o.name === owner.value.type);
});

const onCreate = (index) => {
  const location = simulationConfig.randomLocation();
  owner.value.locations.splice(index, 0, location);
  return location;
};

const onRemove = (index) => {
  owner.value.locations.splice(index, 1);
};
</script>
