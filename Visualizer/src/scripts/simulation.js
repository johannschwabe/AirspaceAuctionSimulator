/**
 * @type {Simulation}
 */
let simulationSingleton = null;

/**
 * @param {Simulation} simulation
 */
export function setSimulationSingleton(simulation) {
  simulationSingleton = simulation;
}

export function useSimulationSingleton() {
  return simulationSingleton;
}
