<template>
  <div class="wrapper">
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
});

const dim = computed(() => {
  return Math.floor(256 / Math.sqrt(props.tiles.length));
});
</script>

<style scoped>
.wrapper {
  width: 256px;
  height: 256px;
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
