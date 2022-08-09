<template>
  <div ref="map_root" :style="{ width: `${size}px`, height: `${size}px` }" />
</template>

<script setup>
import { useSimulationConfigStore } from "../../stores/simulationConfig";
import { computed, ref, shallowRef, watch } from "vue";
import { fromLonLat } from "ol/proj";
import { boundingExtent } from "ol/extent";
import TileLayer from "ol/layer/Tile";
import OSM from "ol/source/OSM";
import { Map, View } from "ol";

defineProps({
  size: {
    type: Number,
    required: false,
    default: 256,
  },
});

const map = shallowRef(null);

const simulationConfig = useSimulationConfigStore();

const mapRoot = ref(null);

const topLeft = computed(() => {
  return fromLonLat([simulationConfig.map.topLeftCoordinate.long, simulationConfig.map.topLeftCoordinate.lat]);
});
const bottomRight = computed(() => {
  return fromLonLat([simulationConfig.map.bottomRightCoordinate.long, simulationConfig.map.bottomRightCoordinate.lat]);
});
const extent = computed(() => {
  return boundingExtent([topLeft.value, bottomRight.value]);
});
const min = computed(() => {
  return extent.value.slice(0, 2);
});
const max = computed(() => {
  return extent.value.slice(2, 4);
});
const dimensions = computed(() => {
  return [max.value[0] - min.value[0], max.value[1] - min.value[1]];
});
const meterCoordsRatio = computed(() => {
  return dimensions.value[0] / simulationConfig.dimension.x;
});
const center = computed(() => [
  (topLeft.value[0] + bottomRight.value[0]) / 2,
  (topLeft.value[1] + bottomRight.value[1]) / 2,
]);
const zoom = computed(() => {
  return Math.floor(15 / Math.sqrt(simulationConfig.map.tiles.length));
});

const tileLayer = new TileLayer({
  source: new OSM(),
  zIndex: 0,
});

const layers = computed(() => {
  return [
    // adding a background tiled layer
    tileLayer,
  ];
});

const useMap = () => {
  // this is where we create the OpenLayers map
  return new Map({
    // the map will be created using the 'map-root' ref
    target: mapRoot.value,
    layers: layers.value,
    controls: [],
    interactions: [],

    // the map view only shows the selected tiles
    view: new View({
      zoom: zoom.value,
      center: center.value,
      extent: extent.value,
      showFullExtent: true,
    }),
  });
};

watch(extent, () => {
  if (map.value !== null) {
    map.value.setView(
      new View({
        zoom: zoom.value,
        center: center.value,
        extent: extent.value,
        showFullExtent: true,
      })
    );
  }
});
</script>

<style scoped></style>
