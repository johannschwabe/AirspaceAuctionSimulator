import Path from "./Path";
import Coordinate3D from "./Coordinate3D";

export default class Blocker {
  /**
   *
   * @param {RawBlocker} rawBlocker
   */
  constructor(rawBlocker) {
    this.id = rawBlocker.id;
    this.dimension = new Coordinate3D(...Object.values(rawBlocker.dimension));
    this.path = new Path(rawBlocker.path);
  }

  positionAtTick(tick) {
    return this.path.ticks[tick];
  }
}
