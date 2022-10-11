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
      label-field="displayName"
      children-field="agents"
      :node-props="nodeProps"
      :render-suffix="renderSuffix"
      :default-checked-keys="simulationStore.selectedAgentIDs"
      @update:checked-keys="updateCheckedKeys"
    />
    <n-button block ghost type="primary" @click.stop="apply" :disabled="!changeMade"> Apply selection </n-button>
  </n-space>
</template>

<script setup>
import { isEmpty, xor } from "lodash-es";
import { ref, computed, h } from "vue";
import { useSimulationOutputStore } from "@/stores/simulationOutputStore";
import { useSimulationSingleton } from "@/scripts/simulationSingleton";
import Owner from "@/SimulationObjects/Owner";
import { NButton } from "naive-ui";

const simulationStore = useSimulationOutputStore();
const simulation = useSimulationSingleton();

const pattern = ref("");
const selectedAgentIDs = ref([...simulationStore.selectedAgentIDs]);
const data = simulation.owners;

const changeMade = computed(() => {
  return !isEmpty(xor(selectedAgentIDs.value, simulationStore.selectedAgentIDs));
});

const updateCheckedKeys = (v) => {
  selectedAgentIDs.value = v;
};

const apply = () => {
  simulationStore.setSelectedAgentIDs(selectedAgentIDs.value);
};

const renderSuffix = ({ option }) => {
  if (!(option instanceof Owner)) {
    const events = [];
    if (option.reAllocationTimesteps.length > 0) {
      events.push(
        h(NButton, { text: true, type: "warning", style: "padding: 0 5px" }, { default: () => "Reallocated" })
      );
    }
    if (option.flyingTicks.length === 0) {
      events.push(h(NButton, { text: true, type: "info", style: "padding: 0 5px" }, { default: () => "No Start" }));
    }
    if (option.totalViolations > 0) {
      events.push(h(NButton, { text: true, type: "error", style: "padding: 0 5px" }, { default: () => "Violations" }));
    }
    return events;
  }
};

const nodeProps = ({ option }) => ({
  onClick() {
    if (!(option instanceof Owner)) {
      simulation.focusOnAgent(option);
    }
  },
});
</script>

<style scoped></style>
