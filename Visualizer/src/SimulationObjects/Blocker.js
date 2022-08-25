import Coordinate3D from "./Coordinate3D";

export default class Blocker {
  /**
   *
   * @param {RawBlocker} rawBlocker
   */
  constructor(rawBlocker) {
    this.id = rawBlocker.id;
    this.dimension = new Coordinate3D(rawBlocker.dimension.x, rawBlocker.dimension.y, rawBlocker.dimension.z);
    this.blocker_type = rawBlocker.blocker_type;
  }

  positionAtTick() {
    /* abstract method */
  }

  get ticksInAir() {
    /* abstract method */
    return [];
  }
}
