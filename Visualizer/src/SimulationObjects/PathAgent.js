import Path from "./Path";
import Branch from "./Branch";
import {
  pathAllocationEventFactory,
  ArrivalEvent,
  FailedAllocationEvent,
  FlightEvent,
  TakeOffEvent,
} from "./FlightEvent";
import Agent from "./Agent";
import { BRANCH_REASONS } from "@/API/enums";
import PathStatistic from "@/SimulationObjects/PathStatistic";

export default class PathAgent extends Agent {
  /**
   * @param {JSONAgent} rawAgent
   * @param {Owner} owner
   * @param {Simulation} simulation
   * @param {PathAgentStatistics} agentStats
   */
  constructor(rawAgent, owner, simulation, agentStats) {
    super(rawAgent, owner, simulation, agentStats);
    // Agent Info
    this.speed = rawAgent.speed;
    this.nearRadius = rawAgent.near_radius;
    this.battery = rawAgent.battery;

    // Agent Statistics
    this.timeInAir = agentStats.time_in_air;
    this.batteryUnused = agentStats.battery_unused;
    this.delayedStarts = agentStats.delayed_starts;
    this.delayedArrivals = agentStats.delayed_arrivals;
    this.reDelayedArrivals = agentStats.re_delayed_arrivals;

    this.paths = rawAgent.paths.map((path) => new Path(path));
    this.combinedPath = Path.join(this.paths);

    this.intermediate_allocations = rawAgent.intermediate_allocations.map((branch) => {
      const branchStats = agentStats.allocations.find((allocationStats) => allocationStats.tick === branch.tick);
      return new Branch(branch, branchStats);
    });

    this.reAllocationTimesteps = this.intermediate_allocations
      .filter((branch) => branch.reason === BRANCH_REASONS.REALLOCATION)
      .map((branch) => branch.tick);

    this.pathStatistics = agentStats.path ? new PathStatistic(agentStats.path) : null;
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
    this.intermediate_allocations.forEach((branch) => {
      const reallocationLocation = branch.paths > 0 ? branch.paths[0].firstLocation : null;
      const AllocationClass = pathAllocationEventFactory(branch.reason);
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
      this.intermediate_allocations.length > 0 &&
      this.intermediate_allocations[this.intermediate_allocations.length - 1].reason ===
        BRANCH_REASONS.ALLOCATION_FAILED
    ) {
      const lastBranch = this.intermediate_allocations[this.intermediate_allocations.length - 1];
      return events.filter((event) => event.tick < lastBranch.tick || event instanceof FailedAllocationEvent);
    }
    return events;
  }

  /**
   * Set current agent into focus mode
   */
  focus() {
    this._simulation.focusOnAgent(this);
  }

  /**
   * @param {int} tick
   * @returns {Coordinate3D|undefined}
   */
  locationAtTick(tick) {
    if (!this.isActiveAtTick(tick)) {
      return undefined;
    }
    return this.combinedPath.at(tick);
  }

  /**
   * @returns {number[]}
   */
  get flyingTicks() {
    return Object.keys(this.combinedPath.ticks).map((t) => parseInt(t, 10));
  }

  /**
   * @returns {[int, int][]}
   */
  get segmentsStartEnd() {
    return this.paths.map((path) => [path.firstTick, path.lastTick]);
  }

  /**
   * @returns {int|undefined}
   */
  get veryFirstTick() {
    return this.combinedPath.firstTick;
  }

  /**
   * @returns {int|undefined}
   */
  get veryLastTick() {
    return this.combinedPath.lastTick;
  }
}
