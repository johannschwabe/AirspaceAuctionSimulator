<template>
  <n-grid cols="8" x-gap="12">
    <n-grid-item span="5">
      <n-grid cols="3" x-gap="12">
        <n-grid-item span="3">
          <n-form-item label="Address">
            <n-input-group>
              <n-input
                placeholder="Address Search"
                v-model:value="addressQuery"
                type="text"
                :style="{ width: '80%' }"
                @blur="resolveAddress"
                @keyup.enter="resolveAddress"
              >
                <template #prefix>
                  <n-icon :component="NavigateCircleOutline" />
                </template>
              </n-input>
              <n-button type="primary" ghost :style="{ width: '20%' }" @click="resolveAddress"> Search </n-button>
            </n-input-group>
          </n-form-item>
        </n-grid-item>
        <n-grid-item span="1">
          <n-form-item label="Dimension Lon (m)">
            <n-input-number :value="dimension.x" disabled />
          </n-form-item>
        </n-grid-item>
        <n-grid-item span="1">
          <n-form-item label="Height (m)">
            <n-input-number v-model:value="config.dimension.y" :min="20" :max="1000" :step="10" />
          </n-form-item>
        </n-grid-item>
        <n-grid-item span="1">
          <n-form-item label="Dimension Lat (m)">
            <n-input-number :value="dimension.z" disabled />
          </n-form-item>
        </n-grid-item>
        <n-grid-item span="1">
          <n-form-item label="Surrounding Tiles">
            <n-input-number v-model:value="surroundingTiles" clearable :min="0" :max="3" />
          </n-form-item>
        </n-grid-item>
      </n-grid>
    </n-grid-item>

    <n-grid-item span="3">
      <map-viewer />
    </n-grid-item>
  </n-grid>
</template>

<script setup>
import OSM from "ol/source/OSM";
import axios from "axios";
import { ref, computed, watchEffect } from "vue";
import { fromLonLat, get, transformExtent } from "ol/proj";
import { NavigateCircleOutline } from "@vicons/ionicons5";
import { useMessage } from "naive-ui";

import MapViewer from "./MapViewer.vue";
import { useSimulationConfigStore } from "../../stores/simulationConfig";

const source = new OSM();
const grid = source.getTileGrid();
const SINGLE_TILE_SIDE_LENGTH = 830.8261666462096;

const message = useMessage();
const config = useSimulationConfigStore();

const surroundingTiles = ref(0);
const addressQuery = ref("Zurich, Switzerland");
const height = ref(100);

const dimension = computed(() => ({
  x: Math.ceil((surroundingTiles.value * 2 + 1) * SINGLE_TILE_SIDE_LENGTH),
  y: height.value,
  z: Math.ceil((surroundingTiles.value * 2 + 1) * SINGLE_TILE_SIDE_LENGTH),
}));

watchEffect(() => {
  config.map.locationName = addressQuery.value;
  config.map.neightbouringTiles = surroundingTiles.value;
  const tiles = [];
  const projectedCoordinate = fromLonLat([config.map.coordinates.long, config.map.coordinates.lat], "EPSG:3857");
  const tileCoord = grid.getTileCoordForCoordAndZ(projectedCoordinate, 15);
  let topLeftCoordinate, bottomRightCoordinate;
  const n = surroundingTiles.value;
  for (let i = -n; i <= n; i++) {
    for (let j = -n; j <= n; j++) {
      const updatedTileCord = [tileCoord[0], tileCoord[1] + j, tileCoord[2] + i];
      tiles.push(updatedTileCord);
      if (i === -n && j === -n) {
        const projectedExtent = grid.getTileCoordExtent(updatedTileCord);
        const extent = transformExtent(projectedExtent, get("EPSG:3857"), get("EPSG:4326"));
        topLeftCoordinate = { lat: extent[3], long: extent[0] };
      }
      if (i === n && j === n) {
        const projectedExtent = grid.getTileCoordExtent(updatedTileCord);
        const extent = transformExtent(projectedExtent, get("EPSG:3857"), get("EPSG:4326"));
        bottomRightCoordinate = { lat: extent[1], long: extent[2] };
      }
    }
  }
  config.map.tiles = tiles;
  config.map.topLeftCoordinate = topLeftCoordinate;
  config.map.bottomRightCoordinate = bottomRightCoordinate;
});

const resolveAddress = async () => {
  const query = `https://nominatim.openstreetmap.org/search?q=${addressQuery.value}&format=json&addressdetails=1`;
  const { data } = await axios.get(query);
  if (!data.length || data.length === 0) {
    message.error("No address found for input query");
  }
  addressQuery.value = data[0].display_name;
  config.map.coordinates.lat = parseFloat(data[0].lat);
  config.map.coordinates.long = parseFloat(data[0].lon);
};
</script>

<style scoped></style>
