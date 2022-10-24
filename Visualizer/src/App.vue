<template>
  <n-config-provider :theme="darkTheme">
    <n-loading-bar-provider>
      <n-message-provider>
        <n-notification-provider>
          <n-dialog-provider>
            <div class="content">
              <router-view />
            </div>
          </n-dialog-provider>
        </n-notification-provider>
      </n-message-provider>
    </n-loading-bar-provider>
  </n-config-provider>
</template>

<script setup>
import { darkTheme } from "naive-ui";
</script>

<style>
body {
  background-color: rgb(16, 16, 16);
}
.content {
  max-width: 2100px;
  margin: 0 auto;
}
.n-drawer {
  background-color: rgb(16, 16, 16);
}
#dashbaord {
  padding: 15px;
}
#dashbaord .n-drawer {
  background-color: rgba(16, 16, 16, 0.81);
}
#dashbaord .n-drawer .n-drawer-content .n-drawer-body-content-wrapper {
  padding-right: 0 !important;
}
</style>
