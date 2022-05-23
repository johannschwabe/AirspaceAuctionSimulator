<template>
  <canvas ref="canvas" touch-action="none" @wheel.prevent="() => {}" />
</template>

<script setup>
import { ref, onMounted } from "vue";
import { onAgentsSelected, onFocusOffAgent, onTick } from "../../scripts/emitter";
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
  useFocusCache,
  useFocusFunctions,
  useGround,
  useHemisphereLight,
  useMainLight,
  useOrientationLights,
  useScene,
  useShadows,
} from "../../scripts/3dmap";
import { useSimulationSingleton } from "../../scripts/simulation";

const simulation = useSimulationSingleton();

const canvas = ref(null);

let engine, scene;
let mainLight, hemisphereLight, selectionLight;
let shadows;
let focusOn, focusOff;
let droneCache, blockerCache, focusCache;

const { x, y, z } = simulation.dimensions;

const nLines = 2;
const lineAlpha = 0.075;

const doBlockerUpdate = () => {
  updateBlockers({ scene, blockerCache, shadows, x, y, z });
};

const doDroneUpdate = () => {
  updateDrones({ scene, droneCache, x, z, focusOn });
};

onTick(() => {
  console.log("3D TICK!");
  doBlockerUpdate();
  doDroneUpdate();
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

  useCamera({ x, y, z, scene, canvas });
  useGround({ scene, x, y, z });

  useAxisIndicators({ scene, x, y, z });
  useOrientationLights({
    nLines,
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
  useBlockers({ scene, blockerCache, shadows, x, z });
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
