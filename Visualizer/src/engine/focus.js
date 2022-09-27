import { useSimulationSingleton } from "@/scripts/simulationSingleton";
import { Color3, Vector3 } from "@babylonjs/core/Maths/math";
import { getMaterialName } from "@/engine/meshes";
import { CreateLines } from "@babylonjs/core/Meshes/Builders";
import Path from "@/SimulationObjects/Path";
import { HEMISPHERE_LIGHT_INTENSITY, MAIN_LIGHT_INTENSITY } from "@/engine/constants";
import SpaceAgent from "@/SimulationObjects/SpaceAgent";
import PathAgent from "@/SimulationObjects/PathAgent";

/**
 * @typedef {Function} FocusOnSpaceAgent
 * @param {Object} args
 * @param {SpaceAgent} args.agent
 * @param {Space} args.space
 * @param {boolean} args.update
 * @returns {void}
 */

/**
 * @typedef {Function} FocusOffSpaceAgent
 * @returns {void}
 */

/**
 * @typedef {Function} FocusOnPathAgent
 * @param {Object} args
 * @param {PathAgent} args.agent
 * @param {number} args.agent_x
 * @param {number} args.agent_y
 * @param {number} args.agent_z
 * @param {boolean} args.update
 * @returns {void}
 */

/**
 * @typedef {Function} FocusOffPathAgent
 * @returns {void}
 */

/**
 * Creates focus functions to focus on/off path/space agents
 * @param {Object} args
 * @param {number} args.x - x dimension of playing field
 * @param {number} args.y - y dimension of playing field
 * @param {number} args.z - z dimension of playing field
 * @param {FocusCache} args.focusCache
 * @param {DirectionalLight} args.mainLight
 * @param {HemisphericLight} args.hemisphereLight
 * @param {DroneCache} args.droneCache
 * @param {ArcRotateCamera} args.camera
 * @returns {{focusOffPathAgent: FocusOffPathAgent, focusOnPathAgent: FocusOnPathAgent, focusOnSpaceAgent: FocusOnSpaceAgent, focusOffSpaceAgent: FocusOffSpaceAgent}}
 */
