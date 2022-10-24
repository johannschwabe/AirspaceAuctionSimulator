import { PointLight } from "@babylonjs/core/Lights/pointLight";
import { Vector3 } from "@babylonjs/core/Maths/math";
import { CreateSphere } from "@babylonjs/core/Meshes/Builders";
import { StandardMaterial } from "@babylonjs/core/Materials/standardMaterial";

/**
 * @typedef {Object.<string, Mesh[]>} BlockerCache
 */

/**
 * Returns an empty object that will hold the cached blockers
 * @returns {BlockerCache}
 */
export function useBlockerCache() {
  return {};
}

/**
 * @typedef {Object.<string, { meshes: Mesh[] }>} DroneCache
 */

/**
 * Returns an empty object that will hold the cached drones
 * @returns {DroneCache}
 */
export function useDroneCache() {
  return {};
}

/**
 * @typedef {Object} FocusCache
 * @property {undefined|Agent} agent
 * @property {Mesh} nearFieldSphere
 * @property {PointLight} selectionLight
 * @property {LinesMesh[]} pathLines
 * @property {StandardMaterial} nearFieldMaterial
 */

/**
 * Creates a cache object to store the agent in focus
 * @param {Object} args
 * @param {Scene} args.scene
 * @returns {FocusCache}
 */
export function useFocusCache({ scene }) {
  // Create selection light
  const selectionLight = new PointLight("selection-light", new Vector3(0, 0, 0), scene);
  selectionLight.range = 0;
  selectionLight.intensity = 0;

  // Create nearField
  const nearFieldSphere = CreateSphere("near-field-sphere", { segments: 8, diameter: 1 }, scene);
  nearFieldSphere.scaling = new Vector3(0, 0, 0);
  const nearFieldMaterial = new StandardMaterial("near-field-material", scene);
  nearFieldMaterial.wireframe = true;
  nearFieldMaterial.alpha = 0.2;
  nearFieldSphere.material = nearFieldMaterial;

  return {
    selectionLight,
    nearFieldSphere,
    nearFieldMaterial,
    pathLines: [],
    agent: undefined,
  };
}
