import AgentTypeEnum from "./AgentTypeEnum";
import Path from "./Path";
import Branch from "./Branch";
import {
  ArrivalEvent,
  FlightEvent,
  ReallocationEvent,
  TakeOffEvent,
} from "./FlightEvent";

export default class Agent {
  /**
   *
   * @param {RawAgent} rawAgent
   * @param {Owner} owner
   * @param {Simulation} simulation
   */
  constructor(rawAgent, owner, simulation) {
    this.agentType = AgentTypeEnum.fromString(rawAgent.agent_type);
    this.id = rawAgent.id;
    this.name = rawAgent.name;
    this.speed = rawAgent.speed;
    this.nearRadius = rawAgent.near_radius;
    this.farRadius = rawAgent.far_radius;
    this.welfare = rawAgent.welfare;
    this.battery = rawAgent.battery;
    this.timeInAir = rawAgent.time_in_air;
    this.nonCollidingWelfare = rawAgent.non_colliding_welfare;
    this.nearFieldIntersections = rawAgent.near_field_intersections;
    this.farFieldIntersections = rawAgent.far_field_intersections;
    this.nearFieldViolations = rawAgent.near_field_violations;
    this.farFieldViolations = rawAgent.far_field_violations;
    this.bid = rawAgent.bid;
    this.owner = owner;
    this.color = owner.color;
    this.paths = rawAgent.paths.map((path) => new Path(path));
    this.combinedPath = Path.join(this.paths);
    this.branches = rawAgent.branches.map((branch) => new Branch(branch));
    this._simulation = simulation;
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
      const reallocationLocation = branch.paths[0].firstLocation;
      const reallocationEvent = new ReallocationEvent(
        branch.tick,
        reallocationLocation,
        branch.reason
      );
      events.push(reallocationEvent);
    });
    events.sort(FlightEvent.sortEventsFunction);
    for (let i = 0; i < events.length - 1; i++) {
      if (events[i + 1].takeoff) {
        events[i].lineType = "dashed";
      }
    }
    return events;
  }

  focus() {
    this._simulation.focusOnAgent(this);
  }
}