export function useFocusFunctions({ x, y, z, focusCache, mainLight, hemisphereLight, droneCache, camera }) {
  const simulation = useSimulationSingleton();

  /**
   * @param {SpaceAgent} agent
   * @param {Space} space
   * @param {boolean} update
   * @returns {void}
   */
  const focusOnSpaceAgent = ({ agent, space, update }) => {
    // Write agent to focus cache
    focusCache.agent = agent;
    // Turn on focus light
    const { selectionLight } = focusCache;
    selectionLight.position.x = space.originX - x / 2;
    selectionLight.position.y = space.originY;
    selectionLight.position.z = space.originZ - z / 2;
    if (!update) {
      selectionLight.diffuse = Color3.FromHexString(agent.color);
      selectionLight.specular = Color3.FromHexString(agent.color);
      selectionLight.range = y * 2;
      selectionLight.intensity = 2;

      // Turn off main light
      mainLight.intensity = 0;

      // Turn off hemisphere light
      hemisphereLight.intensity = 0.5;
    }

    // Darken all other drones
    Object.values(droneCache).forEach(({ meshes }) => {
      if (meshes[0].material.name !== getMaterialName(agent)) {
        meshes[0].material.alpha = 0.2;
        if (meshes.length > 1) {
          meshes[1].alpha = 0.1;
        }
      }
    });

    // Focus camera to agent
    const target = new Vector3(space.originX - x / 2, space.originY, space.originZ - z / 2);
    camera.setTarget(target);

    simulation.focusOnAgent(agent);
  };

  /**
   * @param {PathAgent} agent
   * @param {number} agent_x
   * @param {number} agent_y
   * @param {number} agent_z
   * @param {boolean} update
   * @returns {void}
   */
  const focusOnPathAgent = ({ agent, agent_x, agent_y, agent_z, update }) => {
    // Write agent to focus cache
    focusCache.agent = agent;
    // Turn on focus light
    const { selectionLight } = focusCache;
    selectionLight.position.x = agent_x - x / 2;
    selectionLight.position.y = agent_y;
    selectionLight.position.z = agent_z - z / 2;
    if (!update) {
      selectionLight.diffuse = Color3.FromHexString(agent.color);
      selectionLight.specular = Color3.FromHexString(agent.color);
      selectionLight.range = y * 2;
      selectionLight.intensity = 2;

      // Turn off main light
      mainLight.intensity = 0;

      // Turn off hemisphere light
      hemisphereLight.intensity = 0.5;
    }

    // Activate NearField
    const { nearFieldSphere, nearFieldMaterial } = focusCache;
    nearFieldSphere.position.x = agent_x - x / 2;
    nearFieldSphere.position.y = agent_y;
    nearFieldSphere.position.z = agent_z - z / 2;
    if (!update) {
      const nearR = agent.nearRadius * 2;
      nearFieldSphere.scaling = new Vector3(nearR, nearR, nearR);
      nearFieldMaterial.diffuseColor = Color3.FromHexString(agent.color);
      nearFieldMaterial.emissiveColor = Color3.FromHexString(agent.color);
    }

    // Highlight own agents branches
    if (!update) {
      Object.values(droneCache).forEach(({ meshes }) => {
        if (meshes[0].material.name !== getMaterialName(agent)) {
          meshes[0].material.alpha = 0.2;
          if (meshes.length > 1) {
            meshes[1].alpha = 0.1;
          }
        }
      });
      focusCache.pathLines.forEach((line) => {
        line.dispose();
      });
      const drawPath = ({ path, color, alpha }) => {
        const points = path.ticksInAir.map((_t, i) => {
          const { x: ax, y: ay, z: az } = path.atIndex(i);
          return new Vector3(ax - x / 2, ay, az - z / 2);
        });
        const pathLine = CreateLines(`branch-agent-${agent.id}`, {
          points,
        });
        pathLine.alpha = alpha;
        pathLine.color = Color3.FromHexString(color);
        return pathLine;
      };
      const pathLines = [];
      agent.intermediate_allocations.forEach((branch) => {
        branch.paths.forEach((branch_path) => {
          const path_segments = Path.subtract(branch_path, agent.combinedPath);
          path_segments.forEach((path) => {
            pathLines.push(drawPath({ path, color: "#ffffff", alpha: 1 }));
          });
        });
      });
      agent.paths.forEach((path) => {
        pathLines.push(drawPath({ path, color: agent.color, alpha: 1.0 }));
      });
      focusCache.pathLines = pathLines;
    }

    // Focus camera to agent
    const target = new Vector3(agent_x - x / 2, agent_y, agent_z - z / 2);
    camera.setTarget(target);

    simulation.focusOnAgent(agent);
  };

  /**
   * @returns {void}
   */
  const focusOffSpaceAgent = () => {
    // Turn off focus light
    const { selectionLight } = focusCache;
    selectionLight.intensity = 0.0;

    // Turn on main light
    mainLight.intensity = MAIN_LIGHT_INTENSITY;

    // Turn on hemisphere light
    hemisphereLight.intensity = HEMISPHERE_LIGHT_INTENSITY;

    // Set opacity of other drones to regular values
    Object.values(droneCache).forEach(({ meshes }) => {
      meshes[0].material.alpha = 1.0;
      if (meshes.length > 1) {
        meshes[1].alpha = 0.5;
      }
    });

    // Focus camera to base again
    const target = new Vector3(0, simulation.dimensions.y / 2, 0);
    camera.setTarget(target);

    focusCache.agent = undefined;
  };

  /**
   * @returns {void}
   */
  const focusOffPathAgent = () => {
    // Turn off focus light
    const { selectionLight } = focusCache;
    selectionLight.intensity = 0.0;

    // Turn on main light
    mainLight.intensity = MAIN_LIGHT_INTENSITY;

    // Turn on hemisphere light
    hemisphereLight.intensity = HEMISPHERE_LIGHT_INTENSITY;

    // Disable Near-/ Farfield Spheres
    const { nearFieldSphere } = focusCache;
    nearFieldSphere.scaling = new Vector3(0, 0, 0);

    // Set opacity of other drones to regular values
    Object.values(droneCache).forEach(({ meshes }) => {
      meshes[0].material.alpha = 1.0;
      if (meshes.length > 1) {
        meshes[1].alpha = 0.5;
      }
    });

    // Disable highlighted paths
    focusCache.pathLines.forEach((line) => {
      line.dispose();
    });
    focusCache.pathLines = [];

    // Focus camera to base again
    const target = new Vector3(0, simulation.dimensions.y / 2, 0);
    camera.setTarget(target);

    focusCache.agent = undefined;
  };
  return {
    focusOnSpaceAgent,
    focusOnPathAgent,
    focusOffSpaceAgent,
    focusOffPathAgent,
  };
}

/**
 *
 * @param {FocusCache} focusCache
 * @param {FocusOnSpaceAgent} focusOnSpaceAgent
 * @param {FocusOnPathAgent} focusOnPathAgent
 */
export function updateFocus({ focusCache, focusOnSpaceAgent, focusOnPathAgent }) {
  const agent = focusCache.agent;
  if (!agent) {
    return;
  }
  const simulation = useSimulationSingleton();
  if (!agent.isActiveAtTick(simulation.tick)) {
    return;
  }
  if (agent instanceof SpaceAgent) {
    const space = agent.spaces.find((s) => s.isActiveAtTick(simulation.tick));
    focusOnSpaceAgent({ agent, space, update: true });
  }
  if (agent instanceof PathAgent) {
    const { x: agent_x, y: agent_y, z: agent_z } = focusCache.agent.combinedPath.at(simulation.tick);
    focusOnPathAgent({ agent, agent_x, agent_y, agent_z, update: true });
  }
}
