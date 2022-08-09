<template>
  <div>
    <h3>Stops:</h3>
    <div style="margin-left: 5px">
      <n-dynamic-input
        :value="owner.locations"
        :on-create="onCreate"
        :on-remove="onRemove"
        :min="owner.minLocations"
        :max="owner.maxLocations"
      >
        <template #default="{ index }">
          <owner-stop :owner="owner" :locationIndex="index" />
        </template>
      </n-dynamic-input>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import OwnerStop from "./OwnerStop.vue";
import { useSimulationConfigStore } from "../../stores/simulationConfig";

const props = defineProps({
  ownerIndex: {
    type: Number,
    required: true,
  },
});

const simulationConfig = useSimulationConfigStore();

const owner = computed(() => simulationConfig.owners[props.ownerIndex]);

const onCreate = (index) => {
  const location = simulationConfig.randomLocation();
  owner.value.locations.splice(index, 0, location);
  return location;
};

const onRemove = (index) => {
  owner.value.locations.splice(index, 1);
};
</script>
