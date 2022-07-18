<template>
  <div ref="map_root" :style="{ width: `${size}px`, height: `${size}px` }" />
  <n-button ghost v-if="selectionType === 'heatmap'" @click="onClear" style="width: 100%; margin-top: 5px"
    >clear</n-button
  >
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import TileLayer from "ol/layer/Tile";
import OSM from "ol/source/OSM";
import { boundingExtent } from "ol/extent";
import { fromLonLat } from "ol/proj";
import { View, Map, Feature } from "ol";
import { Heatmap } from "ol/layer";
import VectorSource from "ol/source/Vector";
import { Point } from "ol/geom";
import VectorLayer from "ol/layer/Vector";

const props = defineProps({
  mapInfo: {
    type: Object,
    required: true,
  },
  stop: {
    type: Object,
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
});

const selectionType = computed(() => props.stop?.type);
const map_root = ref(null);
const topLeft = computed(() => fromLonLat([props.mapInfo.topLeftCoordinate.long, props.mapInfo.topLeftCoordinate.lat]));
const bottomRight = computed(() =>
  fromLonLat([props.mapInfo.bottomRightCoordinate.long, props.mapInfo.bottomRightCoordinate.lat])
);
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
  return Math.floor(15 / Math.sqrt(props.mapInfo.tiles.length));
});
const positionValue = { ...props.stop?.position };
const heatmapValue = { ...props.stop?.heatmap };

const tileLayer = new TileLayer({
  // tiles are served by OpenStreetMap
  source: new OSM(),
  zIndex: 0,
});

const layers = computed(() => {
  const val = [
    // adding a background tiled layer
    tileLayer,
  ];
  switch (selectionType.value) {
    case "heatmap":
      val.push(
        // adding a heatmap layer to display created heatmap
        new Heatmap({
          source: new VectorSource({
            features: heatmapValue.features,
          }),
        })
      );
      break;
    case "position":
      val.push(
        // adding a vector layer to display selected position
        new VectorLayer({
          source: new VectorSource({
            features: positionValue.features,
          }),
        })
      );
      break;
    default:
      break;
  }
  return val;
});

let map = null;

function renderMap() {
  // this is where we create the OpenLayers map
  map = new Map({
    // the map will be created using the 'map-root' ref
    target: map_root.value,
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

  if (selectionType.value !== null) {
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
    gridCoords[1] < props.dimension.x &&
    gridCoords[0] < props.dimension.z
  ) {
    // Inverted x coordinate
    const key = `${props.dimension.x - gridCoords[1]}_${gridCoords[0]}`;
    switch (selectionType.value) {
      case "heatmap":
        if (heatmapValue.keys[key] !== undefined) {
          if (heatmapValue.keys[key] >= 1) {
            break;
          }
          heatmapValue.keys[key] = Math.round(heatmapValue.keys[key] * 10 + 1) / 10;
        } else {
          heatmapValue.keys[key] = 0.1;
        }
        heatmapValue.features.push(new Feature(new Point(coords)));
        emit("update:heatmap", heatmapValue);
        break;
      case "position":
        positionValue.key = key;
        positionValue.features.pop();
        positionValue.features.push(new Feature(new Point(coords)));
        emit("update:position", positionValue);
        break;
      default:
        break;
    }
  } else {
    throw new Error(`Invalid coordinates selected: ${coords} map to ${gridCoords}`);
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

function onClear() {
  heatmapValue.features.clear();
  heatmapValue.keys = {};
}
</script>
