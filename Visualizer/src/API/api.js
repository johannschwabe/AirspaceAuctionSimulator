import axios from "axios";
import { saveAs } from "file-saver";

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

const STORAGE_KEY = "simulation_db";
const SIMULATION_STORAGE_KEY = "simulation";
const STATISTICS_STORAGE_KEY = "statistics";
const CONFIG_STORAGE_KEY = "config";

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
 * @returns {Promise<JSONResponse>}
 */
export async function postSimulation(simulationConfig) {
  try {
    const { data } = await apiServer.post("/simulation", simulationConfig);
    await persistSimulation(data);
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

async function openDB() {
  console.log("OPEN");
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(STORAGE_KEY);
    request.onerror = (event) => {
      console.log("OPEN:", event);
      reject(event.target.errorCode);
    };
    request.onsuccess = (event) => {
      const db = event.target.result;
      db.onerror = (error_event) => {
        console.error(`Database error: ${error_event.target.errorCode}`);
      };
      db.onclose = (close_event) => {
        console.log("DB CLOSED:", close_event.target);
      };
      db.onabort = (abort_event) => {
        console.log("DB ABORTED:", abort_event.target);
      };
      resolve(db);
    };
    request.onupgradeneeded = async (event) => {
      const db = event.target.result;
      db.createObjectStore(SIMULATION_STORAGE_KEY);
      db.createObjectStore(CONFIG_STORAGE_KEY);
      db.createObjectStore(STATISTICS_STORAGE_KEY);
    };
  });
}

async function addToObjectStore(db, name, data) {
  console.log("ADD");
  return new Promise((resolve) => {
    db.transaction([name], "readwrite").objectStore(name).add(data, name).onsuccess = (event) => {
      console.log("ADD:", event);
      resolve();
    };
  });
}

async function fetchFromObjectStore(db, name) {
  console.log("FETCH");
  return new Promise((resolve) => {
    db.transaction([name]).objectStore(name).openCursor().onsuccess = (event) => {
      console.log("FETCH:", event);
      resolve(event.target.result?.value ?? null);
    };
  });
}

/**
 * @param {JSONResponse} data
 */
export async function persistSimulation(data) {
  try {
    const simulation = data.simulation;
    const statistics = data.statistics;
    const config = data.config;
    const db = await openDB();
    console.log("DB:", db);
    await addToObjectStore(db, SIMULATION_STORAGE_KEY, simulation);
    await addToObjectStore(db, STATISTICS_STORAGE_KEY, statistics);
    await addToObjectStore(db, CONFIG_STORAGE_KEY, config);
  } catch (e) {
    throw new Error(e);
  }
}

export async function canLoadSimulation() {
  const db = await openDB();
  const data = await fetchFromObjectStore(db, SIMULATION_STORAGE_KEY);
  return !!data;
}

/**
 * @returns {null|JSONSimulation}
 */
export async function loadSimulationData() {
  const db = await openDB(STORAGE_KEY);
  return fetchFromObjectStore(db, SIMULATION_STORAGE_KEY);
}

/**
 * @returns {null|JSONConfig}
 */
export async function loadConfigData() {
  const db = await openDB(STORAGE_KEY);
  return fetchFromObjectStore(db, CONFIG_STORAGE_KEY);
}

/**
 * @returns {null|JSONConfig}
 */
export async function loadStatisticsData() {
  const db = await openDB(STORAGE_KEY);
  return fetchFromObjectStore(db, STATISTICS_STORAGE_KEY);
}

export function downloadSimulation() {
  const data = loadSimulationData();
  const fileToSave = new Blob([JSON.stringify(data, undefined, 2)], {
    type: "application/json",
  });
  saveAs(fileToSave, `${data?.config.name}.json`);
}
