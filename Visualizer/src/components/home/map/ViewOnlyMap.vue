<template>
  <div ref="mapRoot" :style="{ width: `${size}px`, height: `${size}px` }" class="map" />
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useBaseLayer, useMap, usePositionLayer } from "./Map";
import { createBox } from "ol/interaction/Draw";
import { Draw } from "ol/interaction";
import { Collection } from "ol";
import { useSimulationConfigStore } from "@/stores/simulationConfig";

const simulationConfig = useSimulationConfigStore();
defineProps({
  size: {
    type: Number,
    required: false,
    default: 256,
  },
});

const mapRoot = ref(null);
const baseLayer = useBaseLayer();
const features = new Collection([]);
const positionLayer = usePositionLayer(features);

const { map, render } = useMap(mapRoot, [baseLayer, positionLayer]);

const rectangleInteraction = new Draw({
  source: positionLayer.getSource(),
  type: "Circle",
  geometryFunction: function (coordinates, geometry) {
    features.pop();
    const resGeometry = createBox()(coordinates, geometry);
    const firstPoint = coordinates[0];
    const secondPoint = coordinates[1];
    if (firstPoint.lat > secondPoint.lat) {
      let min_lat = secondPoint.lat;
      secondPoint.lat = firstPoint.lat;
      firstPoint.lat = min_lat;
    }
    if (firstPoint.long > secondPoint.long) {
      let min_long = secondPoint.long;
      secondPoint.long = firstPoint.long;
      firstPoint.long = min_long;
    }
    // const bottomLeft = fromLonLat([firstPoint.long, firstPoint.lat], "EPSG:3857");
    // const topRight = fromLonLat([secondPoint.long, secondPoint.lat], "EPSG:3857");
    // simulationConfig.setMapSubTile(bottomLeft, topRight);
    simulationConfig.setMapSubTile(firstPoint, secondPoint);
    return resGeometry;
  },
});
onMounted(() => {
  render();
  map.value.addInteraction(rectangleInteraction);
});
</script>

<style scoped>
.map {
  overflow: hidden;
  border-radius: 5px;
}
</style>
