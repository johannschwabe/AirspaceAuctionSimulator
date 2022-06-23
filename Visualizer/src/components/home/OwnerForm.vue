<template>
  <n-color-picker :modes="['hex']" :show-alpha="false" v-model:value="value.color" />
  <n-input v-model:value="value.name" type="text" placeholder="Owner Name" />
  <n-input-number v-model:value="value.agents" :min="1" :max="100" style="min-width: 130px" placeholder="Nr. Agents" />
  <n-select v-model:value="value.type" :options="options" placeholder="Type" filterable />
</template>

<script setup>
import { ref, watchEffect } from "vue";

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
});

const value = ref({ ...props.modelValue });

watchEffect(() => (value.value = props.modelValue));
watchEffect(() => updateValue(value.value));

const emit = defineEmits(["update:modelValue"]);

function updateValue(updatedValue) {
  emit("update:modelValue", updatedValue);
}

const options = [
  {
    label: "A to B",
    value: "ab",
  },
  {
    label: "A to B to A",
    value: "aba",
  },
  {
    label: "A to B to C",
    value: "abc",
  },
  {
    label: "Stationary",
    value: "stat",
  },
];
</script>

<style scoped></style>
