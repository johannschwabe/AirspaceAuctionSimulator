import "vfonts/Lato.css";
import "vfonts/FiraCode.css";

import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";

import {
  // create naive ui
  create,
  // component
  NButton,
  NConfigProvider,
  NLoadingBarProvider,
  NMessageProvider,
  NNotificationProvider,
  NDialogProvider,
  NCard,
  NLayout,
  NLayoutHeader,
  NLayoutContent,
  NLayoutFooter,
  NSpace,
  NGrid,
  NGridItem,
  NUpload,
  NUploadDragger,
  NIcon,
  NText,
  NP,
  NInput,
  NInputNumber,
  NForm,
  NFormItem,
  NSlider,
  NDynamicInput,
  NCheckbox,
  NColorPicker,
  NSelect,
  NAlert,
  NProgress,
  NPageHeader,
  NStatistic,
  NBreadcrumb,
  NBreadcrumbItem,
  NAvatar,
  NDropdown,
  NNumberAnimation,
  NDrawer,
  NDrawerContent,
  NDivider,
  NTree,
  NTimeline,
  NTimelineItem,
} from "naive-ui";

const naive = create({
  components: [
    NButton,
    NConfigProvider,
    NLoadingBarProvider,
    NMessageProvider,
    NNotificationProvider,
    NDialogProvider,
    NCard,
    NLayout,
    NLayoutHeader,
    NLayoutContent,
    NLayoutFooter,
    NSpace,
    NGrid,
    NGridItem,
    NUpload,
    NUploadDragger,
    NIcon,
    NText,
    NP,
    NInput,
    NInputNumber,
    NForm,
    NFormItem,
    NSlider,
    NDynamicInput,
    NCheckbox,
    NColorPicker,
    NSelect,
    NAlert,
    NProgress,
    NPageHeader,
    NStatistic,
    NBreadcrumb,
    NBreadcrumbItem,
    NAvatar,
    NDropdown,
    NNumberAnimation,
    NDrawer,
    NDrawerContent,
    NDivider,
    NTree,
    NTimeline,
    NTimelineItem,
  ],
});

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(naive);

app.mount("#app");
