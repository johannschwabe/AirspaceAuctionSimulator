<template>
  <div style="text-align: center; color: white">
    <h1>{{ title }}</h1>
    <n-text style="font-size: 16px">
      {{ text }}
    </n-text>
  </div>
</template>

<script setup>
defineProps(["title", "text"]);
</script>

<style scoped></style>
