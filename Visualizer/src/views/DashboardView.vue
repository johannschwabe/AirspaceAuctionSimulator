<template>
  <top-bar
    name="<My Model>"
    description="<My Model Description>"
    :dimension-x="10"
    :dimension-y="20"
    :dimension-z="30"
    :n-owners="3"
    :n-agents="45"
    :achieved-welfare="200"
    :n-collisions="99"
    :n-reallocations="23"
  />

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
            <three-d-map />
          </n-grid-item>
        </n-grid>
      </n-grid-item>

      <!-- Right Part -->
      <n-grid-item span="3">
        <n-grid cols="1">
          <n-grid-item>
            <welfare />
          </n-grid-item>
        </n-grid>
      </n-grid-item>
    </n-grid>

    <n-divider />

    <!-- Bottom Part -->
    <n-grid cols="1">
      <n-grid-item>
        <data-table />
      </n-grid-item>
      <n-grid-item>
        <gantt />
      </n-grid-item>
    </n-grid>
  </div>

  <!-- Left Drawer -->
  <n-drawer
    v-model:show="activeLeft"
    :width="200"
    placement="left"
    :trap-focus="false"
    :close-on-esc="false"
    :mask-closable="false"
    to="#drawer-target"
  >
    <n-drawer-content title="Left Drawer" :closable="true">
      Stoner is a 1965 novel by the American writer John Williams.
    </n-drawer-content>
  </n-drawer>

  <!-- Right Drawer -->
  <n-drawer
    v-model:show="activeRight"
    :width="200"
    placement="right"
    :trap-focus="false"
    :close-on-esc="false"
    :mask-closable="false"
    to="#drawer-target"
  >
    <n-drawer-content title="Right Drawer" :closable="true">
      Stoner is a 1965 novel by the American writer John Williams.
    </n-drawer-content>
  </n-drawer>

  <div class="abs-nav">
    <timeline />
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

const activeLeft = ref(true);
const activeRight = ref(true);
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
#drawer-target >>> .n-drawer-mask {
  background-color: transparent;
  pointer-events: none;
}

</style>
