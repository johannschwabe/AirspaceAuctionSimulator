import {
  ActionManager,
  ArcRotateCamera,
  AxesViewer,
  Color3,
  DirectionalLight,
  Engine,
  ExecuteCodeAction,
  HemisphericLight,
  Mesh,
  MeshBuilder,
  PointLight,
  Scene,
  ShadowGenerator,
  StandardMaterial,
  Vector3,
} from "babylonjs";
import { useSimulationStore } from "../stores/simulation";
import { useAgentStore } from "../stores/agent";

export function useEngine({ canvas }) {
  return new Engine(canvas.value, true, {
    preserveDrawingBuffer: true,
    stencil: true,
  });
}

export function useScene({ engine }) {
  const scene = new Scene(engine);
  scene.clearColor = Color3.FromHexString("#101010");
  return scene;
}

export function useMainLight({ scene, x, y, z }) {
  const mainLight = new DirectionalLight(
    "directionalLight",
    new Vector3(-1, -1, -1),
    scene
  );
  mainLight.diffuse = new Color3.FromHexString("#ffffff");
  mainLight.specular = new Color3.FromHexString("#63e2b7");
  mainLight.groundColor = new Color3.FromHexString("#44ab87");
  mainLight.intensity = 1;
  mainLight.position.x = x / 2;
  mainLight.position.y = y / 2;
  mainLight.position.z = z / 2;
  return mainLight;
  y;
}

export function useCamera({ x, y, z, scene, canvas }) {
  const target = new Vector3(0, (y / 4) * 2, 0);
  const camera = new ArcRotateCamera(
    "camera",
    -Math.PI / 2,
    Math.PI / 2.5,
    3,
    target,
    scene
  );
  camera.attachControl(canvas, true);
  camera.setTarget(target);
  camera.setPosition(new Vector3(-x, y * 2.5, -z));
  return camera;
}

export function useHemisphereLight({ scene }) {
  const hemisphereLight = new HemisphericLight(
    "HemiLight",
    new Vector3(0, 1, 0),
    scene
  );
  hemisphereLight.intensity = 0.5;
  return hemisphereLight;
}

export function useAxisIndicators({ scene, x, y, z }) {
  const lengthOfAxis = Math.max(x, y, z) / 10;
  const axes = new AxesViewer(scene, lengthOfAxis);
  axes.update(
    new Vector3(-x / 2, 0, -z / 2),
    new Vector3(1, 0, 0),
    new Vector3(0, 1, 0),
    new Vector3(0, 0, 1)
  );
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
  const groundMaterial = new StandardMaterial(scene);
  groundMaterial.diffuseColor = new Color3.FromHexString("#313336");
  groundMaterial.alpha = 1;
  ground.material = groundMaterial;
  ground.receiveShadows = true;
  return ground;
}

export function useSelectionLight({ scene }) {
  const selectionLight = new PointLight(
    "selection-light",
    new Vector3(0, 0, 0),
    scene
  );
  selectionLight.range = 0;
  selectionLight.intensity = 0;
  return selectionLight;
}

