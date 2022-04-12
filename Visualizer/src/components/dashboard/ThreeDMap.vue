<template>
  <canvas ref="canvas" touch-action="none" @wheel.prevent="() => {}" />
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useSimulationStore } from "../../stores/simulation.js";
import { useEmitter } from "../../scripts/emitter";
import {
  updateBlockers,
  updateDrones,
  useAxisIndicators,
  useBlockerCache,
  useBlockers,
  useCamera,
  useDroneCache,
  useDrones,
  useEngine,
  useGround,
  useHemisphereLight,
  useMainLight,
  useOrientationLights,
  useScene,
  useSelectionLight,
  useShadows,
} from "../../scripts/3dmap";

const simulationStore = useSimulationStore();
const emitter = useEmitter();

const canvas = ref(null);

let engine, scene;
let mainLight, hemisphereLight, selectionLight;
let shadows;

const { x, y, z } = simulationStore.dimensions;

const nLines = 10;
const lineAlpha = 0.075;
const minLines = 5;

const droneCache = useDroneCache();
const blockerCache = useBlockerCache();

emitter.on("tick", () => {
  console.log("3D Map: Tick");
  updateBlockers({ scene, blockerCache, shadows, x, y, z });
  updateDrones({
    scene,
    droneCache,
    x,
    y,
    z,
    mainLight,
    hemisphereLight,
    selectionLight,
  });
  console.log("3D Map: Done");
});

onMounted(() => {
  engine = useEngine({ canvas });
  scene = useScene({ engine });
  mainLight = useMainLight({ scene, x, y, z });
  hemisphereLight = useHemisphereLight({ scene });
  selectionLight = useSelectionLight({ scene });
  shadows = useShadows({ mainLight });

  useCamera({ x, y, z, scene, canvas });
  useGround({ scene, x, y, z });

  useAxisIndicators({ scene, x, y, z });
  useOrientationLights({
    nLines,
    minLines,
    lineAlpha,
    x,
    y,
    z,
  });
  useBlockers({ scene, blockerCache, shadows, x, z });
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

  // run the render loop
  engine.runRenderLoop(() => {
    scene.render();
  });

  // the canvas/window resize event handler
  window.addEventListener("resize", () => {
    engine.resize();
  });
});
</script>

<style scoped>
canvas {
  width: 100%;
  height: 950px;
  outline: none;
  -webkit-tap-highlight-color: rgba(255, 255, 255, 0);
}
</style>
