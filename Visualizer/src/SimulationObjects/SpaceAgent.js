import Agent from "./Agent";
import Space from "./Space";
import { first, last } from "lodash-es";

export default class SpaceAgent extends Agent {
  /**
   *
   * @param {RawAgent} rawAgent
   * @param {Owner} owner
   * @param {Simulation} simulation
   */
  constructor(rawAgent, owner, simulation) {
    super(rawAgent, owner, simulation);

    /**
     * @type {Space[]}
     */
    this.spaces = rawAgent.spaces.map((space) => new Space(space.min, space.max));

    /**
     * @type {Object<int, Coordinate4D>}
     */
    this.combinedSpace = {};
    this.spaces.forEach((space) => {
      for (let t = space.min.t; t < space.max.t; t++) {
        this.combinedSpace[t] = space;
      }
    });
  }

  get flyingTicks() {
    return Object.keys(this.combinedSpace).map((t) => parseInt(t, 10));
  }

  get segmentsStartEnd() {
    return this.spaces.map((space) => [space.min.t, space.max.t]);
  }

  get veryFirstTick() {
    return first(this.spaces).min.t;
  }

  get veryLastTick() {
    return last(this.spaces).max.t;
  }
}
