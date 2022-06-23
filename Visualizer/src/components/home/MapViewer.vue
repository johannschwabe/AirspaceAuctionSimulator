<template>
  <div class="wrapper" :style="{ width: `${size}px`, heigth: `${size}px` }">
    <img
      v-for="tile in tiles"
      :key="tile"
      :src="tile"
      alt="OSM Tile"
      :width="dim"
      :height="dim"
      class="tile"
      :style="{ width: dim, height: dim }"
    />
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  tiles: Array,
  size: {
    type: Number,
    required: false,
    default: 256,
  },
});

const dim = computed(() => {
  return Math.floor(props.size / Math.sqrt(props.tiles.length));
});
</script>

<style scoped>
.wrapper {
  display: flex;
  flex-flow: row wrap;
  justify-content: flex-start;
  align-items: flex-start;
  align-content: flex-start;
  gap: 0;
}
.tile {
  image-rendering: pixelated;
}
</style>
