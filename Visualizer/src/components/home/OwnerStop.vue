<template>
  <n-grid :cols="1" y-gap="5">
    <n-grid-item>
      <n-select v-model:value="locationType" :options="options" placeholder="Type" filterable />
    </n-grid-item>
<!--    <n-grid-item v-if="value.type !== 'random'">-->
<!--      <owner-heatmap v-model="value" :dimension="dimension" :map-info="mapInfo" />-->
<!--    </n-grid-item>-->
  </n-grid>
</template>

<script setup>
import { computed } from "vue";
import OwnerHeatmap from "./OwnerStopMap.vue";

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

const location = computed(() => {
  return props.owner.locations[props.locationIndex];
});

const locationType = computed({
  get: () => location.value.type,
  set: (type) => (location.value.type = type),
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
