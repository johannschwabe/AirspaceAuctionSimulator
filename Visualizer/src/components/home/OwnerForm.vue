<template>
  <n-color-picker :modes="['hex']" :show-alpha="false" v-model:value="owner.color" />
  <n-input v-model:value="owner.name" type="text" placeholder="Owner Name" />
  <n-input-number v-model:value="owner.agents" :min="1" :max="100" style="min-width: 130px" placeholder="Nr. Agents" />
  <n-select
    v-model:value="owner.type"
    :options="Object.values(config.availableOwnersForMechanism)"
    label-field="_label"
    value-field="classname"
    placeholder="Type"
    filterable
    @update:value="defaultStops"
  />
</template>

<script setup>
import { computed } from "vue";
import { createDefaultStop, validStops } from "../../scripts/stops";
import { useSimulationConfigStore } from "../../stores/simulationConfig";

const props = defineProps({
  owner: {
    type: Object,
    required: true,
  },
});

const config = useSimulationConfigStore();

const owner = computed({
  get: () => props.modelValue,
  set: (updatedValue) => emit("update:owner", updatedValue),
});
const emit = defineEmits(["update:owner"]);

function defaultStops(ownertype) {
  const option = config.availableOwnersForMechanism[ownertype];
  const nr_stops = validStops(option.positions, option.ownertype);
  if (nr_stops.start) {
    owner.value.start = createDefaultStop();
    owner.value.target = createDefaultStop();
  } else {
    owner.value.start = null;
    owner.value.target = null;
  }
  owner.value.stops = [];
  for (let i = 0; i < nr_stops.min; i++) {
    owner.value.stops.push(createDefaultStop());
  }
}
</script>

<style scoped></style>
