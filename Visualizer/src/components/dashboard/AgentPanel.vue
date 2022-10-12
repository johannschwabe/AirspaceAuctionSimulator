<template>
  <div id="agent-drawer-container">
    <n-timeline>
      <n-timeline-item
        v-for="(event, i) in simulation.agentInFocus.events"
        :key="`${simulation.agentInFocus.id}-${i}`"
        v-bind="event"
        @click="setTick(event.tick)"
        style="cursor: pointer"
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
    <simple-data-table title="Path info" :datapoints="pathDatapoints" v-if="pathDatapoints.length > 0" />
    <height-profile
      label="Height profile"
      :color="simulation.agentInFocus.color"
      :data="heightProfileData"
      v-if="heightProfileData"
    />
    <template v-if="allocations">
      <template v-for="(allocation, index) in allocations" :key="`${simulation.agentInFocus.id}-allocation-${index}`">
        <simple-data-table :title="`Allocation ${index + 1}`" :datapoints="allocation.allocationData" />
        <simple-data-table
          :subtitle="`Path for Allocation ${index + 1}`"
          :datapoints="allocation.pathData"
          v-if="allocation.pathData.length > 0"
        />
        <simple-data-table
          v-for="collidingBid in allocation.collidingBids"
          :key="`${simulation.agentInFocus.id}-allocation-${index}-bid-${collidingBid.key}`"
          :subtitle="collidingBid.subtitle"
          :datapoints="collidingBid.datapoints"
        />
        <simple-data-table
          v-for="displayingBid in allocation.displayingBids"
          :key="`${simulation.agentInFocus.id}-allocation-${index}-bid-${displayingBid.key}`"
          :subtitle="displayingBid.subtitle"
          :datapoints="displayingBid.datapoints"
        />
      </template>
    </template>
    <h3 v-if="agentViolations.length > 0">Agent Violations ({{ simulation.agentInFocus.totalViolations }})</h3>
    <template
      v-for="(violation, index) in agentViolations"
      :key="`${simulation.agentInFocus.id}-agent-violation-${index}`"
    >
      <simple-data-table :subtitle="violation.subtitle" :datapoints="violation.datapoints" />
    </template>
    <h3 v-if="blockerViolations.length > 0">
      Blocker Violations ({{ simulation.agentInFocus.totalBlockerViolations }})
    </h3>
    <template
      v-for="(violation, index) in blockerViolations"
      :key="`${simulation.agentInFocus.id}-blocker-violation-${index}`"
    >
      <simple-data-table :subtitle="violation.subtitle" :datapoints="violation.datapoints" />
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted } from "vue";

import {
  FingerPrint,
  Airplane,
  BatteryHalf,
  Speedometer,
  Happy,
  Timer,
  InformationCircle,
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
  Cash,
  ChatboxEllipses,
  GitBranch,
  Skull,
  GitPullRequest,
  BatteryFull,
  Hourglass,
  Pricetag,
  Cube,
  TabletLandscape, ColorPalette
} from "@vicons/ionicons5";
import PerfectScrollbar from "perfect-scrollbar";
import { isArray, isNull, isUndefined } from "lodash-es";

import { useSimulationSingleton } from "@/scripts/simulationSingleton.js";

import SimpleDataTable from "@/components/dashboard/PanelComponents/SimpleDataTable.vue";
import HeightProfile from "@/components/dashboard/PanelComponents/HeightProfile.vue";
import { formatComputeTime } from "@/scripts/format";

let agentScroller;
onMounted(() => {
  const container = document.querySelector("#agent-drawer-container");
  agentScroller = new PerfectScrollbar(container);
});
onUnmounted(() => {
  agentScroller.destroy();
  agentScroller = null;
});

const simulation = useSimulationSingleton();

