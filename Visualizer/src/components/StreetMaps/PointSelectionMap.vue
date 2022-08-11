<template>
  <div ref="mapRoot" :style="{ width: `${size}px`, height: `${size}px` }" />
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";
import {
  restoreHeatmapFeatures,
  restorePositionFeatures,
  useBaseLayer,
  useMap,
  usePositionInteraction,
  usePositionLayer
} from "./Map";
import { Collection } from "ol";

const props = defineProps({
  size: {
    type: Number,
    required: false,
    default: 256,
  },
  location: {
    type: Object,
    required: true,
  },
});

const features = new Collection([]);

const mapRoot = ref(null);
const baseLayer = useBaseLayer();
const positionLayer = usePositionLayer(features);

const { render, map, min, meterCoordsRatio } = useMap(mapRoot, [baseLayer, positionLayer]);

onMounted(() => {
  restorePositionFeatures(features, props.location.gridCoordinates);
  render();
  usePositionInteraction(map, min, meterCoordsRatio, features, props.location);
});

onBeforeUnmount(() => {
  features.clear();
});
</script>

<style scoped></style>
