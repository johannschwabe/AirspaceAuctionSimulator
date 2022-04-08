<template>
  <n-data-table
    ref="table"
    :columns="columns"
    :data="data"
    :pagination="pagination"
    :row-key="(row) => row.address"
    @update:checked-row-keys="handleCheck"
  />
</template>

<script setup>
import { ref } from "vue";
const columns = [
  {
    type: "selection",
    disabled(row, index) {
      return row.name === "Edward King 3";
    },
  },
  {
    title: "Name",
    key: "name",
  },
  {
    title: "Age",
    key: "age",
  },
  {
    title: "Address",
    key: "address",
  },
];

const data = Array.apply(null, { length: 46 }).map((_, index) => ({
  name: `Edward King ${index}`,
  age: 32,
  address: `London, Park Lane no. ${index}`,
}));

const checkedRowKeysRef = ref([]);

const handleCheck = (rowKeys) => {
  checkedRowKeysRef.value = rowKeys;
};
</script>

<style scoped></style>
