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
          <!--          <n-grid-item>-->
          <!--            <heatmap dim-x="x" dim-y="z" title="Top-Down View" />-->
          <!--          </n-grid-item>-->
          <!--          <n-grid-item>-->
          <!--            <heatmap dim-x="x" dim-y="y" title="Front View" />-->
          <!--          </n-grid-item>-->
          <!--          <n-grid-item>-->
          <!--            <heatmap dim-x="z" dim-y="y" title="Side View" />-->
          <!--          </n-grid-item>-->
        </n-grid>
      </n-grid-item>

      <!-- Central Part -->
      <n-grid-item span="6" id="drawer-target">
        <n-grid cols="1">
          <n-grid-item>
            <!--            <three-d-map />-->
          </n-grid-item>
        </n-grid>
      </n-grid-item>

      <!-- Right Part -->
      <n-grid-item span="3">
        <n-grid cols="1">
          <n-grid-item>
            <!--            <welfare />-->
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
        <!--        <gantt />-->
      </n-grid-item>
    </n-grid>
  </div>

  <!-- Left Drawer -->
  <n-drawer
    :show="ownerStore.selected"
    :width="250"
    placement="left"
    :trap-focus="false"
    :close-on-esc="false"
    :mask-closable="false"
    :on-update:show="(show) => show || ownerStore.deselect()"
    to="#drawer-target"
  >
    <n-drawer-content :title="ownerStore.name" :closable="true">
      <owner-info />
    </n-drawer-content>
  </n-drawer>

  <!-- Right Drawer -->
  <n-drawer
    :show="agentStore.selected"
    :width="250"
    placement="right"
    :trap-focus="false"
    :close-on-esc="false"
    :mask-closable="false"
    :on-update:show="(show) => show || agentStore.deselect()"
    to="#drawer-target"
  >
    <n-drawer-content :title="agentStore.name" :closable="true">
      <agent-info />
    </n-drawer-content>
  </n-drawer>

  <div class="abs-nav">
    <!--    <timeline />-->
  </div>
</template>

<script setup>
import { ref } from "vue";

// import Heatmap from "../components/dashboard/Heatmap.vue";
import ThreeDMap from "../components/dashboard/ThreeDMap.vue";
import DataTable from "../components/dashboard/DataTable.vue";
import Timeline from "../components/dashboard/Timeline.vue";
import Gantt from "../components/dashboard/Gantt.vue";
import Welfare from "../components/dashboard/Welfare.vue";
import TopBar from "../components/dashboard/TopBar.vue";
import AgentSelector from "../components/dashboard/AgentSelector.vue";
import AgentInfo from "../components/dashboard/AgentInfo.vue";
import { useAgentStore } from "../stores/agent.js";
import { useSimulationStore } from "../stores/simulation.js";
import { useOwnerStore } from "../stores/owner.js";
import OwnerInfo from "../components/dashboard/OwnerInfo.vue";

const simulationStore = useSimulationStore();
const ownerStore = useOwnerStore();
const agentStore = useAgentStore();

agentStore.select(simulationStore.agents[0]);
</script>

<style scoped>
.abs-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 75px;
  background-color: rgb(16, 16, 16);
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
