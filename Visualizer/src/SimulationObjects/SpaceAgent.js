import Agent from "./Agent";
import Coordinate4D from "./Coordinate4D";

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
  }
}
