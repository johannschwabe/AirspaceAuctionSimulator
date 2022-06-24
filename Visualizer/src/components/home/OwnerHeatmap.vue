<template>
  <map-viewer
    id="map"
    :tiles="mapInfo.tiles"
    :center-coordinates="mapInfo.coordinates"
    :bottom-right-coordiante="mapInfo.bottomRightCoordiante"
    :top-left-coordinate="mapInfo.topLeftCoordinate"
    :size="512"
    heatmap
  />
</template>

<script setup>
import { defineProps } from "vue";
import MapViewer from "./MapViewer.vue";

defineProps({
  mapInfo: {
    type: Object,
    required: false,
    default: null,
  },
});
</script>
