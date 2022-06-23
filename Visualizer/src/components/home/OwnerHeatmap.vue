<template>
  <map-viewer :tiles="tileUrls" :size="512" />
</template>

<script setup>
import OSM from "ol/source/OSM";
import { computed, defineProps } from "vue";
import { get } from "ol/proj";
import MapViewer from "./MapViewer.vue";

const props = defineProps({
  tiles: {
    type: Array,
    required: false,
    default: null,
  },
});

const source = new OSM();

const tileUrls = computed(() => {
  if (props.tiles) {
    const tileUrlFunction = source.getTileUrlFunction();
    return props.tiles.map((coord) => tileUrlFunction(coord, 1, get("EPSG:3857")));
  }
  return [];
});
</script>

<style scoped></style>
