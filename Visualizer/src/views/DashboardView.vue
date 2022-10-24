<template>
  <div v-if="loading" class="loading">
    <n-avatar :src="loadingGif" color="transparent" />
    <p>Loading...</p>
  </div>
  <div v-else id="dashbaord">
    <top-bar />

    <n-divider />

    <div class="nav-margin">
      <n-grid cols="12">
        <!-- Left Part -->
        <n-grid-item span="2" id="agent-selector">
          <n-grid cols="1">
            <n-grid-item>
              <agent-selector />
            </n-grid-item>
          </n-grid>
        </n-grid-item>

        <!-- Central Part -->
        <n-grid-item span="8" id="drawer-target">
          <n-grid cols="1">
            <n-grid-item>
              <three-d-map />
            </n-grid-item>
          </n-grid>
        </n-grid-item>

        <!-- Right Part -->
        <n-grid-item span="2">
          <n-grid cols="1">
            <n-grid-item>
              <welfare />
              <n-divider style="margin-top: 0; margin-bottom: 0" />
            </n-grid-item>
            <n-grid-item>
              <heatmap dim-x="x" dim-y="z" title="Top-Down View" />
              <n-divider style="margin-top: 0; margin-bottom: 0" />
            </n-grid-item>
            <n-grid-item>
              <heatmap dim-x="x" dim-y="y" title="Front View" />
              <n-divider style="margin-top: 0; margin-bottom: 0" />
            </n-grid-item>
            <n-grid-item>
              <heatmap dim-x="z" dim-y="y" title="Side View" />
              <n-divider style="margin-top: 0; margin-bottom: 0" />
            </n-grid-item>
          </n-grid>
        </n-grid-item>
      </n-grid>

      <n-divider />

      <!-- Bottom Part -->
      <n-grid cols="1">
        <n-grid-item>
          <gantt />
        </n-grid-item>
      </n-grid>
    </div>

    <!-- Left Drawer -->
    <n-drawer
      :show="simulationStore.agentInFocus"
      :width="250"
      placement="left"
      :trap-focus="false"
      :block-scroll="false"
      :close-on-esc="false"
      :mask-closable="false"
      :on-update:show="(show) => show || simulation.focusOff()"
      display-directive="if"
      to="#drawer-target"
    >
      <n-drawer-content
        :title="'Owner: ' + simulation.ownerInFocus?.displayName"
        :closable="true"
        :key="simulationStore.ownerInFocusId || 0"
      >
        <owner-info />
      </n-drawer-content>
    </n-drawer>

    <!-- Right Drawer -->
    <n-drawer
      :show="simulationStore.agentInFocus"
      :width="250"
      placement="right"
      :trap-focus="false"
      :block-scroll="false"
      :close-on-esc="false"
      :mask-closable="false"
      :on-update:show="(show) => show || simulation.focusOff()"
      display-directive="if"
      to="#drawer-target"
    >
      <n-drawer-content
        :title="'Agent: ' + simulation.agentInFocus?.displayName"
        :closable="true"
        :key="simulationStore.agentInFocusId || 0"
      >
        <agent-info />
      </n-drawer-content>
    </n-drawer>

    <div class="abs-nav">
      <timeline />
    </div>
  </div>
</template>

<script setup>
import { nextTick, onUnmounted, ref, shallowRef } from "vue";
import { useRouter } from "vue-router";
import { useLoadingBar, useMessage } from "naive-ui";
import PerfectScrollbar from "perfect-scrollbar";

import loadingGif from "../assets/loading.gif";
import TopBar from "../components/dashboard/TopBar.vue";
import ThreeDMap from "../components/dashboard/Engine.vue";
import Heatmap from "../components/dashboard/PlayfieldStatisticsPanel/Heatmap.vue";
import Gantt from "../components/dashboard/GanttChart.vue";
import Welfare from "../components/dashboard/PlayfieldStatisticsPanel/UtilityGraph.vue";
import AgentInfo from "../components/dashboard/AgentPanel.vue";
import AgentSelector from "../components/dashboard/AgentSelector.vue";
import OwnerInfo from "../components/dashboard/OwnerPanel.vue";
import Timeline from "../components/dashboard/Timeline.vue";
import { offAll } from "../scripts/emitter.js";
import {
  hasSimulationSingleton,
  loadSimulationConfig,
  loadSimulationSingleton,
  useSimulationSingleton,
} from "../scripts/simulationSingleton.js";
import { useSimulationOutputStore } from "../stores/simulationOutputStore.js";

const router = useRouter();
const message = useMessage();
const loadingBar = useLoadingBar();

const loading = ref(true);
const simulation = shallowRef({});

const simulationStore = useSimulationOutputStore();

let agentScroller;
onUnmounted(() => {
  agentScroller.destroy();
  agentScroller = null;
});

if (!hasSimulationSingleton()) {
  loadSimulationSingleton()
    .then((simulationSingleton) => {
      loadSimulationConfig();
      message.success("Simulation recovered!");
      simulation.value = simulationSingleton;
    })
    .catch((e) => {
      message.error(e.message);
      router.push("/");
      throw new Error(e);
    })
    .finally(() => {
      loading.value = false;
      nextTick(() => {
        const container = document.querySelector("#agent-selector");
        agentScroller = new PerfectScrollbar(container);
        loadingBar.finish();
      });
    });
} else {
  message.success("Simulation loaded!");
  simulation.value = useSimulationSingleton();
  loadingBar.finish();
  loading.value = false;
  const allAgentIds = [];
  simulation.value.owners.forEach((owner) => {
    allAgentIds.push(owner.id);
    owner.agents.forEach((agent) => {
      allAgentIds.push(agent.id);
    });
  });
  simulationStore.setSelectedAgentIDs(allAgentIds);
  nextTick(() => {
    const container = document.querySelector("#agent-selector");
    agentScroller = new PerfectScrollbar(container);
  });
}

onUnmounted(() => {
  offAll();
});
</script>

<style scoped>
.abs-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 140px;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0) 0%, rgba(0, 0, 0, 0.8) 20%, rgba(0, 0, 0, 1) 100%);
  z-index: 2010;
}
.nav-margin {
  margin-bottom: 100px;
}
#drawer-target {
  position: relative;
  overflow: hidden;
  border-left: 1px solid rgba(255, 255, 255, 0.09);
  border-right: 1px solid rgba(255, 255, 255, 0.09);
}
#drawer-target :deep(.n-drawer-mask) {
  background-color: transparent;
  pointer-events: none;
}
.loading {
  position: absolute;
  top: 2px;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-content: center;
  justify-content: center;
  align-items: center;
  color: #969696;
}
#agent-selector {
  position: relative;
  height: 950px;
  overflow: hidden;
}
</style>
