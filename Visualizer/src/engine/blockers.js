import { useSimulationSingleton } from "@/scripts/simulationSingleton";
import { CreateBox } from "@babylonjs/core/Meshes/Builders";
import { StandardMaterial } from "@babylonjs/core/Materials/standardMaterial";
import { Color3 } from "@babylonjs/core/Maths/math";

/**
 * Creates the default material used for all regular blockers
 * @param {Object} args
 * @param {Scene} args.scene
 * @returns {StandardMaterial}
 */
export function useBlockerMaterial({ scene }) {
  const blockerMaterial = new StandardMaterial("blocker-material", scene);
  blockerMaterial.diffuseColor = Color3.FromHexString("#3a4441");
  blockerMaterial.maxSimultaneousLights = 10;
  blockerMaterial.alpha = 1;
  return blockerMaterial;
}

/**
 * Generates active blockers
 * @param {Object} args
 * @param {Scene} args.scene
 * @param {BlockerCache} args.blockerCache
 * @param {ShadowGenerator} args.shadows
 * @param {number} args.x - x dimension of playing field
 * @param {number} args.z - z dimension of playing field
 * @param {StandardMaterial} args.blockerMaterial
 */
export function useBlockers({ scene, blockerCache, shadows, x, z, blockerMaterial }) {
  const simulation = useSimulationSingleton();

  // Create blockers
  simulation.activeBlockers.forEach((blocker) => {
    if (!(blocker.id in blockerCache)) {
      const blockerCube = CreateBox(
        "box",
        {
          height: blocker.dimension.y,
          width: blocker.dimension.x,
          depth: blocker.dimension.z,
        },
        scene
      );
      blockerCube.material = blockerMaterial;
      blockerCube.receiveShadows = true;
      shadows.getShadowMap().renderList.push(blockerCube);

      blockerCache[blocker.id] = [blockerCube];
    }
    // Update blocker position
    const storedBlockerCube = blockerCache[blocker.id][0];
    storedBlockerCube.position.x = blocker.positionAtTick(simulation.tick).x + blocker.dimension.x / 2 - x / 2;
    storedBlockerCube.position.y = blocker.positionAtTick(simulation.tick).y + blocker.dimension.y / 2;
    storedBlockerCube.position.z = blocker.positionAtTick(simulation.tick).z + blocker.dimension.z / 2 - z / 2;
  });
}

/**
 * Updates positions of blockers
 * @param {Object} args
 * @param {Scene} args.scene
 * @param {BlockerCache} args.blockerCache
 * @param {ShadowGenerator} args.shadows
 * @param {number} args.x - x dimension of playing field
 * @param {number} args.z - z dimension of playing field
 * @param {StandardMaterial} args.blockerMaterial
 */
export function updateBlockers({ scene, blockerCache, shadows, x, z, blockerMaterial }) {
  const simulation = useSimulationSingleton();

  // Remove unused meshes
  const activeIDs = simulation.activeBlockerIDs;
  Object.entries(blockerCache).forEach(([id, meshes]) => {
    if (!(id in activeIDs)) {
      meshes.forEach((mesh) => {
        mesh.dispose();
      });
      delete blockerCache[id];
    }
  });

  useBlockers({ scene, blockerCache, shadows, x, z, blockerMaterial });
}
