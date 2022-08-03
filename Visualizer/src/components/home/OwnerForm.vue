<template>
  <n-color-picker :modes="['hex']" :show-alpha="false" v-model:value="config.color" />
  <n-input v-model:value="config.name" type="text" placeholder="Owner Name" />
  <n-input-number v-model:value="config.agents" :min="1" :max="100" style="min-width: 130px" placeholder="Nr. Agents" />
  <n-select
    v-model:value="config.type"
    :options="Object.values(options)"
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

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
  options: {
    type: Object,
    required: true,
  },
});

const config = computed({
  get: () => props.modelValue,
  set: (updatedValue) => emit("update:modelValue", updatedValue),
});
const emit = defineEmits(["update:modelValue"]);

function defaultStops(ownertype) {
  const option = props.options[ownertype];
  const nr_stops = validStops(option.positions, option.ownertype);
  if (nr_stops.start) {
    config.value.start = createDefaultStop();
    config.value.target = createDefaultStop();
  } else {
    config.value.start = null;
    config.value.target = null;
  }
  config.value.stops = [];
  for (let i = 0; i < nr_stops.min; i++) {
    config.value.stops.push(createDefaultStop());
  }
}
</script>

<style scoped></style>
