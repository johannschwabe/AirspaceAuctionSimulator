import Path from "./Path";
import Coordinate from "./Coordinate";

export default class Blocker {
  /**
   *
   * @param {RawBlocker} rawBlocker
   */
  constructor(rawBlocker) {
    this.id = rawBlocker.id;
    this.dimension = new Coordinate(...Object.values(rawBlocker.dimension));
    this.path = new Path(rawBlocker.path);
  }

  positionAtTick(tick) {
    return this.path.ticks[tick];
  }
}
