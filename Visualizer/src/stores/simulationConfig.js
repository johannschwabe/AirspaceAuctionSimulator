import { ref, reactive, watchEffect, computed } from "vue";
import { defineStore } from "pinia";
import { cloneDeep } from "lodash-es";
import {
  getBiddingStrategiesSupportedByAllocator,
  getPaymentRulesSupportedByAllocator,
  getSupportedAllocators,
} from "../API/api";
import { randomColor } from "../scripts/color";
import { randomName } from "../scripts/names";

/**
 * @typedef {Object} MapConfig
 * @property {{long: number, lat: number}} coordinates
 * @property {{long: number, lat: number}} bottomLeftCoordinate
 * @property {{long: number, lat: number}} topRightCoordinate
 * @property {string} locationName
 * @property {number} neighbouringTiles
 * @property {{bottomLeft: {long: number, lat: number}, topRight: {long: number, lat: number}}} subselection
 * @property {number[]} tiles
 */

/**
 * @typedef {Object} WeightedCoordinate
 * @property {number} lat
 * @property {number} long
 */

/**
 * @typedef {Object} LocationConfig
 * @property {string} type
 * @property {Object} meta
 * @property {WeightedCoordinate[]} points
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
  const paymentRule = ref("FCFSPaymentRule");

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
    bottomLeftCoordinate: undefined,
    topRightCoordinate: undefined,
    subselection: {
      bottomLeft: undefined,
      topRight: undefined,
    },
    resolution: 2,
    height: 100,
    minHeight: 0,
    allocationPeriod: 60,
    timesteps: 1500,
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

  const path_meta = [
    {
      key: "near_field",
      label: "Near field size",
      description: "Radius of reserved field ",
      type: "int",
      value: Math.ceil(Math.random() * 4),
    },
    {
      key: "battery",
      label: "Battery capacity",
      description: "Maximum flight time",
      type: "int",
      value: Math.ceil(Math.random() * 1000),
    },
    {
      key: "speed",
      label: "Ticks per voxel",
      description: "Number ticks needed to traverse a voxel: 1 is the fastest",
      type: "int",
      value: Math.ceil(Math.random() * 5),
    },
  ];
  const space_meta = [
    {
      key: "size_x",
      label: "Field Size X",
      description: "Size of reserved field in X-Dimension",
      type: "int",
      value: Math.ceil(Math.random() * 100),
    },
    {
      key: "size_y",
      label: "Field Size Y",
      description: "Size of reserved field in Y-Dimension",
      type: "int",
      value: Math.ceil(Math.random() * 100),
    },
    {
      key: "size_z",
      label: "Field Size Z",
      description: "Size of reserved field in Z-Dimension",
      type: "int",
      value: Math.ceil(Math.random() * 100),
    },
    {
      key: "size_t",
      label: "Reservation Duration",
      description: "Number of ticks field should be reserved",
      type: "int",
      value: Math.ceil(Math.random() * 100),
    },
  ];

  /**
   * List of all available Bidding Strategies given the selected allocator. Changes whenever the
   * allocator changes.
   * @type {UnwrapNestedRefs<AvailableOwnerConfig[]>}
   */
  const availableBiddingStrategiesForAllocator = reactive([]);
  watchEffect(async () => {
    const allocatorName = allocator.value;
    const biddingStrategiesSupportedByAllocator = await getBiddingStrategiesSupportedByAllocator(allocatorName);
    availableBiddingStrategiesForAllocator.splice(0);
    biddingStrategiesSupportedByAllocator.forEach((biddingStrategy) => {
      availableBiddingStrategiesForAllocator.push({
        label: biddingStrategy.label,
        classname: biddingStrategy.classname,
        description: biddingStrategy.description,
        allocationType: biddingStrategy.strategyType,
        minLocations: biddingStrategy.minLocations,
        maxLocations: biddingStrategy.maxLocations,
        meta: [...(biddingStrategy.strategyType === "space" ? space_meta : path_meta), ...biddingStrategy.meta],
      });
    });
    owners.splice(0);
    owners.push(generateOwner());
  });

  /**
   * List of available biddingStrategies, but computed in a format that is supported by the naive-ui selector
   * @type {ComputedRef<{label: string, value: string}>}
   */
  const availableBiddingStrategiesOptions = computed(() => {
    return availableBiddingStrategiesForAllocator.map((a) => ({ label: a.label, value: a }));
  });

  /**
   * List of all available Bidding Strategies given the selected allocator. Changes whenever the
   * allocator changes.
   * @type {UnwrapNestedRefs<AvailableOwnerConfig[]>}
   */
  const availablePaymentRules = reactive([]);
  watchEffect(async () => {
    const allocatorName = allocator.value;
    const paymentRulesSupportedByAllocator = await getPaymentRulesSupportedByAllocator(allocatorName);
    availablePaymentRules.splice(0);
    paymentRulesSupportedByAllocator.forEach((paymentRule) => {
      availablePaymentRules.push({
        label: paymentRule.label,
        classname: paymentRule.classname,
      });
    });
    if (availablePaymentRules.length > 0) {
      paymentRule.value = availablePaymentRules[0].classname;
    }
  });

  /**
   * List of available paymentRules, but computed in a format that is supported by the naive-ui selector
   * @type {ComputedRef<{label: string, value: string}>}
   */
  const availablePaymentRulesOptions = computed(() => {
    return availablePaymentRules.map((a) => ({ label: a.label, value: a.classname }));
  });

  /**
   * Generates a random location
   * @returns {{meta: {}, coordinates: *[], type: string}}
   */
  const randomLocation = () => ({ type: "random", points: [], meta: {} });

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
    const biddingStrategyTemplate = availableBiddingStrategiesForAllocator[0];
    const locations = generateLocationsForOwner(biddingStrategyTemplate);
    return {
      color: randomColor(),
      name: randomName(),
      agents: 20,
      biddingStrategy: biddingStrategyTemplate,
      locations,
      valueFunction: "-",
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
      paymentRule: paymentRule.value,
      map,
      owners,
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

    map.coordinates = config.map.coordinates;
    map.locationName = config.map.locationName;
    map.neighbouringTiles = config.map.neighbouringTiles;
    map.topRightCoordinate = config.map.topRightCoordinate;
    map.bottomLeftCoordinate = config.map.bottomLeftCoordinate;
    map.subselection = config.map.subselection;
    map.tiles = config.map.tiles;
    map.timesteps = config.map.timesteps;
    map.height = config.map.height;

    owners.splice(0);
    config.owners.forEach((owner) => owners.push(owner));
  };

  const setMapSubTile = (topLeft, bottomRight) => {
    map.subselection.bottomLeft = { long: topLeft[0], lat: topLeft[1] };
    map.subselection.topRight = { long: bottomRight[0], lat: bottomRight[1] };
  };

  const isEmpty = computed(() => !name.value);

  return {
    name,
    description,
    allocator,
    map,
    owners,
    availableAllocators,
    availableAllocatorsOptions,
    availableBiddingStrategiesForAllocator,
    availablePaymentRulesOptions,
    isEmpty,
    randomLocation,
    generateOwner,
    generateConfigJson,
    overwrite,
    loadAvailableAllocators,
    setMapSubTile,
    paymentRule,
    availableBiddingStrategiesOptions,
  };
});
