<template>
  <div ref="map_root" :style="{ width: `${size}px`, height: `${size}px` }"></div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import TileLayer from "ol/layer/Tile";
import OSM from "ol/source/OSM";
import { boundingExtent } from "ol/extent";
import { fromLonLat } from "ol/proj";
import { View, Map, Feature, Collection } from "ol";
import { Heatmap } from "ol/layer";
import VectorSource from "ol/source/Vector";
import { Point } from "ol/geom";

const props = defineProps({
  topLeftCoordinate: Object,
  bottomRightCoordiante: Object,
  centerCoordinates: Object,
  tiles: Array,
  heatmap: {
    type: Boolean,
    required: false,
    default: false,
  },
  size: {
    type: Number,
    required: false,
    default: 256,
  },
});

const map_root = ref(null);
const min = computed(() => fromLonLat([props.topLeftCoordinate.long, props.topLeftCoordinate.lat]));
const max = computed(() => fromLonLat([props.bottomRightCoordiante.long, props.bottomRightCoordiante.lat]));
const extent = computed(() => boundingExtent([min.value, max.value]));
const center = computed(() => [(min.value[0] + max.value[0]) / 2, (min.value[1] + max.value[1]) / 2]);
const zoom = computed(() => {
  return Math.floor(15 / Math.sqrt(props.tiles.length));
});

const features = new Collection([
  new Feature(new Point(center.value)),
  new Feature(new Point(min.value)),
  new Feature(new Point(max.value)),
]);

const layers = computed(() => {
  const val = [
    // adding a background tiled layer
    new TileLayer({
      source: new OSM(), // tiles are served by OpenStreetMap
      zIndex: 0,
    }),
    new Heatmap({
      source: new VectorSource({
        features: features,
        radius: 20,
        zIndex: 1,
      }),
    }),
  ];
  if (!props.heatmap) {
    val.pop();
  }
  return val;
});

function renderMap() {
  if (map_root.value) {
    while (map_root.value.firstChild) {
      map_root.value.removeChild(map_root.value.firstChild);
    }
    // this is where we create the OpenLayers map
    const map = new Map({
      // the map will be created using the 'map-root' ref
      target: map_root.value,
      layers: layers.value,
      controls: [],
      interactions: [],

      // the map view will initially show the whole world
      view: new View({
        zoom: zoom.value,
        center: center.value,
        extent: extent.value,
        showFullExtent: true,
      }),
    });

    if (props.heatmap) {
      map.on("click", (event) => {
        features.push(new Feature(new Point(event.coordinate)));
        console.log(features);
      });
    }
  }
}

watch(extent, renderMap);
onMounted(renderMap);
</script>
