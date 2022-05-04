import Coordinate from "./Coordinate";
import { first, last } from "lodash-es";

export default class Path {
  /**
   * @param {RawPath} rawPath
   */
  constructor(rawPath) {
    /**
     * @type {Object<int, Coordinate>}
     */
    this.ticks = {};
    Object.entries(rawPath.t).forEach(([t, loc]) => {
      const [x, y, z] = loc;
      this.ticks[t] = new Coordinate(x, y, z);
    });
  }

  get ticksInAir() {
    return Object.keys(this.ticks);
  }

  get firstTick() {
    return parseInt(first(this.ticksInAir), 10);
  }

  get lastTick() {
    return parseInt(last(this.ticksInAir), 10);
  }

  get firstLocation() {
    return this.ticks[this.firstTick];
  }

  get lastLocation() {
    return this.ticks[this.lastTick];
  }

  /**
   * Joins multiple paths together to one, long path
   * @param {Path[]} paths
   * @returns {Path}
   */
  static join(paths) {
    const rawPath = {};
    paths.forEach((path) => {
      Object.entries(path.ticks).forEach(([t, loc]) => {
        rawPath[t] = loc.toArrayCoordinate();
      });
    });
    return new Path({ t: rawPath });
  }
}
