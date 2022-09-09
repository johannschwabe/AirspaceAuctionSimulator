<template>
  <div class="label">
    <n-tooltip trigger="hover">
      <template #trigger>
        <n-icon size="16" style="cursor: help" color="grey">
          <help-circle-outline />
        </n-icon>
      </template>

      {{ abstract }}
      <n-button size="small" quaternary type="primary" @click="showMore"> More </n-button>
    </n-tooltip>
    <div>
      <slot />
    </div>
  </div>
</template>

<script setup>
import { h } from "vue";
import { NAvatar, NButton, useNotification } from "naive-ui";
import drone from "../../../assets/drone.png";
import { HelpCircleOutline } from "@vicons/ionicons5";

const props = defineProps({
  title: String,
  abstract: String,
  content: String,
  meta: String,
});

const notification = useNotification();

const showMore = () => {
  const n = notification.create({
    title: `Help: ${props.title}`,
    description: props.abstract,
    content: props.content.replace(/(\n|\t)/g, " "),
    meta: props.meta,
    avatar: () =>
      h(NAvatar, {
        size: "small",
        round: true,
        src: drone,
      }),
    action: () =>
      h(
        NButton,
        {
          tertiary: true,
          type: "primary",
          onClick: () => {
            n.destroy();
          },
        },
        {
          default: () => "Understood",
        }
      ),
  });
};
</script>

<style scoped>
div.label {
  display: flex;
  flex-direction: row;
  justify-content: center;
  column-gap: 5px;
}
</style>
