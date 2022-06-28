<template>
  <map-viewer
    id="map"
    :tiles="mapInfo.tiles"
    :center-coordinates="mapInfo.coordinates"
    :bottom-right-coordiante="mapInfo.bottomRightCoordiante"
    :top-left-coordinate="mapInfo.topLeftCoordinate"
    :size="512"
    :dimension="dimension"
    :selection="value.type"
    :position="value.position"
    :heatmap="value.heatmap"
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

function updatePosition(coords) {
  value.value.position = coords;
}
function updateHeatmap(coords) {
  value.value.heatmap = coords;
}
</script>
