import { ref, reactive, watchEffect, computed } from "vue";
import { defineStore } from "pinia";
import { cloneDeep } from "lodash-es";
import { getOwnersSupportedByAllocator, getSupportedAllocators } from "../API/api";
import { randomColor } from "../scripts/color";
import { randomName } from "../scripts/names";

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

  const owners = reactive([]);

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
      availableAllocators.splice(0);
      allocatorNames.forEach((allocatorName) => availableAllocators.push(allocatorName));
    });
  };
  const availableAllocatorsOptions = computed(() => {
    return availableAllocators.map((a) => ({ label: a, value: a }));
  });

  const availableOwnersForAllocator = reactive([]);
  watchEffect(async () => {
    const allocatorName = allocator.value;
    await loadAvailableAllocators();
    const ownersSupportedByAllocator = await getOwnersSupportedByAllocator(allocatorName);
    availableOwnersForAllocator.splice(0);
    ownersSupportedByAllocator.forEach((owner) => {
      const locationsDescriptor = owner.positions;
      let minLocations = 0;
      let maxLocations = 1000;
      if (parseInt(locationsDescriptor, 10)) {
        minLocations = parseInt(locationsDescriptor, 10);
        maxLocations = minLocations;
      }
      locationsDescriptor
        .split(";")
        .map((d) => d.trim())
        .forEach((d) => {
          if (d.startsWith(">")) {
            minLocations = parseInt(d.substring(1), 10);
          }
          if (d.startsWith("<")) {
            maxLocations = parseInt(d.substring(1), 10);
          }
        });
      availableOwnersForAllocator.push({
        label: owner._label,
        name: owner.classname,
        description: owner.description,
        type: owner.ownertype,
        allocator: allocator.value,
        minLocations,
        maxLocations,
      });
    });
    if (owners.length === 0 || owners[0].allocator !== allocatorName.value) {
      owners.splice(0);
      owners.push(generateOwner());
    }
  });
  const randomLocation = () => ({ type: "random", gridCoordinates: [] });
  const generateLocationsForOwner = (owner) => {
    return Array(owner.minLocations, 10).map(() => randomLocation());
  };
  const generateOwner = () => {
    const ownerTemplate = availableOwnersForAllocator[0];
    const locations = generateLocationsForOwner(ownerTemplate);
    return {
      color: randomColor(),
      name: randomName(),
      agents: 20,
      minLocations: ownerTemplate.minLocations,
      maxLocations: ownerTemplate.maxLocations,
      type: ownerTemplate.name,
      allocator: allocator.value,
      locations,
    };
  };

  const overwrite = (config) => {
    name.value = config.name;
    description.value = config.description;
    allocator.value = config.allocator;

    dimension.x = config.dimension.x;
    dimension.y = config.dimension.y;
    dimension.z = config.dimension.z;
    dimension.t = config.dimension.t;

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
    availableAllocatorsOptions,
    availableOwnersForAllocator,
    isEmpty,
    randomLocation,
    generateOwner,
    generateConfigJson,
    overwrite,
    loadAvailableAllocators,
  };
});
