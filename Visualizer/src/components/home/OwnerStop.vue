<template>
  <n-grid :cols="1" y-gap="5">
    <n-grid-item>
      <n-select v-model:value="value.type" :options="options" placeholder="Type" filterable />
    </n-grid-item>
    <n-grid-item v-if="value.type !== 'random'">
      <owner-heatmap v-model="value" :dimension="dimension" :map-info="mapInfo" />
    </n-grid-item>
  </n-grid>
</template>

<script setup>
import { ref, watchEffect } from "vue";
import OwnerHeatmap from "./OwnerStopMap.vue";

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
  dimension: {
    type: Object,
    required: true,
  },
  mapInfo: {
    type: Object,
    required: true,
  },
});

const value = ref({ ...props.modelValue });
watchEffect(() => (value.value = props.modelValue));
watchEffect(() => updateValue(value.value));
function updateValue(updatedValue) {
  emit("update:modelValue", updatedValue);
}
const emit = defineEmits(["update:modelValue"]);

const options = [
  {
    label: "Random",
    value: "random",
  },
  {
    label: "Position",
    value: "position",
  },
  {
    label: "Heatmap",
    value: "heatmap",
  },
];
</script>

<style scoped></style>
