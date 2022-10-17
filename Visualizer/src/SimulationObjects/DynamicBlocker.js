import Path from "./Path";
import Blocker from "./Blocker";

export default class DynamicBlocker extends Blocker {
  /**
   * @param {JSONBlocker} rawBlocker
   */
  constructor(rawBlocker) {
    super(rawBlocker);
    const convLocations = {};
    rawBlocker.locations.forEach((loc) => {
      convLocations[loc.t] = [loc.x, loc.y, loc.z];
    });
    this.path = new Path({ positions: convLocations });
  }

  /**
   * @param {int} tick
   * @returns {Coordinate3D}
   */
  positionAtTick(tick) {
    return this.path.ticks[tick];
  }

  /**
   * @returns {int[]}
   */
  get ticksInAir() {
    return this.path.ticksInAir;
  }
}
