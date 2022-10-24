<template>
  <canvas ref="canvas" touch-action="none" @wheel.prevent="() => {}" />
</template>

<script setup>
import { ref, onMounted } from "vue";
import { onAgentsSelected, onFocusOffAgent, onFocusOnAgent, onTick } from "@/scripts/emitter.js";
import { useSimulationSingleton } from "@/scripts/simulationSingleton.js";
import SpaceAgent from "@/SimulationObjects/SpaceAgent.js";
import PathAgent from "@/SimulationObjects/PathAgent.js";
import {
  useAxisIndicators,
  useGround,
  useHemisphereLight,
  useMainLight,
  useOrientationLines,
  useShadows,
} from "@/engine/environment";
import { useEngine } from "@/engine";
import { useCamera, useScene } from "@/engine/scene";
import { useBuildings } from "@/engine/buildings";
import { updateDrones, useDrones } from "@/engine/drones";
import { useBlockerCache, useDroneCache, useFocusCache } from "@/engine/cache";
import { updateBlockers, useBlockerMaterial, useBlockers } from "@/engine/blockers";
import { updateFocus, useFocusFunctions } from "@/engine/focus";

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

const doDroneUpdate = async () => {
  await updateDrones({ scene, droneCache, x, z, focusOnSpaceAgent, focusOnPathAgent });
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
  if (focusAgentInvisible) {
    return;
  }
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

onTick(async () => {
  doBlockerUpdate();
  await doDroneUpdate();
  doFocusUpdate();
});

onAgentsSelected(() => {
  doDroneUpdate();
});

onMounted(async () => {
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
  useOrientationLines({
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
  await useDrones({
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
  height: 1050px;
  outline: none;
  -webkit-tap-highlight-color: rgba(255, 255, 255, 0);
}
</style>
