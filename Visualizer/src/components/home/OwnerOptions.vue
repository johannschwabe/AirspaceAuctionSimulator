<template>
  <owner-form v-model="value" />
  <h3>Stops:</h3>
  <div style="margin-left: 5px">
    <n-dynamic-input v-model:value="stops" :on-create="onCreate">
      <template #default="{ value }">
        <n-grid :cols="1" y-gap="5">
          <n-grid-item>
            <n-select v-model:value="value.type" :options="options" placeholder="Type" filterable />
          </n-grid-item>
          <n-grid-item v-if="value.type === 'heatmap'">
            <owner-heatmap :dimension="dimension" :map-info="mapInfo" />
          </n-grid-item>
        </n-grid>
      </template>
    </n-dynamic-input>
  </div>
</template>

<script setup>
import { defineProps, ref, watchEffect } from "vue";
import OwnerForm from "./OwnerForm.vue";
import OwnerHeatmap from "./OwnerHeatmap.vue";

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
  mapInfo: {
    type: Object,
    required: false,
    default: null,
  },
  dimension: {
    type: Object,
    required: true,
  },
});

const stops = ref([
  {
    type: "random",
  },
]);

const onCreate = () => {
  return {
    type: "random",
  };
};

const options = [
  {
    label: "Random",
    value: "random",
  },
  {
    label: "Coordinate",
    value: "coord",
  },
  {
    label: "Heatmap",
    value: "heatmap",
  },
];

const value = ref({ ...props.modelValue });

watchEffect(() => (value.value = props.modelValue));
watchEffect(() => updateValue(value.value));

const emit = defineEmits(["update:modelValue"]);

function updateValue(updatedValue) {
  emit("update:modelValue", updatedValue);
}
</script>

<style scoped></style>
