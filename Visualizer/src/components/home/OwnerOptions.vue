<template>
  <owner-form v-model="value" />
  <h3>Start:</h3>
  <div style="margin-left: 5px">
    <owner-stop v-model="value.start.stop" :dimension="dimension" :map-info="mapInfo" />
  </div>
  <template v-if="value.type === 'abc'">
    <h3>Stops:</h3>
    <div style="margin-left: 5px">
      <n-dynamic-input v-model:value="value.stops" :on-create="onCreate">
        <template #default="{ value }">
          <owner-stop v-model="value.stop" :dimension="dimension" :map-info="mapInfo" />
        </template>
      </n-dynamic-input>
    </div>
  </template>
  <h3>Target:</h3>
  <div style="margin-left: 5px">
    <owner-stop v-model="value.target.stop" :dimension="dimension" :map-info="mapInfo" />
  </div>
</template>

<script setup>
import { ref, watchEffect } from "vue";
import OwnerForm from "./OwnerForm.vue";
import OwnerStop from "./OwnerStop.vue";
import { createDefaultStop } from "../../scripts/stops";

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

const onCreate = () => {
  return createDefaultStop();
};

const value = ref({ ...props.modelValue });
watchEffect(() => (value.value = props.modelValue));
watchEffect(() => updateValue(value.value));
const emit = defineEmits(["update:modelValue"]);
function updateValue(updatedValue) {
  emit("update:modelValue", updatedValue);
}
</script>
