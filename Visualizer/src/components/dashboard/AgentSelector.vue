<template>
  <n-space vertical :size="12">
    <n-input v-model:value="pattern" placeholder="Search" />
    <n-tree
      block-line
      cascade
      checkable
      :data="data"
      :pattern="pattern"
      key-field="id"
      label-field="name"
      children-field="agents"
      :default-checked-keys="simulationStore.selectedAgentIDs"
      @update:checked-keys="updateCheckedKeys"
    />
    <n-button
      block
      ghost
      type="primary"
      @click.stop="apply"
      :disabled="!changeMade"
    >
      Apply selection
    </n-button>
  </n-space>
</template>

<script setup>
import { isEmpty, xor } from "lodash-es";
import { ref, computed } from "vue";
import { useSimulationStore } from "../../stores/simulation";
import { useSimulationSingleton } from "../../scripts/simulation";

const simulationStore = useSimulationStore();
const simulation = useSimulationSingleton();

const pattern = ref("");
const selectedAgentIDs = ref([...simulationStore.selectedAgentIDs]);
const data = simulation.owners;

const changeMade = computed(() => {
  return !isEmpty(
    xor(selectedAgentIDs.value, simulationStore.selectedAgentIDs)
  );
});

const updateCheckedKeys = (v) => {
  selectedAgentIDs.value = v;
  console.log("setSelectedAgentIDs", v);
};

const apply = () => {
  simulationStore.setSelectedAgentIDs(selectedAgentIDs.value);
};
</script>

<style scoped></style>
