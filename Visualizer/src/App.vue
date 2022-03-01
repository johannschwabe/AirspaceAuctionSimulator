<template>
  <n-config-provider :theme="darkTheme">
    <n-loading-bar-provider>
      <n-message-provider>
        <n-notification-provider>
          <n-dialog-provider>
            <router-view />
          </n-dialog-provider>
        </n-notification-provider>
      </n-message-provider>
    </n-loading-bar-provider>
  </n-config-provider>
</template>


<script setup>
import { darkTheme } from 'naive-ui'
</script>

<style>
body {
  background-color: rgb(16, 16, 16);
}
</style>
