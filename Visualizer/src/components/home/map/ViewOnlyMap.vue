<template>
  <div ref="mapRoot" :style="{ width: `${size}px`, height: `${size}px` }" />
</template>

<script setup>
import { onMounted, ref } from "vue";
import { useBaseLayer, useMap } from "./Map";

const props = defineProps({
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

<style scoped></style>
