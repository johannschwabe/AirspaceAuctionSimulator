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

  get segmentsStartEnd() {
    return this.spaces.map((space) => [space.min.t, space.max.t]);
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
