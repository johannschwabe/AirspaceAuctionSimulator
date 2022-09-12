<template>
  <n-timeline>
    <n-timeline-item
      v-for="(event, i) in simulation.agentInFocus.events"
      :key="`${simulation.agentInFocus.id}-${i}`"
      v-bind="event"
    >
      <template #icon>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
          <path :d="event.icon" :fill="fillColor(event)" />
        </svg>
      </template>
    </n-timeline-item>
  </n-timeline>

  <n-divider style="margin-bottom: 6px" />
  <simple-data-table title="General Info" :datapoints="datapoints" />
  <simple-data-table title="Path info" :datapoints="pathDatapoints" />
  <height-profile
    label="Height profile"
    :color="simulation.agentInFocus.color"
    :data="heightProfileData"
    v-if="heightProfileData"
  />
  <template v-for="(allocation, index) in allocations" :key="`${simulation.agentInFocus.id}-allocation-${index}`">
    <simple-data-table :title="`Allocation ${index + 1}`" :datapoints="allocation.allocationData" />
    <simple-data-table
      :subtitle="`Path for Allocation ${index + 1}`"
      :datapoints="allocation.pathData"
      v-if="allocation.pathData.length > 0"
    />
  </template>
  <h3 v-if="violationData.length > 0">Airspace Violations</h3>
  <template v-for="(violation, index) in violationData" :key="`${simulation.agentInFocus.id}-violation-${index}`">
    <simple-data-table :subtitle="violation.subtitle" :datapoints="violation.datapoints" />
  </template>
</template>

<script setup>
import { computed } from "vue";
import {
  FingerPrint,
  Airplane,
  BatteryHalf,
  Speedometer,
  Happy,
  Timer,
  InformationCircle,
  TrophyOutline,
  Remove,
  ReorderTwo,
  Resize,
  Stopwatch,
  Podium,
  SwapVertical,
  ArrowUp,
  ArrowDown,
  TrendingUp,
  TrendingDown,
  Telescope,
  Compass,
  Time,
  ChatboxEllipses,
  GitBranch,
  Skull,
} from "@vicons/ionicons5";
import { format, set } from "date-fns";

import { useSimulationSingleton } from "@/scripts/simulation.js";
import SimpleDataTable from "@/components/dashboard/SimpleDataTable.vue";
import HeightProfile from "@/components/dashboard/HeightProfile.vue";

const simulation = useSimulationSingleton();
const datapoints = computed(() =>
  [
    {
      label: "Agent ID",
      value: simulation.agentInFocus.id,
      icon: FingerPrint,
    },
    {
      label: "Type",
      value: simulation.agentInFocus.agentType,
      icon: Airplane,
    },
    {
      label: "In Air",
      value: simulation.agentInFocus.isActiveAtTick(simulation.tick) ? "Yes" : "No",
      icon: Compass,
    },
    simulation.agentInFocus.isActiveAtTick(simulation.tick) && {
      label: "Current Location",
      value: simulation.agentInFocus.locationAtTick(simulation.tick),
      icon: Telescope,
    },
    {
      label: "First Tick",
      value: simulation.agentInFocus.veryFirstTick,
      icon: TrendingUp,
    },
    {
      label: "Last Tick",
      value: simulation.agentInFocus.veryLastTick,
      icon: TrendingDown,
    },
    {
      label: "Utility",
      value: simulation.agentInFocus.utility,
      icon: Happy,
    },
    {
      label: "Non-Colliding Utility",
      value: simulation.agentInFocus.nonCollidingUtility,
      icon: TrophyOutline,
    },
    {
      label: "Reallocations",
      value: simulation.agentInFocus.totalReallocations,
      icon: GitBranch,
    },
    {
      label: "Violations",
      value: simulation.agentInFocus.totalViolations,
      icon: Skull,
    },
    {
      label: "Battery",
      value: simulation.agentInFocus.battery,
      icon: BatteryHalf,
    },
    {
      label: "Speed",
      value: simulation.agentInFocus.speed,
      icon: Speedometer,
    },
    {
      label: "Time in Air",
      value: simulation.agentInFocus.timeInAir,
      icon: Timer,
    },
    {
      label: "Near Field Radius",
      value: simulation.agentInFocus.nearRadius,
      icon: InformationCircle,
    },
  ].filter((d) => d.value)
);

