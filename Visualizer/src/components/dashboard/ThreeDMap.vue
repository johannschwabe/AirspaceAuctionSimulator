<template>
  <canvas ref="canvas" touch-action="none" @wheel.prevent="() => {}"/>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { Scene, Engine, ArcRotateCamera, MeshBuilder, Vector3, StandardMaterial, Color3, AxesViewer, HemisphericLight, Mesh } from 'babylonjs';
import { useSimulationStore } from "../../stores/simulation";

const simulationStore = useSimulationStore();


const canvas = ref(null)
let engine, scene;

const x = simulationStore.dimensions.x;
const y = simulationStore.dimensions.y; // Direction of Sky
const z = simulationStore.dimensions.z;

const lengthOfAxis = Math.max(x, y, z) / 10

const lineStep = 10; // Only draw an orientation line every x-th coordinate

const createScene = () => {
  const scene = new Scene(engine);
  scene.clearColor = Color3.FromHexString("#101010");

  const axes = new AxesViewer(scene, lengthOfAxis)
  axes.update(new Vector3(-x/2, 0, -z/2), new Vector3(1,0,0), new Vector3(0,1,0), new Vector3(0,0,1));

  const target = new Vector3(0,y/4*3,0)
  const camera = new ArcRotateCamera("camera", -Math.PI / 2, Math.PI / 2.5, 3, target, scene);
  camera.attachControl(canvas, true);
  camera.setTarget(target);
  camera.setPosition(new Vector3(-x, y*2.5, -z));

  const light = new HemisphericLight("light", new Vector3(-1, 1, 0), scene);
  light.diffuse = new Color3.FromHexString("#ffffff");
  light.specular = new Color3.FromHexString("#63e2b7");
  light.groundColor = new Color3.FromHexString("#44ab87");
  light.intensity = 2;

  const ground = MeshBuilder.CreateGround("ground", {width:x, height:z});
  const groundMaterial = new StandardMaterial(scene);
  groundMaterial.diffuseColor = new Color3.Black();
  groundMaterial.alpha = 0.05;
  ground.material = groundMaterial;

  const lineAlpha = 0.025;

  for (let xi = 0; xi < x; xi+=lineStep) {
    for (let yi = 0; yi < y; yi+=lineStep) {
      const line = MeshBuilder.CreateLines(`line-x${xi}-y${yi}`, {
        points: [ new Vector3(xi-x/2, yi, 0-z/2), new Vector3(xi-x/2, yi, z-z/2) ]
      })
      line.alpha = lineAlpha
      line.color = new Color3.White();
    }
  }
  for (let xi = 0; xi < x; xi+=lineStep) {
    for (let zi = 0; zi < z; zi+=lineStep) {
      const line = MeshBuilder.CreateLines(`line-x${xi}-z${zi}`, {
        points: [ new Vector3(xi-x/2, 0, zi-z/2), new Vector3(xi-x/2, y, zi-z/2) ]
      })
      line.alpha = lineAlpha
      line.color = new Color3.White();
    }
  }

  for (let yi = 0; yi < y; yi+=lineStep) {
    for (let zi = 0; zi < z; zi+=lineStep) {
      const line = MeshBuilder.CreateLines(`line-y${yi}-z${zi}`, {
        points: [ new Vector3(0-x/2, yi, zi-z/2), new Vector3(x-x/2, yi, zi-z/2) ]
      })
      line.alpha = lineAlpha
      line.color = new Color3.White();
    }
  }
  return scene;
}

const activeMeshes = {}

const placeDrones = () => {
  // Remove unused meshes
  const activeUUIDs = simulationStore.activeAgentUUIDs;
  Object.entries(activeMeshes).forEach(([uuid, meshes]) => {
    if (!(uuid in activeUUIDs)) {
      meshes.forEach((mesh) => { mesh.dispose(); })
      delete activeMeshes[uuid];
    }
  })
  // Push new meshes
  simulationStore.activeAgents.forEach((agent) => {
    if (!(agent.uuid in activeMeshes)) {
      // Draw path
      const points = agent.locations.map((loc) => new Vector3(loc.x-x/2, loc.y, loc.z-z/2));
      const line = MeshBuilder.CreateLines(`line-agent-${agent.uuid}`, { points })
      line.alpha = 0.5
      line.color = new Color3.FromHexString(agent.owner.color);

      // create Material
      const ownerMaterial = new StandardMaterial(scene);
      ownerMaterial.diffuseColor = new Color3.FromHexString(agent.owner.color);
      ownerMaterial.alpha = 1;

      // Draw drone
      const sphere = Mesh.CreateSphere(`sphere-agent-${agent.uuid}`, 16, 1, scene);
      sphere.material = ownerMaterial;
      activeMeshes[agent.uuid] = [line, sphere]
    }

    // Update sphere position
    const sphere = activeMeshes[agent.uuid][1];
    const current_loc = agent.locations.find((loc) => loc.t === simulationStore.tick);
    sphere.position.x = current_loc.x-x/2;
    sphere.position.y = current_loc.y;
    sphere.position.z = current_loc.z-z/2;
  })
}

simulationStore.$subscribe(() => {
  placeDrones();
})

onMounted(() => {
  engine = new Engine(canvas.value, true, {preserveDrawingBuffer: true, stencil: true});

  scene = createScene();
  placeDrones();

  // run the render loop
  engine.runRenderLoop(() => {
    scene.render();
  });

  // the canvas/window resize event handler
  window.addEventListener('resize', function(){
    engine.resize();
  });
})

</script>

<style scoped>
canvas {
  width: 100%;
  height: 750px;
  outline: none;
  -webkit-tap-highlight-color: rgba(255, 255, 255, 0);
}
</style>
