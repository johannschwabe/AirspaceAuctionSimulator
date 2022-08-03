import Path from "./Path";
import Blocker from "./Blocker";

export default class DynamicBlocker extends Blocker {
  /**
   *
   * @param {RawBlocker} rawBlocker
   */
  constructor(rawBlocker) {
    super(rawBlocker);
    this.path = new Path(rawBlocker.path);
  }

  positionAtTick(tick) {
    return this.path.ticks[tick];
  }

  get ticksInAir() {
    return this.path.ticksInAir;
  }
}
