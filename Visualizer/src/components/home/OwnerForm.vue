<template>
  <n-color-picker :modes="['hex']" :show-alpha="false" v-model:value="config.color" />
  <n-input v-model:value="config.name" type="text" placeholder="Owner Name" />
  <n-input-number v-model:value="config.agents" :min="1" :max="100" style="min-width: 130px" placeholder="Nr. Agents" />
  <n-select
    v-model:value="config.type"
    :options="Object.values(options)"
    label-field="_label"
    value-field="classname"
    placeholder="Type"
    filterable
  />
</template>

<script setup>
import { ref, watchEffect } from "vue";

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
  options: {
    type: Object,
    required: true,
  },
});
// todo: This is beyond ugly. pls refactor @Thomas
const config = ref({ ...props.modelValue });
watchEffect(() => (config.value = props.modelValue));
watchEffect(() => {
  updateValue(config.value);
});
const emit = defineEmits(["update:modelValue"]);
function updateValue(updatedValue) {
  emit("update:modelValue", updatedValue);
}
</script>

<style scoped></style>
