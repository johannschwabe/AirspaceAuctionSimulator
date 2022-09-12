<template>
  <canvas ref="canvas" touch-action="none" @wheel.prevent="() => {}" />
</template>

<script setup>
import { ref, onMounted } from "vue";
import { onAgentsSelected, onFocusOffAgent, onFocusOnAgent, onTick } from "@/scripts/emitter";
import {
  updateBlockers,
  updateDrones,
  updateFocus,
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
  useShadows,
} from "@/scripts/3dmap";
import { useSimulationSingleton } from "@/scripts/simulation";
import SpaceAgent from "@/SimulationObjects/SpaceAgent";
import PathAgent from "@/SimulationObjects/PathAgent";

const simulation = useSimulationSingleton();

const canvas = ref(null);

let engine, scene, camera;
let mainLight, hemisphereLight, selectionLight;
let shadows;
let focusOnSpaceAgent, focusOnPathAgent, focusOffSpaceAgent, focusOffPathAgent, focusAgentInvisible;
let droneCache, blockerCache, focusCache;
let blockerMaterial;

const { x, y, z } = simulation.dimensions;

const lineAlpha = 0.075;

const doBlockerUpdate = () => {
  updateBlockers({ scene, blockerCache, shadows, x, y, z, blockerMaterial });
};

const doDroneUpdate = () => {
  updateDrones({ scene, droneCache, x, z, focusOnSpaceAgent, focusOnPathAgent });
};

const doFocusUpdate = () => {
  if (!simulation.agentInFocus) {
    return;
  }
  const focusAgentInvisibleBefore = focusAgentInvisible;
  const focusAgentInvisibleNow = !simulation.agentInFocus.isActiveAtTick(simulation.tick);

  if (simulation.agentInFocus && !focusAgentInvisibleNow && focusAgentInvisibleBefore) {
    focusOnAgent({ agentInFocus: simulation.agentInFocus });
  } else if (simulation.agentInFocus && focusAgentInvisibleNow && !focusAgentInvisibleBefore) {
    focusOffAgent(simulation.agentInFocus);
  } else {
    updateFocus({
      focusCache,
      focusOnSpaceAgent,
      focusOnPathAgent,
      focusOffSpaceAgent,
      focusOffPathAgent,
    });
  }
  focusAgentInvisible = focusAgentInvisibleNow;
};

function focusOnAgent({ agentInFocus: agent }) {
  focusAgentInvisible = !simulation.agentInFocus.isActiveAtTick(simulation.tick);
  if (focusAgentInvisible) { return; }
  if (agent instanceof SpaceAgent) {
    const space = agent.spaces.find((s) => s.isActiveAtTick(simulation.tick));
    focusOnSpaceAgent({ agent, space });
  }
  if (agent instanceof PathAgent) {
    const { x: agent_x, y: agent_y, z: agent_z } = agent.combinedPath.at(simulation.tick);
    focusOnPathAgent({ agent, agent_x, agent_y, agent_z });
  }
}
onFocusOnAgent(({ previousAgentInFocus }) => {
  focusOffAgent(previousAgentInFocus);
  focusOnAgent({ agentInFocus: simulation.agentInFocus });
});

function focusOffAgent(agent) {
  if (agent instanceof SpaceAgent) {
    focusOffSpaceAgent();
  }
  if (agent instanceof PathAgent) {
    focusOffPathAgent();
  }
}
onFocusOffAgent(focusOffAgent);

onTick(() => {
  doBlockerUpdate();
  doDroneUpdate();
  doFocusUpdate();
});

onAgentsSelected(() => {
  doDroneUpdate();
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

  camera = useCamera({ x, y, z, scene, canvas });
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
    droneCache,
    camera,
  });
  focusOnSpaceAgent = focusFunctions.focusOnSpaceAgent;
  focusOnPathAgent = focusFunctions.focusOnPathAgent;
  focusOffSpaceAgent = focusFunctions.focusOffSpaceAgent;
  focusOffPathAgent = focusFunctions.focusOffPathAgent;
  useBlockers({ scene, blockerCache, shadows, x, z, blockerMaterial });
  useBuildings({
    scene,
    shadows,
    mapTiles: simulation.mapTiles,
    blockerMaterial,
  });
  useDrones({
    scene,
    droneCache,
    x,
    z,
    focusOnSpaceAgent,
    focusOnPathAgent,
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
