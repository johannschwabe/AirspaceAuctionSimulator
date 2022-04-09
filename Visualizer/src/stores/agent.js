import { defineStore } from "pinia";
import { useStorage } from "@vueuse/core";
import {
  mdiAirplaneLanding,
  mdiAirplaneTakeoff,
  mdiSourceBranch,
} from "@mdi/js";
import { useSimulationStore } from "./simulation";
import { useOwnerStore } from "./owner";

const simulationStore = useSimulationStore();
const ownerStore = useOwnerStore();

export const useAgentStore = defineStore({
  id: "agent",
  state: () => ({
    selected: false,
    id: useStorage("agent-id", -1),
    owner_id: useStorage("agent-owner-id", "unknown"),
    name: useStorage("agent-name", "unknown"),
    owner_name: useStorage("agent-owner-name", "unknown"),
    agent_type: useStorage("agent-type", "unknown"),
    battery: useStorage("agent-battery", -1),
    bid: useStorage("agent-bid", -1),
    near_field_intersections: useStorage("agent-near-field-intersections", -1),
    near_field_violations: useStorage("agent-near-field-violations", -1),
    near_radius: useStorage("agent-near-radius", -1),
    far_field_intersections: useStorage("agent-far-field-intersections", -1),
    far_field_violations: useStorage("agent-far-field-violations", -1),
    far_radius: useStorage("agent-far-radius", -1),
    speed: useStorage("agent-speed", -1),
    time_in_air: useStorage("agent-time-in-air", -1),
    welfare: useStorage("agent-welfare", -1),
    branches: useStorage("agent-branches", []),
    paths: useStorage("agent-paths", []),
  }),
  getters: {
    owner(state) {
      return simulationStore.owners.find(
        (owner) => owner.id === state.owner_id
      );
    },
    events(state) {
      const events = [];
      state.paths.forEach((path) => {
        events.push({
          title: "Take off",
          type: "default",
          takeoff: true,
          icon: mdiAirplaneTakeoff,
          time: `Tick: ${path.t[0]}`,
          tick: path.t[0],
          location: { x: path.x[0], y: path.y[0], z: path.z[0] },
        });
        const i = path.t.length - 1;
        events.push({
          title: "Arrival",
          type: "success",
          icon: mdiAirplaneLanding,
          time: `Tick: ${path.t[i]}`,
          tick: path.t[i],
          location: { x: path.x[i], y: path.y[i], z: path.z[i] },
        });
      });
      state.branches.forEach((branch) => {
        events.push({
          title: "Reallocation",
          icon: mdiSourceBranch,
          content: branch.reason.reason,
          type: "warning",
          time: `Tick: ${branch.tick}`,
          tick: branch.tick,
        });
      });
      events.sort((e1, e2) => {
        if (e1.tick === e2.tick) {
          return e1.takeoff ? 1 : -1;
        }
        return e1.tick > e2.tick ? 1 : -1;
      });
      for (let i = 0; i < events.length - 1; i++) {
        if (events[i + 1].takeoff) {
          events[i].lineType = "dashed";
        }
      }
      return events;
    },
  },
  actions: {
    select(agent) {
      this.selected = true;
      this.id = agent.id;
      this.owner_id = agent.owner_id;
      this.name = agent.name;
      this.owner_name = agent.owner_name;
      this.agent_type = agent.agent_type;
      this.battery = agent.battery;
      this.bid = agent.bid;
      this.near_field_intersections = agent.near_field_intersections;
      this.near_field_violations = agent.near_field_violations;
      this.near_radius = agent.near_radius;
      this.far_field_intersections = agent.far_field_intersections;
      this.far_field_violations = agent.far_field_violations;
      this.far_radius = agent.far_radius;
      this.speed = agent.speed;
      this.time_in_air = agent.time_in_air;
      this.welfare = agent.welfare;
      this.branches = agent.branches;
      this.paths = agent.paths;
      ownerStore.select(this.owner);
    },
    deselect() {
      this.selected = false;
    },
  },
});
