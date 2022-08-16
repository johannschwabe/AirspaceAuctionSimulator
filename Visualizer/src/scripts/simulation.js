/**
 * @type {Simulation}
 */
import { useSimulationStore } from "@/stores/simulation";
import { canLoadSimulation, loadSimulationData } from "@/API/api";
import Simulation from "../SimulationObjects/Simulation";
import { useSimulationConfigStore } from "@/stores/simulationConfig";

let simulationSingleton = null;

/**
 * @param {Simulation} simulation
 */
export function setSimulationSingleton(simulation) {
  const simulationStore = useSimulationStore();
  simulationStore.selectedAgentIDs = [];
  simulationStore.tick = 0;
  simulationSingleton = simulation;
}

export function canRecoverSimulationSingleton() {
  return canLoadSimulation();
}

export async function loadSimulationSingleton() {
  const data = loadSimulationData();
  if (!data) {
    throw new Error("Unable to recover last simulation!");
  }
  const simulation = new Simulation(data);
  simulationSingleton = await simulation.load();
  return simulationSingleton;
}

export function setSimulationConfig(data) {
  if (data.config) {
    const simulationConfig = useSimulationConfigStore();
    simulationConfig.overwrite(data.config);
  }
}

export function loadSimulationConfig() {
  const data = loadSimulationData();
  console.log({ data });
  if (!data) {
    throw new Error("Unable to recover last simulation!");
  }
  setSimulationConfig(data);
}

export function useSimulationSingleton() {
  return simulationSingleton;
}

export function hasSimulationSingleton() {
  return !!simulationSingleton;
}
