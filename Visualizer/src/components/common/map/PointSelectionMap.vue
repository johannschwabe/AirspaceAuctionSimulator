<template>
  <div>
    <div ref="mapRoot" :style="{ width: `${size.width}px`, height: `${size.height}px` }" class="map" />
    <n-form-item style="margin-top: 5px" v-if="!disabled">
      <template #label>
        <help v-bind="hPositonMap">
          <span style="font-style: italic"> Click on map to place location marker </span>
        </help>
      </template>
    </n-form-item>
    <slot />
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from "vue";
import { restorePositionFeatures, useBaseLayer, useMap, usePositionInteraction, usePositionLayer } from "./Map";
import { Collection } from "ol";
import { useSimulationConfigStore } from "@/stores/simulationConfigStore";
import Help from "@/components/common/help/help.vue";
import { hPositonMap } from "@/components/common/help/texts";

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
const positionLayer = usePositionLayer(features);

const { render, size, map } = useMap(mapRoot, [baseLayer, positionLayer], true, props.width);

const owner = computed(() => {
  return simulationConfig.owners[props.ownerIndex];
});

onMounted(() => {
  restorePositionFeatures(features, owner.value.locations[props.locationIndex].points);
  render();
  if (!props.disabled) {
    usePositionInteraction(map, features, owner.value.locations[props.locationIndex]);
  }
});

onBeforeUnmount(() => {
  features.clear();
});
</script>

<style scoped>
.map {
  overflow: hidden;
  border-radius: 5px;
}
</style>
