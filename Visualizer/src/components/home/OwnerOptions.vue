<template>
  <owner-form v-model="config" :options="options" />
  <div v-if="nr_stops.start">
    <h3>Start:</h3>
    <div style="margin-left: 5px">
      <owner-stop v-model="config.start.stop" :dimension="dimension" :map-info="mapInfo" />
    </div>
  </div>
  <div v-if="nr_stops.max > 0 || nr_stops.max === undefined">
    <h3>Stops:</h3>
    <div style="margin-left: 5px">
      <n-dynamic-input v-model:value="config.stops" :on-create="onCreate" :max="nr_stops.max">
        <template #default="{ value }">
          <owner-stop v-model="value.stop" :dimension="dimension" :map-info="mapInfo" />
        </template>
      </n-dynamic-input>
    </div>
  </div>
  <div v-if="nr_stops.start">
    <h3>Target:</h3>
    <div style="margin-left: 5px">
      <owner-stop v-model="config.target.stop" :dimension="dimension" :map-info="mapInfo" />
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import OwnerForm from "./OwnerForm.vue";
import OwnerStop from "./OwnerStop.vue";
import { createDefaultStop, validStops } from "../../scripts/stops";

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
  mapInfo: {
    type: Object,
    required: false,
    default: null,
  },
  dimension: {
    type: Object,
    required: true,
  },
  options: {
    type: Object,
    required: true,
  },
});

const onCreate = () => {
  return createDefaultStop();
};

const config = computed({
  get: () => props.modelValue,
  set: (updatedValue) => emit("update:modelValue", updatedValue),
});

const emit = defineEmits(["update:modelValue"]);

const nr_stops = computed(() => {
  const option = props.options[config.value.type];
  return validStops(option.minLocations, option.maxLocations, option.ownerType);
});
</script>
