import Coordinate3D from "./Coordinate3D";
import Blocker from "./Blocker";

export default class StaticBlocker extends Blocker {
  /**
   *
   * @param {RawBlocker} rawBlocker
   */
  constructor(rawBlocker) {
    super(rawBlocker);
    this.location = new Coordinate3D(rawBlocker.location.x, rawBlocker.location.y, rawBlocker.location.z);
  }

  positionAtTick() {
    return this.location;
  }
}
