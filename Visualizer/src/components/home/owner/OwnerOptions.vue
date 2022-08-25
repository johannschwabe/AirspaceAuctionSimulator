<template>
  <n-h3>Stops</n-h3>
  <n-dynamic-input
    :value="owner.locations"
    :on-create="onCreate"
    :on-remove="onRemove"
    :min="owner.minLocations"
    :max="owner.maxLocations"
  >
    <template #default="{ index }">
      <owner-stop :ownerIndex="props.ownerIndex" :locationIndex="index" />
    </template>
  </n-dynamic-input>
  <template v-if="meta.length > 0">
    <n-divider />
    <n-h3>Customization Options</n-h3>
  </template>
  <n-form ref="formRef" label-placement="left" require-mark-placement="right-hanging" label-width="auto">
    <n-form-item v-for="m in meta" :label="m.label" :key="m.key">
      <component
        :is="metaInputResolver[m.type].componentName"
        v-model:value="m.value"
        v-bind="metaInputResolver[m.type].props"
        :placeholder="m.label"
      />
      <n-text depth="3" style="padding-left: 24px">
        {{ m.description }}
      </n-text>
    </n-form-item>
  </n-form>
  <n-divider />
  <p>{{ ownerProperties.label }}: {{ ownerProperties.description }}</p>
</template>

<script setup>
import { computed } from "vue";
import OwnerStop from "./OwnerStop.vue";
import { useSimulationConfigStore } from "@/stores/simulationConfig";

const props = defineProps({
  ownerIndex: {
    type: Number,
    required: true,
  },
});

const simulationConfig = useSimulationConfigStore();

const owner = computed(() => simulationConfig.owners[props.ownerIndex]);

/**
 * Returns config of owner of fitting type
 * @type {ComputedRef<OwnerConfig>}
 */
const ownerProperties = computed(() => {
  return simulationConfig.availableOwnersForAllocator.find((o) => o.classname === owner.value.classname);
});

/**
 * @type {ComputedRef<RawMeta>}
 */
const meta = computed(() => owner.value.meta);

const metaInputResolver = {
  int: {
    componentName: "NInputNumber",
    props: {
      precision: 0,
    },
  },
  float: {
    componentName: "NInputNumber",
    props: {
      precision: 2,
    },
  },
  text: {
    componentName: "NInput",
  },
  boolean: {
    componentName: "NCheckbox",
  },
};

/**
 * Creates a new random location at given index
 * @param {number} index
 * @returns {LocationConfig}
 */
const onCreate = (index) => {
  const location = simulationConfig.randomLocation();
  owner.value.locations.splice(index, 0, location);
  return location;
};

/**
 * Removes location at given index
 * @param {number} index
 */
const onRemove = (index) => {
  owner.value.locations.splice(index, 1);
};
</script>
