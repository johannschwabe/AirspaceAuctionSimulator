import Coordinate4D from "@/SimulationObjects/Coordinate4D";

export default class Space {
  /**
   * @param {{x: number, y: number, z: number, t: number}} min
   * @param {{x: number, y: number, z: number, t: number}} max
   */
  constructor(min, max) {
    this.min = new Coordinate4D(min.x, min.y, min.z, min.t);
    this.max = new Coordinate4D(max.x, max.y, max.z, max.t);
  }

  isActiveAtTick(tick) {
    return this.min.t <= tick && tick <= this.max.t;
  }

  get dimensionX() {
    return this.max.x - this.min.x;
  }

  get dimensionY() {
    return this.max.y - this.min.y;
  }

  get dimensionZ() {
    return this.max.z - this.min.z;
  }

  get dimensionT() {
    return this.max.t - this.min.t;
  }

  get dimensions() {
    return {
      x: this.dimensionX,
      y: this.dimensionY,
      z: this.dimensionZ,
      t: this.dimensionT,
    };
  }

  get originX() {
    return this.min.x + 0.5 * this.dimensionX;
  }

  get originY() {
    return this.min.y + 0.5 * this.dimensionY;
  }

  get originZ() {
    return this.min.z + 0.5 * this.dimensionZ;
  }

  get origin() {
    return {
      x: this.originX,
      y: this.originY,
      z: this.originZ,
    };
  }
}
