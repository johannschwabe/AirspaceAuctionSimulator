import Agent from "./Agent";
import Space from "./Space";
import { first, last } from "lodash-es";
import { FlightEvent, ReservationEndEvent, ReservationStartEvent } from "@/SimulationObjects/FlightEvent";
import Blocks from "./Blocks";
import { BRANCH_REASONS } from "../API/enums";
import SpaceStatistic from "./SpaceStatistic";
import { spaceAllocationEventFactory } from "./FlightEvent";

export default class SpaceAgent extends Agent {
  /**
   *
   * @param {JSONAgent} rawAgent
   * @param {Owner} owner
   * @param {Simulation} simulation
   * @param {SpaceAgentStatistics} agentStats
   */
  constructor(rawAgent, owner, simulation, agentStats) {
    super(rawAgent, owner, simulation, agentStats);
    // Agent Statistics
    this.volume = agentStats.space?.volume;
    this.meanVolume = agentStats.space?.mean_volume;
    this.medianVolume = agentStats.space?.median_volume;
    this.meanHeight = agentStats.space?.mean_height;
    this.medianHeight = agentStats.space?.median_height;
    this.area = agentStats.space?.area;
    this.meanArea = agentStats.space?.mean_area;
    this.medianArea = agentStats.space?.median_area;
    this.meanTime = agentStats.space?.mean_time;
    this.medianTime = agentStats.space?.median_time;
    this.meanHeightAboveGround = agentStats.space?.mean_height_above_ground;
    this.medianHeightAboveGround = agentStats.space?.median_height_above_ground;

    /**
     * @type {Space[]}
     */
    this.spaces = rawAgent.blocks.map((space) => new Space(space));

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

    this.intermediate_allocations = rawAgent.intermediate_allocations.map((block) => {
      const blockStats = agentStats.allocations.find((allocationStats) => allocationStats.tick === block.tick);
      return new Blocks(block, blockStats);
    });

    this.reAllocationTimesteps = this.intermediate_allocations
      .filter((blocks) => blocks.reason === BRANCH_REASONS.REALLOCATION)
      .map((blocks) => blocks.tick);

    this.pathStatistics = agentStats.space ? new SpaceStatistic(agentStats.space) : null;
  }

  /**
   * @returns {FlightEvent[]}
   */
  get events() {
    const events = [];
    const starts = this.spaces.reduce((acc, curr) => {
      acc[curr.min.t] = acc[curr.min.t] ? acc[curr.min.t] + 1 : 1;
      return acc;
    }, {});

    const ends = this.spaces.reduce((acc, curr) => {
      acc[curr.max.t] = acc[curr.max.t] ? acc[curr.max.t] + 1 : 1;
      return acc;
    }, {});
    Object.entries(starts).forEach(([timestep, count]) => {
      const takeOffEvent = new ReservationStartEvent(parseInt(timestep), count);
      events.push(takeOffEvent);
    });
    Object.entries(ends).forEach(([timestep, count]) => {
      const arrivalEvent = new ReservationEndEvent(parseInt(timestep), count);
      events.push(arrivalEvent);
    });
    this.intermediate_allocations.forEach((blocks) => {
      const AllocationClass = spaceAllocationEventFactory(blocks.reason);
      const reallocationEvent = new AllocationClass(blocks.tick);
      events.push(reallocationEvent);
    });
    events.sort(FlightEvent.sortEventsFunction);
    for (let i = 0; i < events.length - 1; i++) {
      if (events[i + 1] instanceof ReservationEndEvent) {
        events[i].lineType = "dashed";
      }
    }
    return events;
  }

  /**
   * @returns {int[]}
   */
  get flyingTicks() {
    return Object.keys(this.combinedSpace).map((t) => parseInt(t, 10));
  }

  /**
   * @param {int} tick
   * @returns {Coordinate3D|undefined}
   */
  locationAtTick(tick) {
    if (!this.isActiveAtTick(tick)) {
      return undefined;
    }
    return this.combinedSpace[tick][0].origin;
  }

  /**
   * @returns {[int,int][]}
   */
  get segmentsStartEnd() {
    return this.spaces.map((space) => [space.min.t, space.max.t]).sort((a, b) => a[0] - b[0]);
  }

  /**
   * @returns {int|null}
   */
  get veryFirstTick() {
    const tick = first(this.spaces);
    return tick !== undefined ? tick.min.t : null;
  }

  /**
   * @returns {int|null}
   */
  get veryLastTick() {
    const tick = last(this.spaces);
    return tick !== undefined ? tick.max.t : null;
  }
}
