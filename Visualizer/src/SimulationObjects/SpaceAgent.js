import Agent from "./Agent";
import Space from "./Space";
import { first, last } from "lodash-es";
import { FlightEvent, ReservationEndEvent, ReservationStartEvent } from "@/SimulationObjects/FlightEvent";

export default class SpaceAgent extends Agent {
  /**
   *
   * @param {JSONAgent} rawAgent
   * @param {Owner} owner
   * @param {Simulation} simulation
   * @param {AgentStatistics} agentStats
   */
  constructor(rawAgent, owner, simulation, agentStats) {
    super(rawAgent, owner, simulation, agentStats);

    this.volume = agentStats.space.volume;
    this.meanVolume = agentStats.space.mean_volume;
    this.medianVolume = agentStats.space.median_volume;
    this.meanHeight = agentStats.space.mean_height;
    this.medianHeight = agentStats.space.median_height;
    this.area = agentStats.space.area;
    this.meanArea = agentStats.space.mean_area;
    this.medianArea = agentStats.space.median_area;
    this.meanTime = agentStats.space.mean_time;
    this.medianTime = agentStats.space.median_time;
    this.meanHeightAboveGround = agentStats.space.mean_height_above_ground;
    this.medianHeightAboveGround = agentStats.space.median_height_above_ground;

    /**
     * @type {Space[]}
     */
    this.spaces = rawAgent.spaces.map((space) => new Space(space));

    /**
     * @type {Object<int, Coordinate4D>}
     */
    this.combinedSpace = {};
    this.spaces.forEach((space) => {
      for (let t = space.min.t; t <= space.max.t; t++) {
        if (this.combinedSpace[t] === undefined) {
          this.combinedSpace[t] = [space];
        } else {
          this.combinedSpace[t].push(space);
        }
      }
    });
  }

  get events() {
    const events = [];
    this.spaces.forEach((space) => {
      const takeOffEvent = new ReservationStartEvent(space.min.t);
      events.push(takeOffEvent);

      const arrivalEvent = new ReservationEndEvent(space.max.t);
      events.push(arrivalEvent);
    });
    events.sort(FlightEvent.sortEventsFunction);
    for (let i = 0; i < events.length - 1; i++) {
      if (events[i + 1] instanceof ReservationEndEvent) {
        events[i].lineType = "dashed";
      }
    }
    return events;
  }

  get flyingTicks() {
    return Object.keys(this.combinedSpace).map((t) => parseInt(t, 10));
  }

  locationAtTick(tick) {
    if (!this.isActiveAtTick(tick)) {
      return undefined;
    }
    return this.combinedSpace[tick].origin;
  }

  get segmentsStartEnd() {
    return this.spaces.map((space) => [space.min.t, space.max.t]).sort((a, b) => a[0] - b[0]);
  }

  get veryFirstTick() {
    const tick = first(this.spaces);
    return tick !== undefined ? tick.min.t : null;
  }

  get veryLastTick() {
    const tick = last(this.spaces);
    return tick !== undefined ? tick.max.t : null;
  }
}
