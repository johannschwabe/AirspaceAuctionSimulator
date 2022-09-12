import Path from "./Path";
import Branch from "./Branch";
import { ArrivalEvent, FlightEvent, ReallocationEvent, TakeOffEvent } from "./FlightEvent";
import Agent from "./Agent";

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
      .filter((branch) => branch.reason === "REALLOCATION")
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
      const reallocationEvent = new ReallocationEvent(branch.tick, reallocationLocation, branch.reason);
      events.push(reallocationEvent);
    });
    events.sort(FlightEvent.sortEventsFunction);
    for (let i = 0; i < events.length - 1; i++) {
      if (events[i + 1] instanceof TakeOffEvent) {
        events[i].lineType = "dashed";
      }
    }
    // const failedIndex = events.findIndex((e) => e.content === "ALLOCATION_FAILED");
    // if (failedIndex > -1) {
    //   return events.slice(0, failedIndex + 1);
    // }
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
