<template>
  <n-grid cols="8" x-gap="12">
    <n-grid-item span="5">
      <n-grid cols="3" x-gap="12">
        <!-- Address Input -->
        <n-grid-item span="3">
          <n-form-item>
            <template #label>
              <help v-bind="hAddress">Address</help>
            </template>
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

        <!-- Dimension Height Input -->
        <n-grid-item span="1">
          <n-form-item>
            <template #label>
              <help v-bind="hHeight">Height (m)</help>
            </template>
            <n-input-number v-model:value="simulationConfig.map.height" :min="20" :max="1000" :step="10" />
          </n-form-item>
        </n-grid-item>

        <n-grid-item span="1">
          <n-form-item>
            <template #label>
              <help v-bind="hVoxelSize">Voxel size (m)</help>
            </template>
            <n-slider v-model:value="simulationConfig.map.resolution" :max="20" :min="1" :step="1" />
          </n-form-item>
        </n-grid-item>
        <!-- Surrounding Tiles Input -->
        <n-grid-item span="1">
          <n-form-item>
            <template #label>
              <help v-bind="hSurroundingTiles">Surrounding Tiles</help>
            </template>
            <n-input-number v-model:value="simulationConfig.map.neighbouringTiles" clearable :min="0" :max="3" />
          </n-form-item>
        </n-grid-item>

        <!-- Minimum flying height  -->
        <n-grid-item span="1">
          <n-form-item>
            <template #label>
              <help v-bind="hMinHeight">Min height</help>
            </template>
            <n-input-number v-model:value="simulationConfig.map.minHeight" clearable :min="0" :max="100" />
          </n-form-item>
        </n-grid-item>
        <!--    Allocation Period    -->
        <n-grid-item span="2">
          <n-form-item>
            <template #label>
              <help v-bind="hAllocationPeriod">Allocation Period</help>
            </template>
            <n-slider
              v-model:value="allocationPeriod"
              :max="Math.pow(simulationConfig.map.timesteps, 1 / 3)"
              :min="1"
              :step="0.01"
              :format-tooltip="formatAllocationPeriodSlider"
              v-on:mouseup="updateAllocationPeriod"
            />
          </n-form-item>
        </n-grid-item>
      </n-grid>
    </n-grid-item>

    <n-grid-item span="3">
      <view-only-map :width="224">
        <n-form-item style="margin-top: 5px">
          <template #label>
            <help v-bind="hMapSelection">
              <span style="font-style: italic">
                (Optional) Select Area on Map
              </span>
            </help>
          </template>
        </n-form-item>
      </view-only-map>
    </n-grid-item>
  </n-grid>
</template>

<script setup>
import OSM from "ol/source/OSM";
import axios from "axios";

import { onUnmounted, ref, watchEffect } from "vue";
import { fromLonLat, get, transformExtent } from "ol/proj";
import { NavigateCircleOutline } from "@vicons/ionicons5";
import { useMessage } from "naive-ui";

import ViewOnlyMap from "./ViewOnlyMap.vue";
import Help from "../help/help.vue";

import { useSimulationConfigStore } from "@/stores/simulationConfigStore";
import { offConfigLoaded, onConfigLoaded } from "../../../scripts/emitter.js";
import {
  hAddress,
  hHeight,
  hVoxelSize,
  hSurroundingTiles,
  hMinHeight,
  hAllocationPeriod,
  hMapSelection,
} from "@/components/common/help/texts.js";

const message = useMessage();
const simulationConfig = useSimulationConfigStore();
const allocationPeriod = ref(Math.pow(simulationConfig.map.allocationPeriod, 1 / 3));

// OSM Source and grid definitions
const source = new OSM();
const grid = source.getTileGrid();

// Prefilled address query
const addressQuery = ref("Zurich, Switzerland");

onConfigLoaded(() => {
  allocationPeriod.value = Math.pow(simulationConfig.map.allocationPeriod, 1 / 3);
});

// Watch change in map config (zoom, address, etc.) and recalculate tiles and topLeft/bottomRight coordinates
watchEffect(() => {
  simulationConfig.map.locationName = addressQuery.value;
  const tiles = [];
  const projectedCoordinate = fromLonLat(
    [simulationConfig.map.coordinates.long, simulationConfig.map.coordinates.lat],
    "EPSG:3857"
  );
  const tileCoord = grid.getTileCoordForCoordAndZ(projectedCoordinate, 15);
  let bottomLeftCoordinate, topRightCoordinate;
  const n = simulationConfig.map.neighbouringTiles;
  for (let i = -n; i <= n; i++) {
    for (let j = -n; j <= n; j++) {
      const updatedTileCord = [tileCoord[0], tileCoord[1] + j, tileCoord[2] + i];
      tiles.push(updatedTileCord);
      if (i === n && j === -n) {
        const projectedExtent = grid.getTileCoordExtent(updatedTileCord);
        const extent = transformExtent(projectedExtent, get("EPSG:3857"), get("EPSG:4326"));
        bottomLeftCoordinate = { lat: extent[1], long: extent[0] };
      }
      if (i === -n && j === n) {
        const projectedExtent = grid.getTileCoordExtent(updatedTileCord);
        const extent = transformExtent(projectedExtent, get("EPSG:3857"), get("EPSG:4326"));
        topRightCoordinate = { lat: extent[3], long: extent[2] };
      }
    }
  }
  simulationConfig.map.tiles = tiles;
  simulationConfig.map.topRightCoordinate = topRightCoordinate;
  simulationConfig.map.bottomLeftCoordinate = bottomLeftCoordinate;
});

/**
 * Resolves map coordinate from address input
 * @returns {Promise<void>}
 */
const resolveAddress = async () => {
  const query = `https://nominatim.openstreetmap.org/search?q=${addressQuery.value}&format=json&addressdetails=1`;
  const { data } = await axios.get(query);
  if (!data.length || data.length === 0) {
    message.error("No address found for input query");
  }
  addressQuery.value = data[0].display_name;
  simulationConfig.map.coordinates.lat = parseFloat(data[0].lat);
  simulationConfig.map.coordinates.long = parseFloat(data[0].lon);
};

function formatAllocationPeriodSlider(value) {
  return `${Math.round(value ** 3, 0)}`;
}
function updateAllocationPeriod() {
  simulationConfig.map.allocationPeriod = Math.round(allocationPeriod.value ** 3);
}
onUnmounted(() => {
  offConfigLoaded();
});
</script>

<style scoped></style>
