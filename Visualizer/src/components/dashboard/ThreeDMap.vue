<template>
  <canvas ref="canvas" touch-action="none" />
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { Scene, Engine, ArcRotateCamera, MeshBuilder, Vector3, StandardMaterial } from 'babylonjs';
import { useSimulationStore } from "../../stores/simulation";

const simulationStore = useSimulationStore();


const canvas = ref(null)
let engine, scene;

const x = simulationStore.dimensions.x;
const y = simulationStore.dimensions.y; // Direction of Sky
const z = simulationStore.dimensions.z;

const lineStep = 10; // Only draw an orientation line every x-th coordinate

const createScene = () => {
  const scene = new Scene(engine);
  scene.clearColor = BABYLON.Color3.FromHexString("#101014");

  const target = new Vector3(0,y/4*3,0)
  const camera = new ArcRotateCamera("camera", -Math.PI / 2, Math.PI / 2.5, 3, target, scene);
  camera.attachControl(canvas, true);
  camera.setTarget(target);
  camera.setPosition(new BABYLON.Vector3(x, y*2.5, z));

  const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(-1, 1, 0), scene);
  light.diffuse = new BABYLON.Color3.FromHexString("#ffffff");
  light.specular = new BABYLON.Color3.FromHexString("#63e2b7");
  light.groundColor = new BABYLON.Color3.FromHexString("#44ab87");
  light.intensity = 2;

  const ground = MeshBuilder.CreateGround("ground", {width:x, height:z});
  const groundMaterial = new StandardMaterial(scene);
  groundMaterial.diffuseColor = new BABYLON.Color3.Black();
  groundMaterial.alpha = 0.05;
  ground.material = groundMaterial;

  const lineAlpha = 0.05;

  for (let xi = 0; xi < x; xi+=lineStep) {
    for (let yi = 0; yi < y; yi+=lineStep) {
      const line = MeshBuilder.CreateLines(`line-x${xi}-y${yi}`, {
        points: [ new Vector3(xi-x/2, yi, 0-z/2), new Vector3(xi-x/2, yi, z-z/2) ]
      })
      line.alpha = lineAlpha
      line.color = new BABYLON.Color3.White();
    }
  }
  for (let xi = 0; xi < x; xi+=lineStep) {
    for (let zi = 0; zi < z; zi+=lineStep) {
      const line = MeshBuilder.CreateLines(`line-x${xi}-z${zi}`, {
        points: [ new Vector3(xi-x/2, 0, zi-z/2), new Vector3(xi-x/2, y, zi-z/2) ]
      })
      line.alpha = lineAlpha
      line.color = new BABYLON.Color3.White();
    }
  }

  for (let yi = 0; yi < y; yi+=lineStep) {
    for (let zi = 0; zi < z; zi+=lineStep) {
      const line = MeshBuilder.CreateLines(`line-y${yi}-z${zi}`, {
        points: [ new Vector3(0-x/2, yi, zi-z/2), new Vector3(x-x/2, yi, zi-z/2) ]
      })
      line.alpha = lineAlpha
      line.color = new BABYLON.Color3.White();
    }
  }

  simulationStore.owners.forEach((owner, oi) => {
    owner.agents.forEach((agent, ai) => {
      const points = agent.locations.map((loc) => new Vector3(loc.x-x/2, loc.y, loc.z-z/2));
      const line = MeshBuilder.CreateLines(`line-owner${oi}-agent${ai}`, { points })
      line.alpha = 0.5
      line.color = new BABYLON.Color3.FromHexString(owner.color);
    })
  })

  return scene;
}

const placeDrones = () => {
  simulationStore.owners.forEach((owner, oi) => {
    owner.agents.forEach((agent, ai) => {
      const ownerMaterial = new StandardMaterial(scene);
      ownerMaterial.diffuseColor = new BABYLON.Color3.FromHexString(owner.color);
      ownerMaterial.alpha = 1;
      agent.locations.forEach((loc) => {
        console.log(loc.t, simulationStore.tick);
        if (loc.t === simulationStore.tick) {
          console.log("Creating SPHEEERE");
          const sphere = BABYLON.Mesh.CreateSphere(`sphere-owner${oi}-agent${ai}`, 16, 1, scene);
          sphere.position.x = loc.x-x/2;
          sphere.position.y = loc.y;
          sphere.position.z = loc.z-z/2;
          sphere.material = ownerMaterial;
        }
      })
    })
  })
}

watch(simulationStore.tick, (t) => {
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
  height: 65vh;
  outline: none;
  -webkit-tap-highlight-color: rgba(255, 255, 255, 0);
}
</style>
