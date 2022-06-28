<template>
  <map-viewer
    :map-info="mapInfo"
    :size="512"
    :dimension="dimension"
    :stop="value"
    @update:position="updatePosition"
    @update:heatmap="updateHeatmap"
  />
</template>

<script setup>
import MapViewer from "./MapViewer.vue";
import { ref, watchEffect } from "vue";

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
  mapInfo: {
    type: Object,
    required: true,
  },
  dimension: {
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

function updatePosition(position) {
  value.value.position = position;
}
function updateHeatmap(heatmap) {
  value.value.heatmap = heatmap;
}
</script>