const pathDatapoints = computed(() => {
  return pathToDatapoints(simulation.agentInFocus.pathStatistics);
});

const heightProfileData = computed(() => {
  return simulation.agentInFocus.pathStatistics?.heightProfile;
});

function pathToDatapoints(path) {
  if (!path) {
    return [];
  }
  return [
    {
      label: "Distance Traveled",
      value: path.distanceTraveled,
      icon: Resize,
    },
    {
      label: "L1 Distance",
      value: path.distanceL1,
      icon: Remove,
    },
    {
      label: "L2 Distance",
      value: path.distanceL2,
      icon: ReorderTwo,
    },
    {
      label: "Ground Distance Traveled",
      value: path.groundDistanceTraveled,
      icon: Resize,
    },
    {
      label: "L1 Ground Distance",
      value: path.groundDistanceL1,
      icon: Remove,
    },
    {
      label: "L2 Ground Distance",
      value: path.groundDistanceL2,
      icon: ReorderTwo,
    },
    {
      label: "Time difference",
      value: path.timeDifference,
      icon: Stopwatch,
    },
    {
      label: "Mean height",
      value: path.meanHeight,
      icon: Podium,
    },
    {
      label: "Median height",
      value: path.medianHeight,
      icon: Podium,
    },
    {
      label: "Height difference",
      value: path.heightDifference,
      icon: SwapVertical,
    },
    {
      label: "Ascent",
      value: path.ascent,
      icon: ArrowUp,
    },
    {
      label: "Descent",
      value: path.descent,
      icon: ArrowDown,
    },
  ]
    .filter((d) => d.value)
    .map((d) => ({ ...d, value: Math.round(d.value * 10) / 10 }));
}

const allocations = computed(() =>
  simulation.agentInFocus.allocationStatistics.map((stat) => ({
    allocationData: [
      {
        label: "tick",
        value: stat.tick,
        icon: Time,
      },
      {
        label: "Reason",
        value: stat.reason,
        icon: ChatboxEllipses,
      },
      {
        label: "Utility",
        value: stat.utility,
        icon: Happy,
      },
      {
        label: "Collisions",
        value: stat.collidingAgentIds.length,
        icon: Skull,
      },
      {
        label: "Compute Time",
        value: () => {
          const milliseconds = stat.compute_time / 1000;
          const date = set(new Date(), {
            year: 0,
            month: 0,
            date: 0,
            hours: 0,
            minutes: 0,
            seconds: 0,
            milliseconds,
          });
          if (stat.compute_time < 1000) {
            return `${stat.compute_time} ns`;
          }
          if (milliseconds < 1000) {
            return `${milliseconds} ms`;
          }
          if (milliseconds < 60 * 1000) {
            return `${format(date, "ss")}s`;
          }
          if (milliseconds < 60 * 60 * 1000) {
            return `${format(date, "mm")}min ${format(date, "ss")}s`;
          }
          return `${format(date, "HH")}h ${format(date, "mm")}min ${format(date, "ss")}s`;
        },
        icon: Timer,
      },
    ],
    pathData: pathToDatapoints(stat.pathStatistics),
  }))
);

const violationData = computed(() => {
  return Object.entries(simulation.agentInFocus.violations)
    .map(([agent_id, locations]) => {
      return locations.map((loc) => ({
        ...loc,
        agent: agent_id,
      }));
    })
    .flat()
    .reduce((acc, violation) => {
      const subtitle = `Tick ${violation.t}`;
      let entryIndex = acc.findIndex((v) => v.subtitle === subtitle);
      if (entryIndex === -1) {
        acc.push({
          subtitle,
          datapoints: [],
        });
        entryIndex = acc.length - 1;
      }
      const agent = simulation.agents.find((a) => a.id === violation.agent);
      acc[entryIndex].datapoints.push({
        label: `${agent.owner.name} > ${agent.id}`,
        value: { x: violation.x, y: violation.y, z: violation.z },
        icon: Skull,
        onClick: () => {
          simulation.focusOnAgent(agent);
        },
      });
      return acc;
    }, []);
});

const fillColor = (event) => {
  return {
    default: "#a8a8a8",
    success: "#048a00",
    info: "#00408a",
    warning: "#cb7500",
    error: "#b90000",
  }[event.type];
};
</script>

<style scoped></style>
