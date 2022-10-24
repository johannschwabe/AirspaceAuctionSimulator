export default class Space {
  /**
   * @param {JSONSpace} rawSpace
   */
  constructor(rawSpace) {
    this.min = rawSpace.min;
    this.max = rawSpace.max;
  }

  /**
   * @param {int} tick
   * @returns {boolean}
   */
  isActiveAtTick(tick) {
    return this.min.t <= tick && tick <= this.max.t;
  }

  /**
   * @returns {number}
   */
  get dimensionX() {
    return this.max.x - this.min.x;
  }

  /**
   * @returns {number}
   */
  get dimensionY() {
    return this.max.y - this.min.y;
  }

  /**
   * @returns {number}
   */
  get dimensionZ() {
    return this.max.z - this.min.z;
  }

  /**
   * @returns {int}
   */
  get dimensionT() {
    return this.max.t - this.min.t;
  }

  /**
   * @returns {{t: int, x: number, y: number, z: number}}
   */
  get dimensions() {
    return {
      x: this.dimensionX,
      y: this.dimensionY,
      z: this.dimensionZ,
      t: this.dimensionT,
    };
  }

  /**
   * @returns {number}
   */
  get originX() {
    return this.min.x + 0.5 * this.dimensionX;
  }

  /**
   * @returns {number}
   */
  get originY() {
    return this.min.y + 0.5 * this.dimensionY;
  }

  /**
   * @returns {number}
   */
  get originZ() {
    return this.min.z + 0.5 * this.dimensionZ;
  }

  /**
   * @returns {{x: number, y: number, z: number}}
   */
  get origin() {
    return {
      x: this.originX,
      y: this.originY,
      z: this.originZ,
    };
  }
}
