import { SceneLoader } from "@babylonjs/core/Loading/sceneLoader";
import { DRONE_TYPE } from "@/engine/constants";
import { useSimulationSingleton } from "@/scripts/simulationSingleton";
import "@babylonjs/loaders";

export let droneMeshes;

/**
 * Returns the mesh of a drone given its parent
 * @param {Scene} scene
 * @param {Agent} agent
 * @returns {Promise<AbstractMesh>}
 */
export async function getDroneInstance(scene, agent) {
  if (!droneMeshes) {
    const { meshes } = await SceneLoader.ImportMeshAsync("", "./3d/", "drones.glb", scene);
    droneMeshes = meshes.filter((mesh) => DRONE_TYPE.includes(mesh.name));
    droneMeshes.forEach((droneMesh) => {
      droneMesh.isVisible = false;
      droneMesh.setParent(null);
    });
  }
  const simulation = useSimulationSingleton();
  const name = `sphere-agent-${agent.id}`;
  const droneMesh = droneMeshes[(simulation.owners.indexOf(agent.owner) + 3) % droneMeshes.length];
  const clone = droneMesh.clone(name);
  clone.isVisible = true;
  return clone;
}

/**
 * Generates material name based on agent
 * @param {Agent} agent
 * @returns {string}
 */
export function getMaterialName(agent) {
  return `material-agent-${agent.id}`;
}
