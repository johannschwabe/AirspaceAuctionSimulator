import Path from "./Path";
import Coordinate3D from "./Coordinate3D";

export default class Blocker {
  /**
   *
   * @param {RawBlocker} rawBlocker
   */
  constructor(rawBlocker) {
    this.id = rawBlocker.id;
    this.dimension = new Coordinate3D(rawBlocker.dimension.x, rawBlocker.dimension.y, rawBlocker.dimension.z);
    this.type = rawBlocker.type;
    if (this.type === "dynamic") {
      this.path = new Path(rawBlocker.path);
    } else if (this.type === "static") {
      this.location = new Coordinate3D(rawBlocker.location.x, rawBlocker.location.y, rawBlocker.location.z);
    } else {
      throw new Error("Invalid blocker type!");
    }
  }

  positionAtTick(tick) {
    if (this.type === "dynamic") {
      return this.path.ticks[tick];
    } else if (this.type === "static") {
      return this.location;
    } else {
      throw new Error("Invalid blocker type!");
    }
  }
}
