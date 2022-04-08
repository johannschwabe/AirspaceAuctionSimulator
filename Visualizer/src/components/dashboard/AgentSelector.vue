<template>
  <n-space vertical :size="12">
    <n-input v-model:value="pattern" placeholder="Search" />
    <n-tree
      block-line
      cascade
      checkable
      :data="data"
      :pattern="pattern"
      key-field="uuid"
      label-field="name"
      children-field="agents"
      @update:checked-keys="updateCheckedKeys"
    />
  </n-space>
</template>

<script setup>
import { ref } from "vue";

const pattern = ref("");
const data = [
  {
    name: "Owner 1",
    uuid: "owner-1-uuid",
    agents: [
      { name: "Agent 1", uuid: "owner-1-agent-1-uuid" },
      { name: "Agent 2", uuid: "owner-1-agent-2-uuid" },
      { name: "Agent 3", uuid: "owner-1-agent-3-uuid" },
    ],
  },
  {
    name: "Owner 2",
    uuid: "owner-2-uuid",
    agents: [
      { name: "Agent 1", uuid: "owner-2-agent-1-uuid" },
      { name: "Agent 2", uuid: "owner-2-agent-2-uuid" },
      { name: "Agent 3", uuid: "owner-2-agent-3-uuid" },
    ],
  },
];
const updateCheckedKeys = (v) => {
  console.log("updateCheckedKeys", v);
};
</script>

<style scoped></style>
