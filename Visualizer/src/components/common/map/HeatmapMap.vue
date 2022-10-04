<template>
  <div>
    <div ref="mapRoot" :style="{ width: `${size.width}px`, height: `${size.height}px` }" class="map" />
    <n-form-item style="margin-top: 5px" v-if="!disabled">
      <template #label>
        <help v-bind="hHeatmap">
          <span style="font-style: italic"> Draw on map to create Heatmap </span>
        </help>
      </template>
    </n-form-item>
    <slot />
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { restoreHeatmapFeatures, useBaseLayer, useHeatmapInteraction, useHeatmapLayer, useMap } from "./Map";
import { Collection } from "ol";
import { useSimulationConfigStore } from "@/stores/simulationConfigStore";
import { computed } from "vue";
import Help from "@/components/common/help/help.vue";
import { hHeatmap } from "@/components/common/help/texts.js";

const props = defineProps({
  ownerIndex: {
    type: Number,
    required: true,
  },
  locationIndex: {
    type: Number,
    required: true,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  width: {
    type: Number,
    required: false,
    default: 400,
  },
});
const features = new Collection([]);
const simulationConfig = useSimulationConfigStore();

const mapRoot = ref(null);
const baseLayer = useBaseLayer();
const heatmapLayer = useHeatmapLayer(features);

const owner = computed(() => {
  return simulationConfig.owners[props.ownerIndex];
});
const { render, map, size } = useMap(mapRoot, [baseLayer, heatmapLayer], true, props.width);

onMounted(() => {
  restoreHeatmapFeatures(features, owner.value.locations[props.locationIndex].points);
  render();
  if (!props.disabled) {
    useHeatmapInteraction(map, features, owner.value.locations[props.locationIndex]);
  }
});
</script>

<style scoped>
.map {
  overflow: hidden;
  border-radius: 5px;
}
</style>