export function useOrientationLights({ nLines, minLines, lineAlpha, x, y, z }) {
  const lineStep = Math.max(
    Math.floor(Math.min(x / nLines, y / nLines, z / nLines)),
    minLines
  );

  for (let xi = 0; xi <= x; xi += lineStep) {
    for (let yi = 0; yi <= y; yi += lineStep) {
      const line = MeshBuilder.CreateLines(`line-x${xi}-y${yi}`, {
        points: [
          new Vector3(xi - x / 2, yi, 0 - z / 2),
          new Vector3(xi - x / 2, yi, z - z / 2),
        ],
      });
      line.alpha = lineAlpha;
      line.color = new Color3.White();
    }
  }
  for (let xi = 0; xi <= x; xi += lineStep) {
    for (let zi = 0; zi <= z; zi += lineStep) {
      const line = MeshBuilder.CreateLines(`line-x${xi}-z${zi}`, {
        points: [
          new Vector3(xi - x / 2, 0, zi - z / 2),
          new Vector3(xi - x / 2, y, zi - z / 2),
        ],
      });
      line.alpha = lineAlpha;
      line.color = new Color3.White();
    }
  }

  for (let yi = 0; yi <= y; yi += lineStep) {
    for (let zi = 0; zi <= z; zi += lineStep) {
      const line = MeshBuilder.CreateLines(`line-y${yi}-z${zi}`, {
        points: [
          new Vector3(0 - x / 2, yi, zi - z / 2),
          new Vector3(x - x / 2, yi, zi - z / 2),
        ],
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

export function useBlockers({ scene, blockerCache, shadows, x, z }) {
  const simulationStore = useSimulationStore();

  // Create blockers
  const blockerMaterial = new StandardMaterial(scene);
  blockerMaterial.diffuseColor = new Color3.FromHexString("#313336");
  blockerMaterial.maxSimultaneousLights = 10;
  blockerMaterial.alpha = 1;

  simulationStore.activeBlockers.forEach((blocker) => {
    const timeIndex = blocker.t.indexOf(simulationStore.tick);

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
    storedBlockerCube.position.x = blocker.x[timeIndex] - x / 2;
    storedBlockerCube.position.y =
      blocker.y[timeIndex] + blocker.dimension.y / 2;
    storedBlockerCube.position.z = blocker.z[timeIndex] - z / 2;
  });
}

export function updateBlockers({ scene, blockerCache, shadows, x, z }) {
  const simulationStore = useSimulationStore();

  // Remove unused meshes
  const activeIDs = simulationStore.activeBlockerIDs;
  Object.entries(blockerCache).forEach(([id, meshes]) => {
    if (!(id in activeIDs)) {
      meshes.forEach((mesh) => {
        mesh.dispose();
      });
      delete blockerCache[id];
    }
  });

  useBlockers({ scene, blockerCache, shadows, x, z });
}

export function useDrones({
  scene,
  droneCache,
  x,
  y,
  z,
  mainLight,
  hemisphereLight,
  selectionLight,
}) {
  const simulationStore = useSimulationStore();
  const agentStore = useAgentStore();

  // Push new meshes
  simulationStore.activeAgents.forEach((agent) => {
    const path = agent.paths.find((p) => p.t.includes(simulationStore.tick));
    const [agent_x, agent_y, agent_z] = agent.positions[simulationStore.tick];

    if (!(agent.id in droneCache)) {
      // Draw path
      const points = path.t.map(
        (_t, i) => new Vector3(path.x[i] - x / 2, path.y[i], path.z[i] - z / 2)
      );
      const agentPathLine = MeshBuilder.CreateLines(`line-agent-${agent.id}`, {
        points,
      });
      agentPathLine.alpha = 0.5;
      agentPathLine.color = new Color3.FromHexString(agent.owner_color);

      // create Material
      const ownerMaterial = new StandardMaterial(scene);
      ownerMaterial.diffuseColor = new Color3.FromHexString(agent.owner_color);
      ownerMaterial.emissiveColor = new Color3.FromHexString(agent.owner_color);
      ownerMaterial.alpha = 1;

      // Draw drone
      const agentLocationSphere = Mesh.CreateSphere(
        `sphere-agent-${agent.id}`,
        4,
        0.5,
        scene
      );
      agentLocationSphere.material = ownerMaterial;
      agentLocationSphere.isPickable = true;
      agentLocationSphere.actionManager = new ActionManager(scene);

      agentLocationSphere.actionManager.registerAction(
        new ExecuteCodeAction(ActionManager.OnPickTrigger, () => {
          agentStore.select(agent);
          selectionLight.position.x = agent_x - x / 2;
          selectionLight.position.y = agent_y;
          selectionLight.position.z = agent_z - z / 2;
          selectionLight.diffuse = new Color3.FromHexString(agent.owner_color);
          selectionLight.specular = new Color3.FromHexString(agent.owner_color);
          selectionLight.range = y * 2;
          selectionLight.intensity = 2;
          mainLight.intensity = 0.1;
          hemisphereLight.intensity = 0.1;
        })
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

export function updateDrones({
  scene,
  droneCache,
  x,
  y,
  z,
  mainLight,
  hemisphereLight,
  selectionLight,
}) {
  const simulationStore = useSimulationStore();
  // Remove unused meshes
  const activeUUIDs = simulationStore.activeAgentIDs;
  Object.entries(droneCache).forEach(([uuid, meshes]) => {
    if (!(uuid in activeUUIDs)) {
      meshes.forEach((mesh) => {
        mesh.dispose();
      });
      delete droneCache[uuid];
    }
  });
  useDrones({
    scene,
    droneCache,
    x,
    y,
    z,
    mainLight,
    hemisphereLight,
    selectionLight,
  });
}
