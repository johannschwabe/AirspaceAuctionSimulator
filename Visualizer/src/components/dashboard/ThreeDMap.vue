<template>
  <canvas ref="canvas" touch-action="none" @wheel.prevent="() => {}" />
</template>

<script setup>
import { ref, onMounted } from "vue";
import {
  Scene,
  Engine,
  ArcRotateCamera,
  MeshBuilder,
  Vector3,
  StandardMaterial,
  Color3,
  AxesViewer,
  DirectionalLight,
  Mesh,
  ActionManager,
  PointLight,
  ExecuteCodeAction,
  ShadowGenerator,
  HemisphericLight,
} from "babylonjs";
import { useSimulationStore } from "../../stores/simulation.js";
import { useAgentStore } from "../../stores/agent.js";

const simulationStore = useSimulationStore();
const agentStore = useAgentStore();

const canvas = ref(null);
let engine, scene, selectionLight, mainLight, hemisphereLight, shadows;

const x = simulationStore.dimensions.x;
const y = simulationStore.dimensions.y; // Direction of Sky
const z = simulationStore.dimensions.z;

const lengthOfAxis = Math.max(x, y, z) / 10;

const lineStep = 10; // Only draw an orientation line every x-th coordinate

const createScene = () => {
  const scene = new Scene(engine);
  scene.clearColor = Color3.FromHexString("#101010");

  const axes = new AxesViewer(scene, lengthOfAxis);
  axes.update(
    new Vector3(-x / 2, 0, -z / 2),
    new Vector3(1, 0, 0),
    new Vector3(0, 1, 0),
    new Vector3(0, 0, 1)
  );

  const target = new Vector3(0, (y / 4) * 3, 0);
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

  mainLight = new DirectionalLight(
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

  hemisphereLight = new HemisphericLight(
    "HemiLight",
    new Vector3(0, 1, 0),
    scene
  );
  hemisphereLight.intensity = 0.5;

  shadows = new ShadowGenerator(2048, mainLight);
  shadows.usePoissonSampling = true;

  const ground = MeshBuilder.CreateGround("ground", { width: x, height: z });
  const groundMaterial = new StandardMaterial(scene);
  groundMaterial.diffuseColor = new Color3.FromHexString("#313336");
  groundMaterial.alpha = 1;
  ground.material = groundMaterial;
  ground.receiveShadows = true;

  // Create selection  light
  selectionLight = new PointLight(
    "selection-light",
    new Vector3(0, 0, 0),
    scene
  );
  selectionLight.range = 0;
  selectionLight.intensity = 0;

  shadows.getShadowMap().refreshRate = 1;
  mainLight.autoUpdateExtends = false;

  return scene;
};

const activeDroneMeshes = {};
const activeBlockerMeshes = {};

const createOrientationLines = () => {
  // Create orientation lines
  const lineAlpha = 0.025;

  for (let xi = 0; xi < x; xi += lineStep) {
    for (let yi = 0; yi < y; yi += lineStep) {
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
  for (let xi = 0; xi < x; xi += lineStep) {
    for (let zi = 0; zi < z; zi += lineStep) {
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

  for (let yi = 0; yi < y; yi += lineStep) {
    for (let zi = 0; zi < z; zi += lineStep) {
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
};

const placeBlockers = () => {
  // Remove unused meshes
  const activeIDs = simulationStore.activeBlockerIDs;
  Object.entries(activeBlockerMeshes).forEach(([id, meshes]) => {
    if (!(id in activeIDs)) {
      meshes.forEach((mesh) => {
        mesh.dispose();
      });
      delete activeBlockerMeshes[id];
    }
  });

  // Create blockers
  const blockerMaterial = new StandardMaterial(scene);
  blockerMaterial.diffuseColor = new Color3.FromHexString("#313336");
  blockerMaterial.maxSimultaneousLights = 10;
  blockerMaterial.alpha = 1;

  simulationStore.activeBlockers.forEach((blocker) => {
    const timeIndex = blocker.t.indexOf(simulationStore.tick);

    if (!(blocker.id in activeBlockerMeshes)) {
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

      activeBlockerMeshes[blocker.id] = [blockerCube];
    }
    // Update blocker position
    const storedBlockerCube = activeBlockerMeshes[blocker.id][0];
    storedBlockerCube.position.x = blocker.x[timeIndex] - x / 2;
    storedBlockerCube.position.y =
      blocker.y[timeIndex] + blocker.dimension.y / 2;
    storedBlockerCube.position.z = blocker.z[timeIndex] - z / 2;
  });
};

const placeDrones = () => {
  // Remove unused meshes
  const activeUUIDs = simulationStore.activeAgentIDs;
  Object.entries(activeDroneMeshes).forEach(([uuid, meshes]) => {
    if (!(uuid in activeUUIDs)) {
      meshes.forEach((mesh) => {
        mesh.dispose();
      });
      delete activeDroneMeshes[uuid];
    }
  });

  // Push new meshes
  simulationStore.activeAgents.forEach((agent) => {
    const path = agent.paths.find((p) => p.t.includes(simulationStore.tick));
    const currentLocIndex = path.t.findIndex((t) => t === simulationStore.tick);

    if (!(agent.id in activeDroneMeshes)) {
      // Draw path
      const points = path.t.map(
        (_t, i) => new Vector3(path.x[i] - x / 2, path.y[i], path.z[i] - z / 2)
      );
      const agentPathLine = MeshBuilder.CreateLines(`line-agent-${agent.id}`, {
        points,
      });
      agentPathLine.alpha = 0.5;
      agentPathLine.color = new Color3.FromHexString(agent.owner.color);

      // create Material
      const ownerMaterial = new StandardMaterial(scene);
      ownerMaterial.diffuseColor = new Color3.FromHexString(agent.owner.color);
      ownerMaterial.emissiveColor = new Color3.FromHexString(agent.owner.color);
      ownerMaterial.alpha = 1;

      // Draw drone
      const agentLocationSphere = Mesh.CreateSphere(
        `sphere-agent-${agent.id}`,
        16,
        1,
        scene
      );
      agentLocationSphere.material = ownerMaterial;
      agentLocationSphere.isPickable = true;
      agentLocationSphere.actionManager = new ActionManager(scene);

      agentLocationSphere.actionManager.registerAction(
        new ExecuteCodeAction(ActionManager.OnPickTrigger, () => {
          agentStore.select(agent);
          selectionLight.position.x = path.x[currentLocIndex] - x / 2;
          selectionLight.position.y = path.y[currentLocIndex];
          selectionLight.position.z = path.z[currentLocIndex] - z / 2;
          selectionLight.diffuse = new Color3.FromHexString(agent.owner.color);
          selectionLight.specular = new Color3.FromHexString(agent.owner.color);
          selectionLight.range = y * 2;
          selectionLight.intensity = 2;
          mainLight.intensity = 0.1;
          hemisphereLight.intensity = 0.1;
        })
      );

      activeDroneMeshes[agent.id] = [agentPathLine, agentLocationSphere];
    }

    // Update sphere position
    const storedAgentLocationSphere = activeDroneMeshes[agent.id][1];
    storedAgentLocationSphere.position.x = path.x[currentLocIndex] - x / 2;
    storedAgentLocationSphere.position.y = path.y[currentLocIndex];
    storedAgentLocationSphere.position.z = path.z[currentLocIndex] - z / 2;
  });
};

simulationStore.$subscribe(() => {
  placeBlockers();
  placeDrones();
});

onMounted(() => {
  engine = new Engine(canvas.value, true, {
    preserveDrawingBuffer: true,
    stencil: true,
  });

  scene = createScene();
  createOrientationLines();
  placeBlockers();
  placeDrones();

  // run the render loop
  engine.runRenderLoop(() => {
    scene.render();
  });

  // the canvas/window resize event handler
  window.addEventListener("resize", function () {
    engine.resize();
  });
});
</script>

<style scoped>
canvas {
  width: 100%;
  height: 750px;
  outline: none;
  -webkit-tap-highlight-color: rgba(255, 255, 255, 0);
}
</style>
