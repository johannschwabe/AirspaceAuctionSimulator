<template>
  <owner-form v-model="config" :options="options" />
  <span v-if="nr_stops.max === undefined || nr_stops.max > 0 || nr_stops.start">
    <h3>Start:</h3>
    <div style="margin-left: 5px">
      <owner-stop v-model="config.start.stop" :dimension="dimension" :map-info="mapInfo" /></div
  ></span>
  <span v-if="nr_stops.max > 0 || nr_stops.max === undefined">
    <h3>Stops:</h3>
    <div style="margin-left: 5px">
      <n-dynamic-input v-model:value="config.stops" :on-create="onCreate" :max="nr_stops.max">
        <template #default="{ value }">
          <owner-stop v-model="value.stop" :dimension="dimension" :map-info="mapInfo" />
        </template>
      </n-dynamic-input>
    </div>
  </span>
  <span v-if="nr_stops.max === undefined || nr_stops.max > 1 || nr_stops.start">
    <h3>Target:</h3>
    <div style="margin-left: 5px">
      <owner-stop v-model="config.target.stop" :dimension="dimension" :map-info="mapInfo" />
    </div>
  </span>
</template>

<script setup>
import { computed, ref, watchEffect } from "vue";
import OwnerForm from "./OwnerForm.vue";
import OwnerStop from "./OwnerStop.vue";
import { createDefaultStop } from "../../scripts/stops";

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

const config = ref({ ...props.modelValue });
watchEffect(() => (config.value = props.modelValue));
watchEffect(() => updateValue(config.value));
const emit = defineEmits(["update:modelValue"]);
const nr_stops = computed(() => {
  const res = {
    min: 1,
    max: undefined,
    start: props.options[config.value.type].ownertype === "PathOwner",
  };
  const raw = props.options[config.value.type].positions;
  console.log(raw);
  raw
    .split(";")
    .map((cond) => cond.trim())
    .forEach((condition) => {
      if (condition.startsWith(">")) {
        res.min = parseInt(condition.substring(1)) + 1 - (res.start ? 2 : 0);
      } else if (condition.startsWith("<")) {
        console.log(condition.substring(1));
        res.max = parseInt(condition.substring(1)) - 1 - (res.start ? 2 : 0);
      } else {
        res.max = parseInt(condition) - (res.start ? 2 : 0);
        res.min = parseInt(condition) - (res.start ? 2 : 0);
      }
    });
  return res;
});
function updateValue(updatedValue) {
  emit("update:modelValue", updatedValue);
}
</script>
