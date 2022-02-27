<template>
  <div>
    <n-slider v-model:value="simulationStore.tick" :max="simulationStore.dimensions.t" show-tooltip />
  </div>
</template>

<script setup>
import {useSimulationStore} from "../../stores/simulation";

const simulationStore = useSimulationStore();

</script>

<style scoped>

</style>
