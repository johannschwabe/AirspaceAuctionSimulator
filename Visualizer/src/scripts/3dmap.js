import {
  ActionManager,
  ArcRotateCamera,
  AxesViewer,
  Color3,
  DirectionalLight,
  Engine,
  ExecuteCodeAction,
  HemisphericLight,
  MeshBuilder,
  PointLight,
  Scene,
  ShadowGenerator,
  StandardMaterial,
  Vector3,
  Color4,
} from "babylonjs";
import { useSimulationSingleton } from "./simulation";

export function useEngine({ canvas }) {
  return new Engine(canvas.value, true, {
    preserveDrawingBuffer: true,
    stencil: true,
  });
}

export function useScene({ engine }) {
  const scene = new Scene(engine);
  scene.clearColor = Color4.FromHexString("#101010");
  return scene;
}

export function useBlockerMaterial({ scene }) {
  const blockerMaterial = new StandardMaterial("blocker-material", scene);
  blockerMaterial.diffuseColor = new Color3.FromHexString("#313336");
  blockerMaterial.maxSimultaneousLights = 10;
  blockerMaterial.alpha = 1;
  return blockerMaterial;
}

export function useMainLight({ scene, x, y, z }) {
  const mainLight = new DirectionalLight("directionalLight", new Vector3(-1, -1, -1), scene);
  mainLight.diffuse = new Color3.FromHexString("#ffffff");
  mainLight.specular = new Color3.FromHexString("#63e2b7");
  mainLight.groundColor = new Color3.FromHexString("#44ab87");
  mainLight.intensity = 1;
  mainLight.position.x = x / 2;
  mainLight.position.y = y / 2;
  mainLight.position.z = z / 2;
  return mainLight;
}

export function useCamera({ x, y, z, scene, canvas }) {
  const target = new Vector3(0, (y / 4) * 2, 0);
  const camera = new ArcRotateCamera("camera", -Math.PI / 2, Math.PI / 2.5, 3, target, scene);
  camera.attachControl(canvas, true);
  camera.setTarget(target);
  camera.setPosition(new Vector3(-x, y * 2.5, -z));
  return camera;
}

export function useHemisphereLight({ scene }) {
  const hemisphereLight = new HemisphericLight("HemiLight", new Vector3(0, 1, 0), scene);
  hemisphereLight.intensity = 0.5;
  return hemisphereLight;
}

export function useAxisIndicators({ scene, x, y, z }) {
  const lengthOfAxis = Math.max(x, y, z) / 10;
  const axes = new AxesViewer(scene, lengthOfAxis);
  axes.update(new Vector3(-x / 2, 0, -z / 2), new Vector3(1, 0, 0), new Vector3(0, 1, 0), new Vector3(0, 0, 1));
  return axes;
}

export function useShadows({ mainLight }) {
  const shadows = new ShadowGenerator(2048, mainLight);
  shadows.usePoissonSampling = true;
  shadows.getShadowMap().refreshRate = 1;
  mainLight.autoUpdateExtends = false;
  return shadows;
}

export function useGround({ scene, x, z }) {
  const ground = MeshBuilder.CreateGround("ground", { width: x, height: z });
  const groundMaterial = new StandardMaterial("ground-material", scene);
  groundMaterial.diffuseColor = new Color3.FromHexString("#101010");
  groundMaterial.specularColor = new Color3.FromHexString("#2b2b2c");
  groundMaterial.alpha = 1;
  ground.material = groundMaterial;
  ground.receiveShadows = true;
  return ground;
}

export function useBuildings({ scene, shadows, mapTiles, blockerMaterial }) {
  mapTiles.forEach((mapTile, i) => {
    mapTile.buildings.forEach((building, j) => {
      const options = {
        shape: building.coordinates.map(({ x, y }) => new Vector3(x, y, 0)),
        path: [new Vector3(0, 0, 0), new Vector3(0, building.height, 0)],
        cap: Mesh.CAP_END,
      };
      const buildingMesh = MeshBuilder.ExtrudeShape(`tile-${i}-building-${j}`, options, scene);
      buildingMesh.material = blockerMaterial;
      buildingMesh.receiveShadows = true;
      shadows.getShadowMap().renderList.push(buildingMesh);
    });
  });
}

