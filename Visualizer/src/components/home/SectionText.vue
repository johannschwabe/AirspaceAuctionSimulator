<template>
  <div style="text-align: center; color: white">
    <h1>{{ title }}</h1>
    <n-text style="font-size: 16px">
      {{ text }}
    </n-text>
  </div>
</template>

<script setup>
// eslint-disable-next-line no-unused-vars
const props = defineProps(["title", "text"]);
</script>

<style scoped></style>
