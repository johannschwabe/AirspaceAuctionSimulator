import { ref, reactive, watchEffect, computed } from "vue";
import { defineStore } from "pinia";
import { cloneDeep } from "lodash-es";
import { getOwnersSupportedByAllocator, getSupportedAllocators } from "../API/api";
import { randomColor } from "../scripts/color";
import { randomName } from "../scripts/names";

/**
 * @typedef {Object} MapConfig
 * @property {{long: number, lat: number}} coordinates
 * @property {string} locationName
 * @property {number} neighbouringTiles
 * @property {{long: number, lat: number}} topLeftCoordinate
 * @property {{long: number, lat: number}} bottomRightCoordinate
 * @property {number[]} tiles
 */

/**
 * @typedef {Object} GridCoordinateConfig
 * @property {number} x
 * @property {number} y
 * @property {number} lat
 * @property {number} long
 * @property {number} value
 */

/**
 * @typedef {Object} LocationConfig
 * @property {string} type
 * @property {GridCoordinateConfig[]} features
 */

/**
 * @typedef {Object} OwnerConfig
 * @property {string} color
 * @property {string} name
 * @property {number} agents
 * @property {number} minLocations
 * @property {number} maxLocations
 * @property {string} type
 * @property {string} allocator
 * @property {LocationConfig[]} locations
 */

/**
 * @typedef {Object} SimulationConfig
 * @property {Ref<string>} name
 * @property {Ref<string>} description
 * @property {Ref<string>} allocator
 * @property {{x: number, y: number, z: number, t: number}} dimension
 * @property {MapConfig} map
 * @property {OwnerConfig[]} owners
 */

/**
 * @typedef {Object} AvailableOwnerConfig
 * @property {string} label
 * @property {string} name
 * @property {string} description
 * @property {string} type
 * @property {string} allocator
 * @property {number} minLocations
 * @property {number} maxLocations
 */

/**
 * Simulation Config Store
 */
export const useSimulationConfigStore = defineStore("simulationConfig", () => {
  const name = ref("");
  const description = ref("");
  const allocator = ref("FCFSAllocator");

  /**
   * @type {UnwrapNestedRefs<{t: number, x: number, y: number, z: number}>}
   */
  const dimension = reactive({
    x: 100,
    y: 100,
    z: 100,
    t: 1500,
  });

  /**
   * @type {UnwrapNestedRefs<MapConfig>}
   */
  const map = reactive({
    coordinates: {
      long: 8.5410422,
      lat: 47.3744489,
    },
    locationName: "",
    neighbouringTiles: 0,
    topLeftCoordinate: undefined,
    bottomRightCoordinate: undefined,
    tiles: [],
  });

  /**
   * @type {UnwrapNestedRefs<OwnerConfig[]>}
   */
  const owners = reactive([]);

  /**
   * @type {UnwrapNestedRefs<string[]>}
   */
  const availableAllocators = reactive([]);

  /**
   * Loads available allocators from the backend API
   */
  const loadAvailableAllocators = () => {
    getSupportedAllocators().then((allocatorNames) => {
      availableAllocators.splice(0);
      allocatorNames.forEach((allocatorName) => availableAllocators.push(allocatorName));
    });
  };

  /**
   * List of available allocators, but computed in a format that is supported by the naive-ui selector
   * @type {ComputedRef<{label: string, value: string}>}
   */
  const availableAllocatorsOptions = computed(() => {
    return availableAllocators.map((a) => ({ label: a, value: a }));
  });

  /**
   * List of all available owners given the selected allocator. Changes whenever the
   * allocator changes.
   * @type {UnwrapNestedRefs<AvailableOwnerConfig[]>}
   */
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

  /**
   * Generates a random location
   * @returns {LocationConfig}
   */
  const randomLocation = () => ({ type: "random", gridCoordinates: [] });

  /**
   * Generates random locations for owner,
   * given the owners constraints (min and max locations)
   * @param {OwnerConfig} owner
   * @returns {LocationConfig[]}
   */
  const generateLocationsForOwner = (owner) => {
    return Array(owner.minLocations, 10).map(() => randomLocation());
  };

  /**
   * Generates a new random owner from the list of available owners for the given allocator
   * @returns {OwnerConfig}
   */
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

  /**
   * Turns the store into a downloadable config json by unwrapping the vue reactive refs
   */
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

  /**
   * Owerwrites the existing store with the content from a .JSON File, idealy a previously downloaded
   * configuration generated by the same Frontend
   * @param {Object} config
   */
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
    map.neighbouringTiles = config.map.neighbouringTiles;
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