export function useOrientationLights({ lineAlpha, x, y, z }) {
  const stepX = Math.floor(x / 1);
  const stepY = Math.floor(y / 10);
  const stepZ = Math.floor(z / 1);

  for (let xi = 0; xi <= x; xi += stepX) {
    for (let yi = 0; yi <= y; yi += stepY) {
      const line = MeshBuilder.CreateLines(`line-x${xi}-y${yi}`, {
        points: [new Vector3(xi - x / 2, yi, 0 - z / 2), new Vector3(xi - x / 2, yi, z - z / 2)],
      });
      line.alpha = lineAlpha;
      line.color = new Color3.White();
    }
  }
  for (let xi = 0; xi <= x; xi += stepX) {
    for (let zi = 0; zi <= z; zi += stepZ) {
      const line = MeshBuilder.CreateLines(`line-x${xi}-z${zi}`, {
        points: [new Vector3(xi - x / 2, 0, zi - z / 2), new Vector3(xi - x / 2, y, zi - z / 2)],
      });
      line.alpha = lineAlpha;
      line.color = new Color3.White();
    }
  }

  for (let yi = 0; yi <= y; yi += stepY) {
    for (let zi = 0; zi <= z; zi += stepZ) {
      const line = MeshBuilder.CreateLines(`line-y${yi}-z${zi}`, {
        points: [new Vector3(0 - x / 2, yi, zi - z / 2), new Vector3(x - x / 2, yi, zi - z / 2)],
      });
      line.alpha = lineAlpha;
      line.color = new Color3.White();
    }
  }
}

export function useBlockerCache() {
  return {};
}

export function useDroneCache() {
  return {};
}

export function useFocusCache({ scene }) {
  // Create selection light
  const selectionLight = new PointLight("selection-light", new Vector3(0, 0, 0), scene);
  selectionLight.range = 0;
  selectionLight.intensity = 0;

  // Create nearField
  const nearFieldSphere = MeshBuilder.CreateSphere("near-field-sphere", { segments: 8, diameter: 1 }, scene);
  nearFieldSphere.scaling = new Vector3(0, 0, 0);
  const nearFieldMaterial = new StandardMaterial("near-field-material", scene);
  nearFieldMaterial.wireframe = true;
  nearFieldMaterial.alpha = 0.2;
  nearFieldSphere.material = nearFieldMaterial;

  // Create farField
  const farFieldSphere = MeshBuilder.CreateSphere("far-field-sphere", { segments: 16, diameter: 1 }, scene);
  farFieldSphere.scaling = new Vector3(0, 0, 0);
  const farFieldMaterial = new StandardMaterial("far-field-material", scene);
  farFieldMaterial.wireframe = true;
  farFieldMaterial.alpha = 0.05;
  farFieldSphere.material = farFieldMaterial;

  return {
    selectionLight,
    nearFieldSphere,
    nearFieldMaterial,
    farFieldSphere,
    farFieldMaterial,
  };
}

