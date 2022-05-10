<template>
  <top-bar />

  <n-divider />

  <div class="nav-margin">
    <n-grid cols="12">
      <!-- Left Part -->
      <n-grid-item span="3">
        <n-grid cols="1">
          <n-grid-item>
            <agent-selector />
          </n-grid-item>
        </n-grid>
      </n-grid-item>

      <!-- Central Part -->
      <n-grid-item span="6" id="drawer-target">
        <n-grid cols="1">
          <n-grid-item>
            <three-d-map />
          </n-grid-item>
        </n-grid>
      </n-grid-item>

      <!-- Right Part -->
      <n-grid-item span="3">
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
        <!--        <data-table />-->
      </n-grid-item>
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
    :close-on-esc="false"
    :mask-closable="false"
    :on-update:show="(show) => show || simulation.focusOff()"
    display-directive="if"
    to="#drawer-target"
  >
    <n-drawer-content
      :title="simulation.ownerInFocus?.name"
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
    :close-on-esc="false"
    :mask-closable="false"
    :on-update:show="(show) => show || simulation.focusOff()"
    display-directive="if"
    to="#drawer-target"
  >
    <n-drawer-content
      :title="simulation.agentInFocus?.name"
      :closable="true"
      :key="simulationStore.agentInFocusId || 0"
    >
      <agent-info />
    </n-drawer-content>
  </n-drawer>

  <div class="abs-nav">
    <timeline />
  </div>
</template>

<script setup>
import { onUnmounted } from "vue";
import { useRouter } from "vue-router";

// import DataTable from "../components/dashboard/DataTable.vue";
import TopBar from "../components/dashboard/TopBar.vue";
import AgentSelector from "../components/dashboard/AgentSelector.vue";
import ThreeDMap from "../components/dashboard/ThreeDMap.vue";
import Heatmap from "../components/dashboard/Heatmap.vue";
import Gantt from "../components/dashboard/Gantt.vue";
import Welfare from "../components/dashboard/Welfare.vue";
import AgentInfo from "../components/dashboard/AgentInfo.vue";
import OwnerInfo from "../components/dashboard/OwnerInfo.vue";
import Timeline from "../components/dashboard/Timeline.vue";
import { offAll } from "../scripts/emitter";
import { hasSimulationSingleton, loadSimulationSingleton, useSimulationSingleton } from "../scripts/simulation";
import { useSimulationStore } from "../stores/simulation";
import { useLoadingBar, useMessage } from "naive-ui";

const router = useRouter();
const message = useMessage();
const loadingBar = useLoadingBar();

if (!hasSimulationSingleton()) {
  try {
    loadSimulationSingleton();
    message.success("Simulation recovered!");
  } catch (e) {
    console.error(e);
    message.error(e.message);
    router.push("/");
  } finally {
    loadingBar.finish();
  }
} else {
  message.success("Simulation loaded!");
  loadingBar.finish();
}

const simulationStore = useSimulationStore();
const simulation = useSimulationSingleton();

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
  background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.8) 20%, rgba(0,0,0,1) 100%);
  z-index: 1000;
}
.nav-margin {
  margin-bottom: 80px;
}
#drawer-target {
  position: relative;
  overflow: hidden;
  border-left: 1px solid rgba(255, 255, 255, 0.09);
  border-right: 1px solid rgba(255, 255, 255, 0.09);
}
#drawer-target /deep/ .n-drawer-mask {
  background-color: transparent;
  pointer-events: none;
}
</style>
