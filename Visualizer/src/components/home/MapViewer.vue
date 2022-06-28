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
import VectorLayer from "ol/layer/Vector";

const props = defineProps({
  topLeftCoordinate: {
    type: Object,
    required: true,
  },
  bottomRightCoordiante: {
    type: Object,
    required: true,
  },
  centerCoordinates: {
    type: Object,
    required: true,
  },
  tiles: {
    type: Array,
    required: true,
  },
  selection: {
    type: String,
    required: false,
    default: null,
  },
  size: {
    type: Number,
    required: false,
    default: 256,
  },
  dimension: {
    type: Object,
    required: true,
  },
  position: {
    type: String,
    required: false,
    default: null,
  },
  heatmap: {
    type: Object,
    required: false,
    default: () => ({}),
  },
});

const selectionType = computed(() => props.selection);
const map_root = ref(null);
const topLeft = computed(() => fromLonLat([props.topLeftCoordinate.long, props.topLeftCoordinate.lat]));
const bottomRight = computed(() => fromLonLat([props.bottomRightCoordiante.long, props.bottomRightCoordiante.lat]));
const extent = computed(() => boundingExtent([topLeft.value, bottomRight.value]));
const min = computed(() => extent.value.slice(0, 2));
const max = computed(() => extent.value.slice(2, 4));
const dimensions = computed(() => [max.value[0] - min.value[0], max.value[1] - min.value[1]]);
const meterCoordsRatio = computed(() => dimensions.value[0] / props.dimension.x);
const center = computed(() => [
  (topLeft.value[0] + bottomRight.value[0]) / 2,
  (topLeft.value[1] + bottomRight.value[1]) / 2,
]);
const zoom = computed(() => {
  return Math.floor(15 / Math.sqrt(props.tiles.length));
});

const features = new Collection([]);
const position = new Collection([]);

const layers = computed(() => {
  const val = [
    // adding a background tiled layer
    new TileLayer({
      source: new OSM(), // tiles are served by OpenStreetMap
      zIndex: 0,
    }),
  ];
  if (props.selection !== null) {
    if (props.selection === "heatmap") {
      val.push(
        new Heatmap({
          source: new VectorSource({
            features: features,
          }),
        })
      );
    }
    if (props.selection === "position") {
      val.push(
        new VectorLayer({
          source: new VectorSource({
            features: position,
          }),
        })
      );
    }
  }
  return val;
});

const positionCoordinates = ref(props.position);
const heatmapCoordinates = ref(props.heatmap);

let map = null;

function renderMap() {
  // this is where we create the OpenLayers map
  map = new Map({
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

  if (props.selection !== null) {
    map.on("click", onClickOrDrag);
    map.on("pointerdrag", onClickOrDrag);
  }
}

const emit = defineEmits(["update:position", "update:heatmap"]);

function onClickOrDrag(event) {
  const coords = event.coordinate;
  const gridCoords = [
    Math.floor((coords[0] - min.value[0]) / meterCoordsRatio.value),
    Math.floor((coords[1] - min.value[1]) / meterCoordsRatio.value),
  ];
  if (
    gridCoords[0] >= 0 &&
    gridCoords[1] >= 0 &&
    gridCoords[0] < props.dimension.x &&
    gridCoords[1] < props.dimension.z
  ) {
    const key = `${gridCoords[0]}_${gridCoords[1]}`;
    if (props.selection === "position") {
      positionCoordinates.value = key;
      position.pop();
      position.push(new Feature(new Point(coords)));
      emit("update:position", positionCoordinates.value);
    } else if (props.selection === "heatmap") {
      if (heatmapCoordinates.value[key] !== undefined) {
        if (heatmapCoordinates.value[key] >= 1) {
          return;
        }
        heatmapCoordinates.value[key] = Math.round(heatmapCoordinates.value[key] * 10 + 1) / 10;
      } else {
        heatmapCoordinates.value[key] = 0.1;
      }
      features.push(new Feature(new Point(coords)));
      emit("update:heatmap", heatmapCoordinates.value);
    }
  }
}

watch(selectionType, () => {
  if (map !== null) {
    map.setLayers(layers.value);
  }
});

watch(extent, () => {
  if (map !== null) {
    map.setView(
      new View({
        zoom: zoom.value,
        center: center.value,
        extent: extent.value,
        showFullExtent: true,
      })
    );
  }
});
onMounted(renderMap);
</script>