export function useBlockers({ scene, blockerCache, shadows, x, z, blockerMaterial }) {
  const simulation = useSimulationSingleton();

  // Create blockers
  simulation.activeBlockers.forEach((blocker) => {
    if (!(blocker.id in blockerCache)) {
      const blockerCube = MeshBuilder.CreateBox(
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
    storedBlockerCube.position.x = blocker.positionAtTick(simulation.tick).x - x / 2;
    storedBlockerCube.position.y = blocker.positionAtTick(simulation.tick).y + blocker.dimension.y / 2;
    storedBlockerCube.position.z = blocker.positionAtTick(simulation.tick).z - z / 2;
  });
}

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

export function useFocusFunctions({ x, y, z, focusCache, mainLight, hemisphereLight }) {
  const simulation = useSimulationSingleton();
  const focusOn = ({ agent, agent_x, agent_y, agent_z }) => {
    // Turn on focus light
    const { selectionLight } = focusCache;
    selectionLight.position.x = agent_x - x / 2;
    selectionLight.position.y = agent_y;
    selectionLight.position.z = agent_z - z / 2;
    selectionLight.diffuse = new Color3.FromHexString(agent.color);
    selectionLight.specular = new Color3.FromHexString(agent.color);
    selectionLight.range = y * 2;
    selectionLight.intensity = 2;

    // Turn off main light
    focusCache.mainLightIntensity = mainLight.intensity;
    mainLight.intensity = 0;

    // Turn off hemisphere light
    focusCache.hemisphereLightIntensity = hemisphereLight.intensity;
    hemisphereLight.intensity = 0.5;

    // Activate NearField
    const { nearFieldSphere, nearFieldMaterial } = focusCache;
    const nearR = agent.nearRadius * 2;
    nearFieldSphere.scaling = new Vector3(nearR, nearR, nearR);
    nearFieldSphere.position.x = agent_x - x / 2;
    nearFieldSphere.position.y = agent_y;
    nearFieldSphere.position.z = agent_z - z / 2;
    nearFieldMaterial.diffuseColor = new Color3.FromHexString(agent.color);
    nearFieldMaterial.emissiveColor = new Color3.FromHexString(agent.color);

    // Activate FarField
    const { farFieldSphere, farFieldMaterial } = focusCache;
    const farR = agent.farRadius * 2;
    farFieldSphere.scaling = new Vector3(farR, farR, farR);
    farFieldSphere.position.x = agent_x - x / 2;
    farFieldSphere.position.y = agent_y;
    farFieldSphere.position.z = agent_z - z / 2;
    farFieldMaterial.diffuseColor = new Color3.FromHexString(agent.color);
    farFieldMaterial.emissiveColor = new Color3.FromHexString(agent.color);

    simulation.focusOnAgent(agent);
  };
  const focusOff = () => {
    // Turn off focus light
    const { selectionLight } = focusCache;
    selectionLight.intensity = 0.0;

    // Turn on main light
    mainLight.intensity = focusCache.mainLightIntensity;

    // Turn on hemisphere light
    hemisphereLight.intensity = focusCache.hemisphereLightIntensity;

    // Disable Near-/ Farfield Spheres
    const { nearFieldSphere, farFieldSphere } = focusCache;
    nearFieldSphere.scaling = new Vector3(0, 0, 0);
    farFieldSphere.scaling = new Vector3(0, 0, 0);
  };
  return {
    focusOn,
    focusOff,
  };
}

export function useDrones({ scene, droneCache, x, z, focusOn }) {
  const simulation = useSimulationSingleton();

  // Push new meshes
  simulation.activeAgents.forEach((agent) => {
    const path = agent.paths.find((p) => p.isActiveAtTick(simulation.tick));
    const { x: agent_x, y: agent_y, z: agent_z } = agent.combinedPath.at(simulation.tick);

    if (!(agent.id in droneCache)) {
      // Draw path
      const points = path.ticksInAir.map((_t, i) => {
        const { x: ax, y: ay, z: az } = path.atIndex(i);
        return new Vector3(ax - x / 2, ay, az - z / 2);
      });
      const agentPathLine = MeshBuilder.CreateLines(`line-agent-${agent.id}`, {
        points,
      });
      agentPathLine.alpha = 0.5;
      agentPathLine.color = new Color3.FromHexString(agent.color);

      // create Material
      const ownerMaterial = new StandardMaterial(`material-agent-${agent.id}`, scene);
      ownerMaterial.diffuseColor = new Color3.FromHexString(agent.color);
      ownerMaterial.emissiveColor = new Color3.FromHexString(agent.color);
      ownerMaterial.alpha = 1;

      // Draw drone
      const agentLocationSphere = MeshBuilder.CreateSphere(
        `sphere-agent-${agent.id}`,
        { segments: 4, diameter: 1 },
        scene
      );
      agentLocationSphere.material = ownerMaterial;
      agentLocationSphere.isPickable = true;
      agentLocationSphere.actionManager = new ActionManager(scene);

      agentLocationSphere.actionManager.registerAction(
        new ExecuteCodeAction(ActionManager.OnPickTrigger, () => focusOn({ agent, agent_x, agent_y, agent_z }))
      );

      droneCache[agent.id] = [agentPathLine, agentLocationSphere];
    }

    // Update sphere position
    const storedAgentLocationSphere = droneCache[agent.id][1];
    storedAgentLocationSphere.position.x = agent_x - x / 2;
    storedAgentLocationSphere.position.y = agent_y;
    storedAgentLocationSphere.position.z = agent_z - z / 2;
  });
}

export function updateDrones({ scene, droneCache, x, z, focusOn }) {
  const simulation = useSimulationSingleton();

  // Remove unused meshes
  const activeUUIDs = simulation.activeAgentIDs;
  Object.entries(droneCache).forEach(([uuid, meshes]) => {
    if (!(uuid in activeUUIDs)) {
      meshes.forEach((mesh) => {
        mesh.dispose();
      });
      delete droneCache[uuid];
    }
  });
  useDrones({ scene, droneCache, x, z, focusOn });
}
