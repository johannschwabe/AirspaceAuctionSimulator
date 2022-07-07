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
    this.spaces = rawAgent.spaces.map((space) => new Coordinate4D(space.x, space.y, space.z, space.t));
  }
}
