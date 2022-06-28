<template>
  <owner-form v-model="value" />
  <h3>Start:</h3>
  <div style="margin-left: 5px">
    <owner-stop v-model="value.start" :dimension="dimension" :map-info="mapInfo" />
  </div>
  <template v-if="value.type === 'abc'">
    <h3>Stops:</h3>
    <div style="margin-left: 5px">
      <n-dynamic-input v-model:value="value.stops" :on-create="onCreate">
        <template #default="{ value, index }">
          <owner-stop
            :model-value="value"
            @update:modelValue="updateStop(index, $event)"
            :dimension="dimension"
            :map-info="mapInfo"
          />
        </template>
      </n-dynamic-input>
    </div>
  </template>
  <h3>Target:</h3>
  <div style="margin-left: 5px">
    <owner-stop v-model="value.target" :dimension="dimension" :map-info="mapInfo" />
  </div>
</template>

<script setup>
import { ref, watchEffect } from "vue";
import OwnerForm from "./OwnerForm.vue";
import OwnerStop from "./OwnerStop.vue";

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

const defaultStop = {
  type: "random",
  position: null,
  heatmap: {},
};

const onCreate = () => {
  return {
    ...defaultStop,
  };
};

function updateStop(index, stop) {
  value.value.stops[index] = stop;
}

const value = ref({ ...props.modelValue });
watchEffect(() => (value.value = props.modelValue));
watchEffect(() => updateValue(value.value));
const emit = defineEmits(["update:modelValue"]);
function updateValue(updatedValue) {
  emit("update:modelValue", updatedValue);
}
</script>

<style scoped></style>
