import { ref, reactive, watchEffect, computed } from "vue";
import { defineStore } from "pinia";
import { cloneDeep } from "lodash-es";
import { getOwnersSupportedByAllocator, getSupportedAllocators } from "../API/api";

export const useSimulationConfigStore = defineStore("simulationConfig", () => {
  const name = ref("");
  const description = ref("");
  const allocator = ref("FCFSAllocator");

  const dimension = reactive({
    x: 100,
    y: 20,
    z: 100,
    t: 1500,
  });

  const map = reactive({
    coordinates: {
      long: 8.5410422,
      lat: 47.3744489,
    },
    locationName: "",
    neightbouringTiles: 0,
    topLeftCoordinate: undefined,
    bottomRightCoordinate: undefined,
    tiles: [],
  });

  const owners = reactive([
    {
      color: "#00559d",
      name: "Digitec",
      agents: 20,
      type: "",
      locations: [],
    },
  ]);

  const generateConfigJson = () =>
    cloneDeep({
      name: name.value,
      description: description.value,
      allocator: allocator.value,
      dimension,
      map,
      owners,
      availableAllocators,
      availableOwnersForAllocator,
    });

  const availableAllocators = reactive([]);
  const loadAvailableAllocators = () => {
    getSupportedAllocators().then((allocatorNames) => {
      allocatorNames.forEach((allocatorName) => availableAllocators.push(allocatorName));
    });
  };

  const availableOwnersForAllocator = reactive([]);
  watchEffect(async () => {
    const allocatorName = allocator.value;
    await loadAvailableAllocators();
    const ownersSupportedByAllocator = await getOwnersSupportedByAllocator(allocatorName);
    availableOwnersForAllocator.splice(0);
    ownersSupportedByAllocator.forEach((owner) => {
      availableOwnersForAllocator.push(owner);
    });
  });

  const overwrite = (config) => {
    name.value = config.name;
    description.value = config.description;
    allocator.value = config.allocator;

    map.coordinates = config.map.coordinates;
    map.locationName = config.map.locationName;
    map.neightbouringTiles = config.map.neightbouringTiles;
    map.topLeftCoordinate = config.map.topLeftCoordinate;
    map.bottomRightCoordinate = config.map.bottomRightCoordinate;
    map.tiles = config.map.tiles;

    owners.splice(0);
    config.owners.forEach((owner) => owners.push(owner));
  };

  const isEmpty = computed(() => !name.value);

  return {
    name,
    description,
    allocator,
    dimension,
    map,
    owners,
    availableAllocators,
    availableOwnersForAllocator,
    isEmpty,
    generateConfigJson,
    overwrite,
    loadAvailableAllocators,
  };
});
