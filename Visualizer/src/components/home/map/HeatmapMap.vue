<template>
  <div ref="mapRoot" :style="{ width: `${size}px`, height: `${size}px` }" />
</template>

<script setup>
import { onMounted, ref } from "vue";
import {
  restoreHeatmapFeatures,
  useBaseLayer,
  useHeatmapInteraction,
  useHeatmapLayer,
  useMap
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
const heatmapLayer = useHeatmapLayer(features);

const { render, map, min, meterCoordsRatio } = useMap(mapRoot, [baseLayer, heatmapLayer]);

onMounted(() => {
  restoreHeatmapFeatures(features, props.location.gridCoordinates);
  render();
  useHeatmapInteraction(map, min, meterCoordsRatio, features, props.location);
});
</script>

<style scoped></style>
