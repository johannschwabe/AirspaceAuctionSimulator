import Coordinate3D from "./Coordinate3D";
import Blocker from "./Blocker";

export default class StaticBlocker extends Blocker {
  /**
   *
   * @param {RawBlocker} rawBlocker
   * @param {number} maxTick
   */
  constructor(rawBlocker, maxTick) {
    super(rawBlocker);
    this.maxTick = maxTick;
    this.location = new Coordinate3D(rawBlocker.location.x, rawBlocker.location.y, rawBlocker.location.z);
  }

  positionAtTick() {
    return this.location;
  }

  get ticksInAir() {
    return [...Array(this.maxTick).keys()];
  }
}
