import Agent from "./Agent";
import Coordinate4D from "./Coordinate4D";
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
    this.spaces = rawAgent.spaces.map((space) => ({
      min: new Coordinate4D(space.min.x, space.min.y, space.min.z, space.min.t),
      max: new Coordinate4D(space.max.x, space.max.y, space.max.z, space.max.t),
    }));
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
    return Object.keys(this.combinedSpace);
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