const setTick = (tick) => {
  simulation.tick = parseInt(tick, 10);
};

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
      label: "Value",
      value: simulation.agentInFocus.value,
      icon: Pricetag,
    },
    {
      label: "Non-Colliding Value",
      value: simulation.agentInFocus.nonCollidingValue,
      icon: Pricetag,
    },
    {
      label: "Utility",
      value: simulation.agentInFocus.utility,
      icon: Happy,
    },
    {
      label: "Non-Colliding Utility",
      value: simulation.agentInFocus.nonCollidingUtility,
      icon: Happy,
    },
    {
      label: "Payment",
      value: simulation.agentInFocus.payment,
      icon: Cash,
    },
    {
      label: "Reallocations",
      value: simulation.agentInFocus.totalReallocations,
      icon: GitBranch,
    },
    {
      label: "Incomplete Allocations",
      value: simulation.agentInFocus.incompleAllocation,
      icon: GitBranch,
    },
    {
      label: "Violations",
      value: simulation.agentInFocus.totalViolations + simulation.agentInFocus.totalBlockerViolations,
      icon: Skull,
    },
    {
      label: "Battery",
      value: simulation.agentInFocus.battery,
      icon: BatteryFull,
    },
    {
      label: "Battery Unused",
      value: simulation.agentInFocus.batteryUnused,
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
      label: "Delayed Starts",
      value: simulation.agentInFocus.delayedStarts,
      icon: Hourglass,
    },
    {
      label: "Delayed Arrivals",
      value: simulation.agentInFocus.delayedArrivals,
      icon: Hourglass,
    },
    {
      label: "Relative Delayed Arrivals",
      value: simulation.agentInFocus.reDelayedArrivals,
      icon: Hourglass,
    },
    {
      label: "Near Field Radius",
      value: simulation.agentInFocus.nearRadius,
      icon: InformationCircle,
    },
    {
      label: "Volume",
      value: simulation.agentInFocus.volume,
      icon: Cube,
    },
    {
      label: "Mean Volume",
      value: simulation.agentInFocus.meanVolume,
      icon: Cube,
    },
    {
      label: "Median Volume",
      value: simulation.agentInFocus.medianVolume,
      icon: Cube,
    },
    {
      label: "Mean Height",
      value: simulation.agentInFocus.meanHeight,
      icon: Podium,
    },
    {
      label: "Median Height",
      value: simulation.agentInFocus.medianHeight,
      icon: Podium,
    },
    {
      label: "Area",
      value: simulation.agentInFocus.area,
      icon: TabletLandscape,
    },
    {
      label: "Mean Area",
      value: simulation.agentInFocus.meanArea,
      icon: TabletLandscape,
    },
    {
      label: "Median Area",
      value: simulation.agentInFocus.medianArea,
      icon: TabletLandscape,
    },
    {
      label: "Mean Time",
      value: simulation.agentInFocus.meanTime,
      icon: Time,
    },
    {
      label: "Median Time",
      value: simulation.agentInFocus.medianTime,
      icon: Time,
    },
    {
      label: "Mean Height above Ground",
      value: simulation.agentInFocus.meanHeightAboveGround,
      icon: TrendingUp,
    },
    {
      label: "Median Height above Ground",
      value: simulation.agentInFocus.medianHeightAboveGround,
      icon: TrendingUp,
    },
  ].filter((d) => !isUndefined(d.value) && !isNull(d.value) && (!isArray(d.value) || d.value.length > 0))
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
    .filter((d) => !isUndefined(d.value) && !isNull(d.value) && (!isArray(d.value) || d.value.length > 0))
    .map((d) => ({ ...d, value: Math.round(d.value * 10) / 10 }));
}

function bidToDatapoints(bid) {
  if (!bid) {
    return [];
  }
  return Object.entries(bid.display).map(([label, value]) => ({
    label: "Bid: " + label.replace(/(^|\s)\S/g, (t) => t.toUpperCase()),
    value,
    icon: Pricetag,
  }));
}

const allocations = computed(() => {
  if (!simulation.agentInFocus.allocationStatistics) {
    return undefined;
  }
  return simulation.agentInFocus.allocationStatistics.map((stat) => ({
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
        label: "Value",
        value: stat.value,
        icon: Pricetag,
      },
      {
        label: "Utility",
        value: stat.utility,
        icon: Happy,
      },
      {
        label: "Payment",
        value: stat.payment,
        icon: Cash,
      },
      ...bidToDatapoints(stat.bid),
      {
        label: "Allocation competitions won",
        value: Object.keys(stat.collidingAgentBids).length,
        icon: GitPullRequest,
      },
      {
        label: "Allocation competitions lost",
        value: Object.keys(stat.displacingAgentBids).length,
        icon: GitPullRequest,
      },
      {
        label: "Compute Time",
        value: () => formatComputeTime(stat.compute_time),
        icon: Timer,
      },
    ],
    pathData: pathToDatapoints(stat.pathStatistics),
    collidingBids: Object.entries(stat.collidingAgentBids).map(([agent_id, bid]) => ({
      subtitle: `Won allocation competition against Agent ${agent_id}`,
      datapoints: bidToDatapoints(bid),
      key: agent_id,
    })),
    displayingBids: Object.entries(stat.displacingAgentBids).map(([agent_id, bid]) => ({
      subtitle: `Lost allocation competition against Agent ${agent_id}`,
      datapoints: bidToDatapoints(bid),
      key: agent_id,
    })),
  }));
});

const agentViolations = computed(() => {
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
        icon: GitPullRequest,
        onClick: () => {
          simulation.focusOnAgent(agent);
        },
      });
      return acc;
    }, []);
});

const blockerViolations = computed(() => {
  return Object.values(simulation.agentInFocus.blockerViolations)
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
      acc[entryIndex].datapoints.push({
        label: `Blocker`,
        value: { x: violation.x, y: violation.y, z: violation.z },
        icon: GitPullRequest,
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

<style scoped>
#agent-drawer-container {
  position: relative;
  height: 950px;
  width: 200px;
  padding-right: 24px;
  overflow: hidden;
}
</style>
