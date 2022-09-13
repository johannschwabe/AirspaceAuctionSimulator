import Path from "./Path";
import Branch from "./Branch";
import {
  allocationEventFactory,
  ArrivalEvent,
  FailedAllocationEvent,
  FlightEvent,
  ReallocationEvent,
  TakeOffEvent,
} from "./FlightEvent";
import Agent from "./Agent";
import { BRANCH_REASONS } from "@/API/enums";

export default class PathAgent extends Agent {
  /**
   *
   * @param {JSONAgent} rawAgent
   * @param {Owner} owner
   * @param {Simulation} simulation
   * @param {AgentStatistics} agentStats
   */
  constructor(rawAgent, owner, simulation, agentStats) {
    super(rawAgent, owner, simulation, agentStats);
    this.speed = rawAgent.speed;
    this.nearRadius = rawAgent.near_radius;
    this.battery = rawAgent.battery;
    this.timeInAir = agentStats.time_in_air;
    this.paths = rawAgent.paths.map((path) => new Path(path));
    this.combinedPath = Path.join(this.paths);
    this.branches = rawAgent.branches.map((branch) => {
      const branchStats = agentStats.allocations.find((allocationStats) => allocationStats.tick === branch.tick);
      return new Branch(branch, branchStats);
    });
    this.reAllocationTimesteps = this.branches
      .filter((branch) => branch.reason === BRANCH_REASONS.REALLOCATION)
      .map((branch) => branch.tick);
  }

  /**
   * Returns a list of all relevant events for the given agent over his lifetime
   * @returns {FlightEvent[]}
   */
  get events() {
    const events = [];
    this.paths.forEach((path) => {
      const takeOffEvent = new TakeOffEvent(path.firstTick, path.firstLocation);
      events.push(takeOffEvent);

      const arrivalEvent = new ArrivalEvent(path.lastTick, path.lastLocation);
      events.push(arrivalEvent);
    });
    this.branches.forEach((branch) => {
      const reallocationLocation = branch.paths > 0 ? branch.paths[0].firstLocation : null;
      const AllocationClass = allocationEventFactory(branch.reason);
      const reallocationEvent = new AllocationClass(branch.tick, reallocationLocation, branch.explanation);
      events.push(reallocationEvent);
    });
    events.sort(FlightEvent.sortEventsFunction);
    let isFlying = false;
    events.forEach((event) => {
      if (event instanceof TakeOffEvent) {
        isFlying = true;
      }
      if (event instanceof ArrivalEvent) {
        isFlying = false;
      }
      if (!isFlying) {
        event.lineType = "dashed";
      }
    });
    if (
      this.branches.length > 0 &&
      this.branches[this.branches.length - 1].reason === BRANCH_REASONS.ALLOCATION_FAILED
    ) {
      const lastBranch = this.branches[this.branches.length - 1];
      return events.filter((event) => event.tick < lastBranch.tick || event instanceof FailedAllocationEvent);
    }
    return events;
  }

  focus() {
    this._simulation.focusOnAgent(this);
  }

  locationAtTick(tick) {
    if (!this.isActiveAtTick(tick)) {
      return undefined;
    }
    return this.combinedPath.at(tick);
  }

  get flyingTicks() {
    return Object.keys(this.combinedPath.ticks).map((t) => parseInt(t, 10));
  }

  get segmentsStartEnd() {
    return this.paths.map((path) => [path.firstTick, path.lastTick]);
  }

  get veryFirstTick() {
    return this.combinedPath.firstTick;
  }

  get veryLastTick() {
    return this.combinedPath.lastTick;
  }
}
