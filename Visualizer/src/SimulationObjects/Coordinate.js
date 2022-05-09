export default class Coordinate {
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
   * @returns {int[]}
   */
  toArrayCoordinate() {
    return [this.x, this.y, this.z];
  }
}
