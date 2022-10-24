export default class Coordinate3D {
  /**
   * @param {int} x
   * @param {int} y
   * @param {int} z
   */
  constructor(x, y, z) {
    this.x = x;
    this.y = y;
    this.z = z;
  }

  /**
   * @returns {[int, int, int]}
   */
  toArrayCoordinate() {
    return [this.x, this.y, this.z];
  }

  /**
   * @returns {number}
   */
  get xyz() {
    return parseInt(`${this.x}${this.y}${this.z}`, 10);
  }
}
