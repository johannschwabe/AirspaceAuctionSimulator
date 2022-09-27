/**
 * @type {Simulation}
 */
import { useSimulationOutputStore } from "@/stores/simulationOutputStore";
import { canLoadSimulation, loadConfigData, loadSimulationData, loadStatisticsData } from "@/API/api";
import Simulation from "../SimulationObjects/Simulation";
import { useSimulationConfigStore } from "@/stores/simulationConfigStore";

let simulationSingleton = null;

/**
 * @param {Simulation} simulation
 */
export function setSimulationSingleton(simulation) {
  const simulationStore = useSimulationOutputStore();
  simulationStore.selectedAgentIDs = [];
  simulationStore.tick = 0;
  simulationSingleton = simulation;
}

/**
 * @returns {Promise<boolean>}
 */
export async function canRecoverSimulationSingleton() {
  return canLoadSimulation();
}

/**
 * @returns {Promise<Simulation>}
 */
export async function loadSimulationSingleton() {
  const simulation_data = await loadSimulationData();
  const config_data = await loadConfigData();
  const statistics_data = await loadStatisticsData();
  if (simulation_data && config_data && statistics_data) {
    const simulation = new Simulation(simulation_data, config_data, statistics_data);
    simulationSingleton = await simulation.load();
    return simulationSingleton;
  } else {
    throw new Error("Unable to recover last simulation!");
  }
}

/**
 * @param {JSONConfig} config
 */
export function setSimulationConfig(config) {
  if (config) {
    const simulationConfig = useSimulationConfigStore();
    simulationConfig.overwrite(config);
  }
}

/**
 * @returns {Promise<void>}
 */
export async function loadSimulationConfig() {
  const config_data = await loadConfigData();
  if (!config_data) {
    throw new Error("Unable to recover last simulation!");
  }
  setSimulationConfig(config_data);
}

/**
 * @returns {Simulation}
 */
export function useSimulationSingleton() {
  return simulationSingleton;
}

/**
 * @returns {boolean}
 */
export function hasSimulationSingleton() {
  return !!simulationSingleton;
}
