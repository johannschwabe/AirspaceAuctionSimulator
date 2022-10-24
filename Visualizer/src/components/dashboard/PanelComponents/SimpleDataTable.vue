<template>
  <h3 v-if="title">
    {{ title }}
  </h3>
  <h4 v-if="subtitle">
    {{ subtitle }}
  </h4>
  <div
    v-for="datapoint in datapoints"
    :key="datapoint.label"
    @click="datapoint.onClick"
    :style="{ cursor: datapoint.onClick ? 'pointer' : 'default' }"
  >
    <div style="display: flex">
      <div style="display: flex; flex-direction: column; justify-content: center; margin-right: 10px">
        <n-icon :component="datapoint.icon" :depth="5" size="25" />
      </div>
      <div>
        <div style="color: rgba(255, 255, 255, 0.52); font-size: 12px">
          {{ datapoint.label }}
        </div>
        <n-text :type="datapoint.color ?? 'default'" v-html="formatData(datapoint.value)">
        </n-text>
      </div>
    </div>
    <n-divider style="margin-top: 6px; margin-bottom: 6px" />
  </div>
</template>

<script setup>
import {isArray, isFunction, isNumber, isObject} from "lodash-es";

const props = defineProps({
  title: { type: String, required: false },
  subtitle: { type: String, required: false },
  datapoints: { type: Array, required: true },
});

function formatData(data) {
  if (isNumber(data)) {
    return Math.round(data * 100) / 100;
  }
  if (isFunction(data)) {
    return data();
  }
  if (isArray(data)) {
    return data.join(", ");
  }
  if (isObject(data)) {
    let s = "";
    Object.entries(data).forEach(([key, value]) => {
      s = `${s} ${key}: ${value}`;
    });
    return s;
  }
  return data;
}
</script>

<style scoped></style>
