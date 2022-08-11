<template>
  <n-grid :cols="1" y-gap="5">
    <n-grid-item>
      <n-select v-model:value="locationType" :options="options" placeholder="Type" filterable />
    </n-grid-item>
    <n-grid-item>
      <component :is="componentMap[locationType]" :location="location" />
    </n-grid-item>
  </n-grid>
</template>

<script setup>
import { computed } from "vue";
import PointSelectionMap from "../StreetMaps/PointSelectionMap.vue";
import HeatmapMap from "../StreetMaps/HeatmapMap.vue";

const props = defineProps({
  owner: {
    type: Object,
    required: true,
  },
  locationIndex: {
    type: Number,
    required: true,
  },
});

const componentMap = {
  random: "span",
  position: PointSelectionMap,
  heatmap: HeatmapMap,
};

const location = computed(() => {
  return props.owner.locations[props.locationIndex];
});

const locationType = computed({
  get: () => location.value.type,
  set: (type) => {
    location.value.type = type;
    location.value.gridCoordinates = [];
  },
});

const options = [
  {
    label: "Random",
    value: "random",
  },
  {
    label: "Position",
    value: "position",
  },
  {
    label: "Heatmap",
    value: "heatmap",
  },
];
</script>

<style scoped></style>
