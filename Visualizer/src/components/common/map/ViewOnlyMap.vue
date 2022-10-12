<template>
  <div>
    <div ref="mapRoot" :style="{ width: `${size.width}px`, height: `${size.height}px` }" class="map" />
    <slot />
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from "vue";
import { useBaseLayer, useMap, usePositionLayer } from "./Map";
import { createBox } from "ol/interaction/Draw";
import { Draw } from "ol/interaction";
import { Collection, Feature } from "ol";
import { useSimulationConfigStore } from "@/stores/simulationConfigStore";
import { fromLonLat, toLonLat } from "ol/proj";
import { fromExtent } from "ol/geom/Polygon";
import { offConfigLoaded, onConfigLoaded } from "../../../scripts/emitter";

const simulationConfig = useSimulationConfigStore();
const props = defineProps({
  disabled: {
    type: Boolean,
    required: false,
    default: false,
  },
  width: {
    type: Number,
    required: false,
    default: 400,
  },
  subselection: {
    type: Boolean,
    required: false,
    default: false,
  },
});

let firstClick = true;

const mapRoot = ref(null);
const baseLayer = useBaseLayer();
const features = new Collection([]);
const positionLayer = usePositionLayer(features);

const { map, render, size } = useMap(mapRoot, [baseLayer, positionLayer], props.subselection, props.width);

const rectangleInteraction = new Draw({
  source: positionLayer.getSource(),
  type: "Circle",
  geometryFunction: createBox(),
});

onMounted(() => {
  fromConfig();
  render();
  if (!props.disabled) {
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
  }
});
onConfigLoaded(fromConfig);
onUnmounted(offConfigLoaded);

function fromConfig() {
  if (!simulationConfig.map.subselection?.bottomLeft || !simulationConfig.map.subselection?.topRight) {
    return;
  }
  const nothingSelected = features.getLength() === 0;
  let selectionChanged = false;

  const bottomLeftNewPM = fromLonLat([
    simulationConfig.map.subselection?.bottomLeft.long,
    simulationConfig.map.subselection?.bottomLeft.lat,
  ]);
  const topRightNewPM = fromLonLat([
    simulationConfig.map.subselection?.topRight.long,
    simulationConfig.map.subselection?.topRight.lat,
  ]);
  if (!nothingSelected) {
    const extent = features.item(0).getGeometry().getExtent();
    const bottomLeftCurrent = [extent[0], extent[1]];
    const topRightCurrent = [extent[2], extent[3]];

    const roundingError = 0.001;
    selectionChanged =
      Math.abs(bottomLeftNewPM[0] - bottomLeftCurrent[0]) > roundingError ||
      Math.abs(bottomLeftNewPM[1] - bottomLeftCurrent[1]) > roundingError ||
      Math.abs(topRightNewPM[0] - topRightCurrent[0]) > roundingError ||
      Math.abs(topRightNewPM[1] - topRightCurrent[1]) > roundingError;
  }
  if (!props.subselection && (selectionChanged || nothingSelected)) {
    features.clear();
    features.push(
      new Feature({
        geometry: fromExtent([...bottomLeftNewPM, ...topRightNewPM]),
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
