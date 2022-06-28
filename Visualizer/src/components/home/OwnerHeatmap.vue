<template>
  <map-viewer
    id="map"
    :tiles="mapInfo.tiles"
    :center-coordinates="mapInfo.coordinates"
    :bottom-right-coordiante="mapInfo.bottomRightCoordiante"
    :top-left-coordinate="mapInfo.topLeftCoordinate"
    :size="512"
    :dimension="dimension"
    heatmap
  />
</template>

<script setup>
import MapViewer from "./MapViewer.vue";

defineProps({
  mapInfo: {
    type: Object,
    required: true,
  },
  dimension: {
    type: Object,
    required: true,
  },
});
</script>
