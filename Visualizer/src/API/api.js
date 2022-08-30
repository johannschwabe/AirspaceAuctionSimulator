import axios from "axios";
import { saveAs } from "file-saver";
import { compress, decompress } from "compress-json";

/**
 * @typedef {Object} ApiOwnerType
 * @property {string} name
 * @property {string} color
 * @property {string} type
 * @property {int} agents
 */

/**
 * @typedef {Object} ApiDimensionType
 * @property {int} x
 * @property {int} y
 * @property {int} z
 * @property {int} t
 */

/**
 * @typedef {Object} MapObject
 * @property {int[][]} tiles
 * @property {{long: number, lat: number}} topLeftCoordinate
 * @property {{long: number, lat: number}} bottomRightCoordiante
 */

/**
 * @typedef {Object} ApiSimulationConfigType
 * @property {string} name
 * @property {?string} description
 * @property {?MapObject} map
 * @property {ApiOwnerType} owners
 * @property {ApiDimensionType} dimension
 * @property {string} allocator
 */

/**
 * @type {AxiosInstance}
 */
const apiServer = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 60 * 60 * 1000, // 1h
});

const STORAGE_KEY = "simulation";

/**
 * @param {Object} e
 * @returns {string}
 */
const apiPostErrorToString = (e) => {
  if (!e.response) {
    return e.message;
  }
  return e.response.data.detail.map((d) => `${d.msg}: ${d.loc.join(".")}`).join("\n");
};

/**
 * @param {ApiSimulationConfigType} simulationConfig
 * @returns {Promise<RawSimulation>}
 */
export async function postSimulation(simulationConfig) {
  try {
    const { data } = await apiServer.post("/simulation", simulationConfig);
    persistSimulation(data);
    return data;
  } catch (e) {
    const details = apiPostErrorToString(e);
    throw new Error(details);
  }
}

/**
 * Get all registered value functions from the backend
 * @returns {Promise<Object[]>} - Names of allocators
 */
export async function getSupportedValueFunctions(allocator, bidding_strategy) {
  try {
    const { data } = await apiServer.get(`/valueFunctions/${allocator}/${bidding_strategy}`);
    return data;
  } catch (e) {
    const details = apiPostErrorToString(e);
    throw new Error(details);
  }
}

/**
 * Get all registered allocators from the backend
 * @returns {Promise<string[]>} - Names of allocators
 */
export async function getSupportedAllocators() {
  try {
    const { data } = await apiServer.get("/allocators");
    return data;
  } catch (e) {
    const details = apiPostErrorToString(e);
    throw new Error(details);
  }
}

/**
 * Get bidding strategies compatible with selected allocator
 * @returns {Promise<Object[]>} - owners
 */
export async function getBiddingStrategiesSupportedByAllocator(allocator) {
  try {
    const { data } = await apiServer.get(`/biddingStrategies/${allocator}`);
    return data;
  } catch (e) {
    const details = apiPostErrorToString(e);
    throw new Error(details);
  }
}

/**
 * Get payment rules compatible with selected allocator
 * @returns {Promise<Object[]>} - owners
 */
export async function getPaymentRulesSupportedByAllocator(allocator) {
  try {
    const { data } = await apiServer.get(`/paymentRules/${allocator}`);
    return data;
  } catch (e) {
    const details = apiPostErrorToString(e);
    throw new Error(details);
  }
}

/**
 * @param {RawSimulation} data
 */
export function persistSimulation(data) {
  try {
    const compressed = compress(data);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(compressed));
  } catch (e) {
    throw new Error(e);
  }
}

export function canLoadSimulation() {
  return !!localStorage.getItem(STORAGE_KEY);
}

/**
 * @returns {null|RawSimulation}
 */
export function loadSimulationData() {
  const data = localStorage.getItem(STORAGE_KEY);
  if (data) {
    return decompress(JSON.parse(data));
  }
  return null;
}

export function downloadSimulation() {
  const data = loadSimulationData();
  const fileToSave = new Blob([JSON.stringify(data, undefined, 2)], {
    type: "application/json",
  });
  saveAs(fileToSave, `${data?.config.name}.json`);
}
