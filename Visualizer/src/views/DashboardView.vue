<template>
  <div class="nav-margin">
    <n-grid cols="12">
      <n-grid-item span="3">

        <n-grid cols="1">
          <n-grid-item>
            <heatmap dim-x="x" dim-y="z" title="Top-Down View"/>
          </n-grid-item>
          <n-grid-item>
            <heatmap dim-x="x" dim-y="y" title="Front View"/>
          </n-grid-item>
          <n-grid-item>
            <heatmap  dim-x="z" dim-y="y" title="Side View"/>
          </n-grid-item>
        </n-grid>

      </n-grid-item>

      <n-grid-item span="6">
        <n-grid cols="1">
          <n-grid-item>
            <three-d-map />
          </n-grid-item>
          <n-grid-item>
            <data-table />
          </n-grid-item>
        </n-grid>
      </n-grid-item>

      <n-grid-item span="3">
        <n-grid cols="1">
          <n-grid-item>
            <welfare />
          </n-grid-item>
        </n-grid>
      </n-grid-item>

    </n-grid>

    <n-grid cols="1">
      <n-grid-item>
        <gantt />
      </n-grid-item>
    </n-grid>
  </div>

  <div class="abs-nav">
    <timeline />
  </div>

</template>

<script setup>
import Heatmap from '../components/dashboard/Heatmap.vue'
import ThreeDMap from '../components/dashboard/ThreeDMap.vue'
import DataTable from '../components/dashboard/DataTable.vue'
import Timeline from '../components/dashboard/Timeline.vue'
import Gantt from "../components/dashboard/Gantt.vue";
import Welfare from "../components/dashboard/Welfare.vue";
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
</style>
