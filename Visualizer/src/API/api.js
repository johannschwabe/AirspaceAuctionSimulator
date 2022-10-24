import axios from "axios";
import { saveAs } from "file-saver";

/**
 * @type {AxiosInstance}
 */
const apiServer = axios.create({
  baseURL: import.meta.env.VITE_API || "http://localhost:8000",
  timeout: 60 * 60 * 1000, // 1h
});

export const client_id = `ci_${Math.round(Math.random() * 1000)}`;
const ws_base_url = import.meta.env.VITE_WS_API || "ws://localhost:8000/ws";
export const ws = new WebSocket(`${ws_base_url}/${client_id}`);

const STORAGE_KEY = "simulation_db";
const SIMULATION_STORAGE_KEY = "simulation";
const STATISTICS_STORAGE_KEY = "statistics";
const CONFIG_STORAGE_KEY = "config";
const OWNER_MAP_STORAGE_KEY = "owner_map";

/**
 * Converts an API error thrown by FastAPI into a readable string
 * @param {Object} e - Fastify error object
 * @returns {string}
 */
const apiPostErrorToString = (e) => {
  if (!e.response) {
    return e.message;
  }
  try {
    return e.response.data.detail.map((d) => `${d.msg}: ${d.loc.join(".")}`).join("\n");
  } catch (err) {
    console.error(e);
    return e.toString();
  }
};

/**
 * Posts a simulation to the python backend and persists the simulation in the users browser
 * @param {JSONConfig} simulationConfig
 * @returns {Promise<JSONResponse>}
 */
export async function postSimulation(simulationConfig) {
  try {
    const { data } = await apiServer.post(`/simulation/${client_id}`, simulationConfig);
    await persistSimulation(data);
    return data;
  } catch (e) {
    const details = apiPostErrorToString(e);
    throw new Error(details);
  }
}

/**
 * Get all registered value functions from the backend
 * @returns {Promise<Object[]>} - Value function objects
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
    const { data } = await apiServer.get("allocators");
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
 * @returns {Promise<Object[]>} - payment rules
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
 * Opens and returns an indexed database for storing the simulation output
 * @returns {Promise<IDBDatabase>}
 */
async function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(STORAGE_KEY);
    request.onerror = (event) => {
      reject(event.target.errorCode);
    };
    request.onsuccess = (event) => {
      const db = event.target.result;
      db.onerror = (error_event) => {
        console.error("DB ERROR:", error_event.target);
      };
      db.onclose = (close_event) => {
        console.warn("DB CLOSED:", close_event.target);
      };
      db.onabort = (abort_event) => {
        console.warn("DB ABORTED:", abort_event.target);
      };
      resolve(db);
    };
    request.onupgradeneeded = async (event) => {
      const db = event.target.result;
      db.createObjectStore(SIMULATION_STORAGE_KEY);
      db.createObjectStore(CONFIG_STORAGE_KEY);
      db.createObjectStore(STATISTICS_STORAGE_KEY);
      db.createObjectStore(OWNER_MAP_STORAGE_KEY);
    };
  });
}

/**
 * Stores object into database
 * @param {IDBDatabase} db - Database in which data should be stored
 * @param {string} name - Storage key
 * @param {any} data - Data to be stored
 * @returns {Promise<void>}
 */
async function addToObjectStore(db, name, data) {
  const oldData = await getFromObjectStore(db, name);
  if (oldData !== null) {
    await deleteFromObjectStore(db, name);
  }
  return new Promise((resolve) => {
    db.transaction([name], "readwrite").objectStore(name).add(data, name).onsuccess = () => {
      resolve();
    };
  });
}

/**
 * Removes an object from the database
 * @param {IDBDatabase} db - Database from which data should be deleted
 * @param {string} name - Storage key
 * @returns {Promise<void>}
 */
async function deleteFromObjectStore(db, name) {
  return new Promise((resolve) => {
    db.transaction([name], "readwrite").objectStore(name).delete(name).onsuccess = () => {
      resolve();
    };
  });
}

/**
 * Queries an object from the database
 * @param {IDBDatabase} db - Database from which data should be queried
 * @param {string} name - Storage key
 * @returns {Promise<Any>}
 */
async function getFromObjectStore(db, name) {
  return new Promise((resolve) => {
    const request = db.transaction([name], "readwrite").objectStore(name).get(name);
    request.onsuccess = (event) => {
      resolve(event.target.result ?? null);
    };
    request.onerror = () => {
      resolve(null);
    };
  });
}

/**
 * Persists the simulation output by adding it to the database
 * @param {JSONResponse} data
 */
export async function persistSimulation(data) {
  try {
    const simulation = data.simulation;
    const statistics = data.statistics;
    const config = data.config;
    const ownerMap = data.owner_map;
    const db = await openDB();
    await addToObjectStore(db, SIMULATION_STORAGE_KEY, simulation);
    await addToObjectStore(db, STATISTICS_STORAGE_KEY, statistics);
    await addToObjectStore(db, CONFIG_STORAGE_KEY, config);
    await addToObjectStore(db, OWNER_MAP_STORAGE_KEY, ownerMap);
    db.close();
  } catch (e) {
    throw new Error(e);
  }
}

/**
 * Checks whether a simulation can be recovered from the browser database
 * @returns {Promise<boolean>}
 */
export async function canLoadSimulation() {
  const db = await openDB();
  const simulation = await getFromObjectStore(db, SIMULATION_STORAGE_KEY);
  const config = await getFromObjectStore(db, CONFIG_STORAGE_KEY);
  const statistics = await getFromObjectStore(db, STATISTICS_STORAGE_KEY);
  const ownerMap = await getFromObjectStore(db, OWNER_MAP_STORAGE_KEY);
  db.close();
  return !!(simulation && config && statistics && ownerMap);
}

/**
 * Loads a simulation output from the database and returns it
 * @returns {JSONSimulation}
 */
export async function loadSimulationData() {
  const db = await openDB();
  const simulation = getFromObjectStore(db, SIMULATION_STORAGE_KEY);
  db.close();
  return simulation;
}

/**
 * Loads a simulation owner map from the database and returns it
 * @returns {OwnerMap}
 */
export async function loadOwnerMap() {
  const db = await openDB();
  const simulation = getFromObjectStore(db, OWNER_MAP_STORAGE_KEY);
  db.close();
  return simulation;
}

/**
 * Loads a simulation configuration from the database and returns it
 * @returns {JSONConfig}
 */
export async function loadConfigData() {
  const db = await openDB();
  const config = getFromObjectStore(db, CONFIG_STORAGE_KEY);
  db.close();
  return config;
}

/**
 * Loads simulation statistics from the database and returns them
 * @returns {SimulationStatistics}
 */
export async function loadStatisticsData() {
  const db = await openDB();
  const statistics = getFromObjectStore(db, STATISTICS_STORAGE_KEY);
  db.close();
  return statistics;
}

/**
 * Helper function for converting a simulation output into a file and prompt the user for a file location
 * @returns {Promise<void>}
 */
export async function downloadSimulation() {
  const simulation = await loadSimulationData();
  const config = await loadConfigData();
  const statistics = await loadStatisticsData();
  const ownerMap = await loadOwnerMap();
  const data = {
    simulation: simulation,
    config: config,
    statistics: statistics,
    owner_map: ownerMap,
  };
  const fileToSave = new Blob([JSON.stringify(data)], {
    type: "application/json",
  });
  saveAs(fileToSave, `${config.name.toLowerCase().replace(/ /g, "-")}-simulation.json`);
}
