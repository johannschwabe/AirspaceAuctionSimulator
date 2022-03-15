<template>
  <n-dynamic-input v-model:value="owners" :on-create="onCreate">
    <template #default="{ value }">
      <div style="display: flex; column-gap: 10px; width: 100%">
        <n-color-picker :modes="['hex']" v-model:value="value.color" />
        <n-input
          v-model:value="value.name"
          type="text"
          placeholder="Owner Name"
        />
        <n-input-number
          v-model:value="value.agents"
          :min="1"
          :max="100"
          style="min-width: 130px"
          placeholder="Nr. Agents"
        />
        <n-select
          v-model:value="value.type"
          :options="options"
          placeholder="Type"
          filterable
        />
      </div>
    </template>
  </n-dynamic-input>
</template>

<script setup>
import { ref } from "vue";

const owners = ref([
  {
    color: "#00559d",
    name: "Digitec",
    agents: 20,
    type: "a-to-b",
  },
]);

const onCreate = () => {
  return {
    color: "#63e2b7",
    name: null,
    agents: null,
    type: null,
  };
};

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
    label: "Stationary",
    value: "stat",
  },
];

defineExpose({
  owners,
});
</script>

<style scoped></style>
