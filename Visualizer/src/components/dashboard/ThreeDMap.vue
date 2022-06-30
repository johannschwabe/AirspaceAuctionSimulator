<template>
  <canvas ref="canvas" touch-action="none" @wheel.prevent="() => {}" />
</template>

<script setup>
import { ref, onMounted } from "vue";
import { onAgentsSelected, onFocusOffAgent, onTick } from "../../scripts/emitter";
import {
  updateBlockers,
  updateDrones, updateFocus,
  useAxisIndicators,
  useBlockerCache,
  useBlockerMaterial,
  useBlockers,
  useBuildings,
  useCamera,
  useDroneCache,
  useDrones,
  useEngine,
  useFocusCache,
  useFocusFunctions,
  useGround,
  useHemisphereLight,
  useMainLight,
  useOrientationLights,
  useScene,
  useShadows
} from "../../scripts/3dmap";
import { useSimulationSingleton } from "../../scripts/simulation";

const simulation = useSimulationSingleton();

const canvas = ref(null);

let engine, scene;
let mainLight, hemisphereLight, selectionLight;
let shadows;
let focusOn, focusOff;
let droneCache, blockerCache, focusCache;
let blockerMaterial;

const { x, y, z } = simulation.dimensions;

const lineAlpha = 0.075;

const doBlockerUpdate = () => {
  updateBlockers({ scene, blockerCache, shadows, x, y, z, blockerMaterial });
};

const doDroneUpdate = () => {
  updateDrones({ scene, droneCache, x, z, focusOn });
};

const doFocusUpdate = () => {
  updateFocus({
    focusCache,
    focusOn,
    focusOff,
  });
};

onTick(() => {
  console.log("3D TICK!");
  doBlockerUpdate();
  doDroneUpdate();
  doFocusUpdate();
});

onAgentsSelected(() => {
  doDroneUpdate();
});

onFocusOffAgent(() => {
  focusOff();
});

onMounted(() => {
  engine = useEngine({ canvas });
  scene = useScene({ engine });
  mainLight = useMainLight({ scene, x, y, z });
  hemisphereLight = useHemisphereLight({ scene });
  shadows = useShadows({ mainLight });

  droneCache = useDroneCache();
  blockerCache = useBlockerCache();
  focusCache = useFocusCache({ scene });

  blockerMaterial = useBlockerMaterial({ scene });

  useCamera({ x, y, z, scene, canvas });
  useGround({ scene, x, y, z });

  useAxisIndicators({ scene, x, y, z });
  useOrientationLights({
    lineAlpha,
    x,
    y,
    z,
  });
  const focusFunctions = useFocusFunctions({
    x,
    y,
    z,
    focusCache,
    mainLight,
    hemisphereLight,
    selectionLight,
  });
  focusOn = focusFunctions.focusOn;
  focusOff = focusFunctions.focusOff;
  useBlockers({ scene, blockerCache, shadows, x, z, blockerMaterial });
  useBuildings({ scene, shadows, mapTiles: simulation.mapTiles, blockerMaterial });
  useDrones({
    scene,
    droneCache,
    x,
    z,
    focusOn,
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
