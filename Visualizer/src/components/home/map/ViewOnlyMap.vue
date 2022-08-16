<template>
  <div ref="mapRoot" :style="{ width: `${size}px`, height: `${size}px` }" class="map" />
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useBaseLayer, useMap } from "./Map";

defineProps({
  size: {
    type: Number,
    required: false,
    default: 256,
  },
});

const mapRoot = ref(null);
const baseLayer = useBaseLayer();

const { render } = useMap(mapRoot, [baseLayer]);

onMounted(() => render());
</script>

<style scoped>
.map {
  overflow: hidden;
  border-radius: 5px;
}
</style>
