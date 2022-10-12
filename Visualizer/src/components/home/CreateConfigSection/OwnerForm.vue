<template>
  <!-- Inputs for color, name and number of agents -->
  <n-form-item class="small-form">
    <template #label v-if="ownerIndex === 0">
      <help v-bind="hOwnerColor">Color</help>
    </template>
    <n-color-picker :modes="['hex']" :show-alpha="false" v-model:value="owner.color"/>
  </n-form-item>
  <n-form-item class="small-form">
    <template #label v-if="ownerIndex === 0">
      <help v-bind="hOwnerName">Owner Name</help>
    </template>
    <n-input v-model:value="owner.name" type="text" placeholder="Owner Name" />
  </n-form-item>
  <n-form-item class="small-form">
    <template #label v-if="ownerIndex === 0">
      <help v-bind="hOwnerAgents">Nr. Agents</help>
    </template>
    <n-input-number
      v-model:value="owner.agents"
      :min="1"
      :max="100"
      style="min-width: 130px"
      placeholder="Nr. Agents"
    />
  </n-form-item>
  <!-- Dropdown selection for owner type -->
  <n-form-item class="small-form">
    <template #label v-if="ownerIndex === 0">
      <help v-bind="hOwnerBidding">Bidding Strategy</help>
    </template>
    <n-select
      v-model:value="biddingStrategy"
      :options="simulationConfig.availableBiddingStrategiesOptions"
      placeholder="Type"
      @on-update:value="biddingStrategySelected"
    />
  </n-form-item>
  <!-- Dropdown selection for owner type -->
  <n-form-item class="small-form">
    <template #label v-if="ownerIndex === 0">
      <help v-bind="hOwnerValue">Value Function</help>
    </template>
    <n-select v-model:value="owner.valueFunction" :options="compatibleValueFunctions" placeholder="Type" />
  </n-form-item>
</template>

<script setup>
import { computed, ref, watch } from "vue";
import { useSimulationConfigStore } from "../../../stores/simulationConfigStore.js";
import { getSupportedValueFunctions } from "../../../API/api";
import Help from "@/components/common/help/help.vue";
import { hOwnerColor, hOwnerName, hOwnerAgents, hOwnerBidding, hOwnerValue } from "@/components/common/help/texts.js";

const props = defineProps({
  ownerIndex: {
    type: Number,
    required: true,
  },
});

const simulationConfig = useSimulationConfigStore();

const owner = computed(() => simulationConfig.owners[props.ownerIndex]);
loadCompatibleValueFunctions();

const biddingStrategy = ref(owner.value.biddingStrategy.classname);
/**
 * Whenever the selected ownerType changes, make sure the requirements for minimum
 * and maximum number of locations are met
 */

const compatibleValueFunctions = ref([]);
function loadCompatibleValueFunctions() {
  getSupportedValueFunctions(simulationConfig.allocator, owner.value.biddingStrategy.classname).then((res) => {
    compatibleValueFunctions.value = res.map((a) => ({ label: a.label, value: a.classname }));
    const compatible = compatibleValueFunctions.value.find((comp) => {
      return comp.value === owner.value.valueFunction;
    });
    if (!compatible) {
      owner.value.valueFunction = compatibleValueFunctions.value[0].value;
    }
  });
}
const biddingStrategySelected = () => {
  if (owner.value.locations.length > owner.value.biddingStrategy.maxLocations) {
    owner.value.locations = owner.value.locations.slice(0, owner.value.biddingStrategy.maxLocations);
  }
  while (owner.value.locations.length < owner.value.biddingStrategy.minLocations) {
    owner.value.locations.push(simulationConfig.randomLocation());
  }
};

watch(
  () => biddingStrategy.value,
  () => {
    owner.value.biddingStrategy = simulationConfig.getBiddingStrategy(biddingStrategy.value);
    loadCompatibleValueFunctions();
  }
);
</script>

<style scoped>
.small-form :deep(.n-form-item-feedback-wrapper) {
  display: none;
}
.small-form :deep(.n-form-item-label) {
  margin-top: -24px;
}
.small-form {
  grid-template-rows: none;
  min-width: 75px;
}
</style>
