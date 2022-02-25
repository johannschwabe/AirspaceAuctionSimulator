<template>
  <n-grid cols="12">
    <n-grid-item span="3">

      <n-grid cols="1">
        <n-grid-item>
          <heatmap />
        </n-grid-item>
        <n-grid-item>
          <heatmap />
        </n-grid-item>
        <n-grid-item>
          <heatmap />
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

    </n-grid-item>

  </n-grid>

  <n-grid cols="12">
    <n-grid-item span="12">
      <timeline />
    </n-grid-item>
  </n-grid>

</template>

<script setup>
import Heatmap from '../components/dashboard/Heatmap.vue'
import ThreeDMap from '../components/dashboard/ThreeDMap.vue'
import DataTable from '../components/dashboard/DataTable.vue'
import Timeline from '../components/dashboard/Timeline.vue'
</script>
