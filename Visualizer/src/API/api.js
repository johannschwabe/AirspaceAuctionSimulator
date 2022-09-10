import axios from "axios";
import { saveAs } from "file-saver";

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
 * @param {JSONConfig} simulationConfig
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
  const oldData = await getFromObjectStore(db, name);
  if (oldData !== null) {
    await deleteFromObjectStore(db, name);
  }
  return new Promise((resolve) => {
    db.transaction(name, "readwrite").objectStore(name).add(data, name).onsuccess = () => {
      resolve();
    };
  });
}

async function deleteFromObjectStore(db, name) {
  return new Promise((resolve) => {
    db.transaction(name, "readwrite").objectStore(name).delete(name).onsuccess = () => {
      resolve();
    };
  });
}

async function getFromObjectStore(db, name) {
  return new Promise((resolve) => {
    const request = db.transaction(name).objectStore(name).get(name);
    request.onsuccess = (event) => {
      resolve(event.target.result ?? null);
    };
    request.onerror = () => {
      resolve(null);
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
    await addToObjectStore(db, SIMULATION_STORAGE_KEY, simulation);
    await addToObjectStore(db, STATISTICS_STORAGE_KEY, statistics);
    await addToObjectStore(db, CONFIG_STORAGE_KEY, config);
    db.close();
  } catch (e) {
    throw new Error(e);
  }
}

export async function canLoadSimulation() {
  const db = await openDB();
  const data = await getFromObjectStore(db, SIMULATION_STORAGE_KEY);
  db.close();
  return data !== null;
}

/**
 * @returns {null|JSONSimulation}
 */
export async function loadSimulationData() {
  const db = await openDB();
  const simulation = getFromObjectStore(db, SIMULATION_STORAGE_KEY);
  db.close();
  return simulation;
}

/**
 * @returns {null|JSONConfig}
 */
export async function loadConfigData() {
  const db = await openDB();
  const config = getFromObjectStore(db, CONFIG_STORAGE_KEY);
  db.close();
  return config;
}

/**
 * @returns {null|SimulationStatistics}
 */
export async function loadStatisticsData() {
  const db = await openDB();
  const statistics = getFromObjectStore(db, STATISTICS_STORAGE_KEY);
  db.close();
  return statistics;
}

export async function downloadSimulation() {
  const simulation = await loadSimulationData();
  const config = await loadConfigData();
  const statistics = await loadStatisticsData();
  const data = { simulation, config, statistics };
  const fileToSave = new Blob([JSON.stringify(data)], {
    type: "application/json",
  });
  saveAs(fileToSave, `${config.name}.json`);
}
