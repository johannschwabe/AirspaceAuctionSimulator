import Coordinate3D from "./Coordinate3D.js";

export default class Blocker {
  /**
   *
   * @param {RawBlocker} rawBlocker
   */
  constructor(rawBlocker) {
    this.id = rawBlocker.id;
    this.dimension = new Coordinate3D(rawBlocker.dimension.x, rawBlocker.dimension.y, rawBlocker.dimension.z);
    this.blocker_type = rawBlocker.blocker_type;
    this.osm_id = rawBlocker.osm_id;
  }

  positionAtTick() {
    /* abstract method */
  }

  get ticksInAir() {
    /* abstract method */
    return [];
  }
}
