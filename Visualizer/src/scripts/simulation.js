/**
 * @type {Simulation}
 */
import { useSimulationStore } from "../stores/simulation";
import { canLoadSimulation, loadSimulation } from "../API/api";
import Simulation from "../SimulationObjects/Simulation";

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

export function loadSimulationSingleton() {
  const data = loadSimulation();
  if (!data) {
    throw new Error("Unable to recover last simulation!");
  }
  simulationSingleton = new Simulation(data);
}

export function useSimulationSingleton() {
  return simulationSingleton;
}

export function hasSimulationSingleton() {
  return !!simulationSingleton;
}
