import { useSimulationSingleton } from "@/scripts/simulationSingleton";
import { CreateBox, CreateLines } from "@babylonjs/core/Meshes/Builders";
import { Color3, Vector3 } from "@babylonjs/core/Maths/math";
import { StandardMaterial } from "@babylonjs/core/Materials/standardMaterial";
import { getDroneInstance, getMaterialName } from "@/engine/meshes";
import { ActionManager } from "@babylonjs/core/Actions/actionManager";
import { ExecuteCodeAction } from "@babylonjs/core/Actions/directActions";

/**
 * Creates drones and their interactions
 * @param {Object} args
 * @param {Scene} args.scene
 * @param {DroneCache} args.droneCache
 * @param {number} args.x - x dimension of playing field
 * @param {number} args.z - z dimension of playing field
 * @param {FocusOnPathAgent} args.focusOnPathAgent
 * @param {FocusOnSpaceAgent} args.focusOnSpaceAgent
 */
export function useDrones({ scene, droneCache, x, z, focusOnPathAgent, focusOnSpaceAgent }) {
  const simulation = useSimulationSingleton();

  // Push new meshes for SPACE AGENTS
  simulation.activeSpaceAgents.forEach(async (agent) => {
    const spaces = agent.spaces.filter((s) => s.isActiveAtTick(simulation.tick));
    const reservedSpaces = [];

    if (droneCache[agent.id]) {
      droneCache[agent.id].meshes.forEach((mesh) => {
        mesh.dispose();
      });
      delete droneCache[agent.id];
    }

    spaces.forEach((space) => {
      // Draw occupied field
      const agentReservedSpace = CreateBox(`space-agent-${agent.id}`, {
        height: space.dimensionY,
        width: space.dimensionX,
        depth: space.dimensionZ,
      });
      agentReservedSpace.color = Color3.FromHexString(agent.color);

      // create Material
      const ownerMaterial = new StandardMaterial(getMaterialName(agent), scene);
      ownerMaterial.diffuseColor = Color3.FromHexString(agent.color);
      agentReservedSpace.visibility = 0.66;
      agentReservedSpace.material = ownerMaterial;
      agentReservedSpace.isPickable = true;
      agentReservedSpace.actionManager = new ActionManager(scene);

      agentReservedSpace.actionManager.registerAction(
        new ExecuteCodeAction(ActionManager.OnPickTrigger, () => focusOnSpaceAgent({ agent, space }))
      );

      agentReservedSpace.position.x = space.originX - x / 2;
      agentReservedSpace.position.y = space.originY;
      agentReservedSpace.position.z = space.originZ - z / 2;

      reservedSpaces.push(agentReservedSpace);
    });

    droneCache[agent.id] = {
      meshes: reservedSpaces,
    };
  });

  // Push new meshes for PATH AGENTS
  simulation.activePathAgents.forEach(async (agent) => {
    const path = agent.paths.find((p) => p.isActiveAtTick(simulation.tick));
    const pathIdx = agent.paths.indexOf(path);
    const { x: agent_x, y: agent_y, z: agent_z } = agent.combinedPath.at(simulation.tick);

    if (agent.id in droneCache && droneCache[agent.id].pathIdx !== pathIdx) {
      droneCache[agent.id].meshes.forEach((mesh) => {
        mesh.dispose();
      });
      delete droneCache[agent.id];
    }

    if (!(agent.id in droneCache)) {
      // Draw path
      const points = path.ticksInAir.map((_t, i) => {
        const { x: ax, y: ay, z: az } = path.atIndex(i);
        return new Vector3(ax - x / 2, ay, az - z / 2);
      });
      const agentPathLine = CreateLines(`line-agent-${agent.id}`, {
        points,
      });
      agentPathLine.alpha = 0.5;
      agentPathLine.color = Color3.FromHexString(agent.color);

      // create Material
      const ownerMaterial = new StandardMaterial(getMaterialName(agent), scene);
      ownerMaterial.diffuseColor = Color3.FromHexString(agent.color);
      ownerMaterial.emissiveColor = Color3.FromHexString(agent.color);
      ownerMaterial.alpha = 1;

      const agentMesh = await getDroneInstance(scene, agent);
      agentMesh.material = ownerMaterial;
      agentMesh.isPickable = true;
      agentMesh.actionManager = new ActionManager(scene);

      if (simulation.agentInFocus && simulation.agentInFocus?.id !== agent.id) {
        ownerMaterial.alpha = 0.2;
        agentPathLine.alpha = 0.1;
      }

      agentMesh.actionManager.registerAction(
        new ExecuteCodeAction(ActionManager.OnPickTrigger, () => focusOnPathAgent({ agent, agent_x, agent_y, agent_z }))
      );

      droneCache[agent.id] = {
        meshes: [agentMesh, agentPathLine],
        pathIdx,
      };
    }

    // Update sphere position
    const storedAgentLocationSphere = droneCache[agent.id].meshes[0];
    storedAgentLocationSphere.position.x = agent_x - x / 2;
    storedAgentLocationSphere.position.y = agent_y;
    storedAgentLocationSphere.position.z = agent_z - z / 2;
  });
}

/**
 * Updates positions of drones on playing field
 * @param {Object} args
 * @param {Scene} args.scene
 * @param {DroneCache} args.droneCache
 * @param {number} x - args.x dimension of playing field
 * @param {number} z - args.z dimension of playing field
 * @param {FocusOnSpaceAgent} args.focusOnSpaceAgent
 * @param {FocusOnPathAgent} args.focusOnPathAgent
 * @returns {Promise<void>}
 */
export async function updateDrones({ scene, droneCache, x, z, focusOnSpaceAgent, focusOnPathAgent }) {
  const simulation = useSimulationSingleton();

  // Remove unused meshes
  const activeUUIDs = simulation.activeAgentIDs;
  Object.entries(droneCache).forEach(([uuid, cache]) => {
    if (!activeUUIDs.includes(uuid)) {
      cache.meshes.forEach((mesh) => {
        mesh.dispose();
      });
      delete droneCache[uuid];
    }
  });
  await useDrones({ scene, droneCache, x, z, focusOnSpaceAgent, focusOnPathAgent });
}
