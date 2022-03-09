<template>
    <n-form ref="formRef" :model="model" :rules="rules">
        <n-form-item path="name" label="Model Name">
            <n-input
                v-model:value="model.name"
                type="text"
                placeholder="Unique Model Name"
            />
        </n-form-item>
        <n-form-item path="description" label="Model Description">
            <n-input
                v-model:value="model.description"
                type="textarea"
                placeholder="Model description (Metadata)"
            />
        </n-form-item>
        <n-grid cols="3" x-gap="12">
            <n-grid-item span="1">
                <n-form-item path="dimension.x" label="Dimension X">
                    <n-input-number
                        v-model:value="model.dimension.x"
                        :min="10"
                        :max="1000"
                        :step="10"
                    />
                </n-form-item>
            </n-grid-item>
            <n-grid-item span="1">
                <n-form-item path="dimension.y" label="Dimension Y">
                    <n-input-number
                        v-model:value="model.dimension.y"
                        :min="10"
                        :max="1000"
                        :step="10"
                    />
                </n-form-item>
            </n-grid-item>
            <n-grid-item span="1">
                <n-form-item path="dimension.z" label="Dimension Z">
                    <n-input-number
                        v-model:value="model.dimension.z"
                        :min="10"
                        :max="1000"
                        :step="10"
                    />
                </n-form-item>
            </n-grid-item>
        </n-grid>
        <n-form-item path="dimension.t" label="Timesteps">
            <n-slider
                show-tooltip
                v-model:value="model.dimension.t"
                :min="10"
                :max="1000"
                :step="10"
            />
        </n-form-item>
        <n-form-item path="owners" label="Owners">
            <owner ref="ownerRef" />
        </n-form-item>
    </n-form>
    <n-button
        ghost
        v-if="!simulationStore.loaded"
        type="primary"
        @click.stop="simulate"
    >
        Simulate
    </n-button>
    <n-grid cols="2" x-gap="10" v-else>
        <n-grid-item>
            <n-button
                ghost
                block
                icon-placement="right"
                type="primary"
                @click.stop="() => simulationStore.download()"
            >
                Download Simulation
                <template #icon>
                    <n-icon>
                        <cloud-download-outline />
                    </n-icon>
                </template>
            </n-button>
        </n-grid-item>
        <n-grid-item>
            <n-button
                block
                icon-placement="right"
                type="primary"
                @click.stop="() => router.push({ name: 'dashboard' })"
            >
                Go to Simulation
                <template #icon>
                    <n-icon>
                        <arrow-forward-outline />
                    </n-icon>
                </template>
            </n-button>
        </n-grid-item>
    </n-grid>
    <n-alert v-if="errorText" title="Invalid Data" type="error">
        {{ errorText }}
    </n-alert>
</template>

<script setup>
import axios from "axios";

import { ref } from "vue";
import { useMessage, useLoadingBar } from "naive-ui";
import { useRouter } from "vue-router";
import { CloudDownloadOutline, ArrowForwardOutline } from "@vicons/ionicons5";

import Owner from "./Owner.vue";

import { useSimulationStore } from "../../stores/simulation";

const formRef = ref(null);
const ownerRef = ref(null);
const errorText = ref(null);

const message = useMessage();
const loadingBar = useLoadingBar();
const router = useRouter();

const simulationStore = useSimulationStore();

const model = ref({
    name: null,
    description: null,
    dimension: {
        x: 100,
        y: 20,
        z: 100,
        t: 250,
    },
});

const owners = ref([]);

const rules = {
    name: [
        {
            required: true,
            trigger: ["input", "blur"],
        },
    ],
};

const detailedError = (e) => {
    return e.response.data.detail
        .map((d) => `${d.msg}: ${d.loc.join(".")}`)
        .join("\n");
};

const simulate = () => {
    errorText.value = null;
    owners.value = ownerRef.value.owners;
    formRef.value?.validate((errors) => {
        if (!errors) {
            loadingBar.start();
            axios
                .post("http://localhost:8000/simulation", {
                    ...model.value,
                    owners: owners.value,
                })
                .then((res) => {
                    simulationStore.setSimulation(res.data);
                    loadingBar.finish();
                    message.success("Simulation Created!");
                })
                .catch((e) => {
                    loadingBar.error();
                    message.error("Failed creating the Session!");
                    errorText.value = detailedError(e);
                });
        } else {
            errorText.value = "Some Form fields are not Valid";
        }
    });
};
</script>

<style scoped></style>
