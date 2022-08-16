<template>
  <div ref="mapRoot" :style="{ width: `${size}px`, height: `${size}px` }" class="map" />
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";
import { restorePositionFeatures, useBaseLayer, useMap, usePositionInteraction, usePositionLayer } from "./Map";
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
const positionLayer = usePositionLayer(features);

const { render, map, min, meterCoordsRatio } = useMap(mapRoot, [baseLayer, positionLayer]);

onMounted(() => {
  restorePositionFeatures(features, props.location.gridCoordinates);
  render();
  if (!props.disabled) {
    usePositionInteraction(map, min, meterCoordsRatio, features, props.location);
  }
});

onBeforeUnmount(() => {
  features.clear();
});
</script>

<style scoped>
.map {
  overflow: hidden;
  border-radius: 5px;
}
</style>
