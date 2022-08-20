<template>
  <div ref="mapRoot" :style="{ width: `${size}px`, height: `${size}px` }" class="map" />
</template>

<script setup>
import { onMounted, ref, watch } from "vue";
import { useBaseLayer, useMap, usePositionLayer } from "./Map";
import { createBox } from "ol/interaction/Draw";
import { Draw } from "ol/interaction";
import { Collection, Feature } from "ol";
import { useSimulationConfigStore } from "@/stores/simulationConfig";
import { fromLonLat, toLonLat } from "ol/proj";
import { fromExtent } from "ol/geom/Polygon";

const simulationConfig = useSimulationConfigStore();
defineProps({
  size: {
    type: Number,
    required: false,
    default: 256,
  },
});

let firstClick = true;

const mapRoot = ref(null);
const baseLayer = useBaseLayer();
const features = new Collection([]);
const positionLayer = usePositionLayer(features);

const { map, render } = useMap(mapRoot, [baseLayer, positionLayer]);

const rectangleInteraction = new Draw({
  source: positionLayer.getSource(),
  type: "Circle",
  geometryFunction: createBox(),
});

onMounted(() => {
  render();
  map.value.on("click", () => {
    if (firstClick) {
      features.clear();
      firstClick = false;
    } else {
      const extent = features.item(0).getGeometry().getExtent();
      const bottomLeft = [extent[0], extent[1]];
      const topRight = [extent[2], extent[3]];
      simulationConfig.setMapSubTile(toLonLat(bottomLeft), toLonLat(topRight));
      firstClick = true;
    }
  });
  map.value.addInteraction(rectangleInteraction);
});
watch(simulationConfig.map.subselection, () => {
  fromConfig();
});

function fromConfig() {
  const extent = features.item(0).getGeometry().getExtent();
  const bottomLeft = [extent[0], extent[1]];
  const topRight = [extent[2], extent[3]];
  console.log(simulationConfig.map.subselection?.bottomLeft, toLonLat(bottomLeft));
  if (
    //Todo Kinda ugly
    Math.abs(fromLonLat(simulationConfig.map.subselection?.bottomLeft)[0] - bottomLeft[0]) > 0.00001 ||
    Math.abs(fromLonLat(simulationConfig.map.subselection?.bottomLeft)[1] - bottomLeft[1]) > 0.00001 ||
    Math.abs(fromLonLat(simulationConfig.map.subselection?.topRight)[0] - topRight[0]) > 0.00001 ||
    Math.abs(fromLonLat(simulationConfig.map.subselection?.topRight)[1] - topRight[1]) > 0.00001
  ) {
    features.clear();
    const bottomLeft = fromLonLat(simulationConfig.map.subselection.bottomLeft);
    const topRight = fromLonLat(simulationConfig.map.subselection.topRight);
    features.push(
      new Feature({
        geometry: fromExtent([...bottomLeft, ...topRight]),
      })
    );
    firstClick = true;
  }
}
</script>

<style scoped>
.map {
  overflow: hidden;
  border-radius: 5px;
}
</style>
