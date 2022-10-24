import Coordinate3D from "./Coordinate3D.js";

export default class Blocker {
  /**
   * @param {JSONBlocker} rawBlocker
   */
  constructor(rawBlocker) {
    this.id = rawBlocker.id;
    this.dimension = new Coordinate3D(rawBlocker.dimension.x, rawBlocker.dimension.y, rawBlocker.dimension.z);
    this.blockerType = rawBlocker.blocker_type;
    this.osmId = rawBlocker.osm_id;
  }

  /**
   * @abstract
   */
  positionAtTick() {
    /* abstract method */
  }

  /**
   * @abstract
   * @returns {int[]}
   */
  get ticksInAir() {
    /* abstract method */
    return [];
  }
}
