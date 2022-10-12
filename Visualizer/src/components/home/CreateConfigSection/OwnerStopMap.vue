<template>
  <n-grid :cols="1" y-gap="5">
    <n-grid-item>
      <n-select v-model:value="locationType" :options="options" placeholder="Type" filterable :disabled="disabled" />
    </n-grid-item>
    <n-grid-item>
      <component
        :is="componentMap[locationType]"
        :locationIndex="props.locationIndex"
        :ownerIndex="props.ownerIndex"
      />
    </n-grid-item>
  </n-grid>
</template>

<script setup>
import { computed } from "vue";

import { useComponentMapping } from "@/components/common/map/Map";
import { useSimulationConfigStore } from "@/stores/simulationConfigStore";

const props = defineProps({
  ownerIndex: {
    type: Number,
    required: true,
  },
  locationIndex: {
    type: Number,
    required: true,
  },
});

/**
 * Maps location type to component suited of filling the features of said type
 * @type {{random: string, heatmap: HeatmapMap, position: PointSelectionMap}}
 */
const componentMap = useComponentMapping();
const simulationConfig = useSimulationConfigStore();

const owner = computed(() => simulationConfig.owners[props.ownerIndex]);

const location = computed(() => {
  return owner.value.locations[props.locationIndex];
});

const locationType = computed({
  get: () => location.value.type,
  set: (type) => {
    location.value.type = type;
    location.value.points = [];
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
