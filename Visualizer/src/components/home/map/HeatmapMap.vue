<template>
  <div ref="mapRoot" :style="{ width: `${size}px`, height: `${size}px` }" class="map" />
</template>

<script setup>
import { onMounted, ref } from "vue";
import { restoreHeatmapFeatures, useBaseLayer, useHeatmapInteraction, useHeatmapLayer, useMap } from "./Map";
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
  disabled: {
    type: Boolean,
    default: false,
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
  if (!props.disabled) {
    useHeatmapInteraction(map, min, meterCoordsRatio, features, props.location);
  }
});
</script>

<style scoped>
.map {
  overflow: hidden;
  border-radius: 5px;
}
</style>
