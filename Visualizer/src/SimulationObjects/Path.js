import { first, last } from "lodash-es";

import Coordinate3D from "./Coordinate3D.js";

export default class Path {
  /**
   * @param {JSONPath} rawPath
   */
  constructor(rawPath) {
    /**
     * @type {Object<int, Coordinate3D>}
     */
    this.ticks = {};
    Object.entries(rawPath.positions).forEach(([t, loc]) => {
      const [x, y, z] = loc;
      this.ticks[t] = new Coordinate3D(x, y, z);
    });
  }

  /**
   * @returns {int[]}
   */
  get ticksInAir() {
    return Object.keys(this.ticks).map((t) => parseInt(t, 10));
  }

  /**
   * @returns {int|undefined}
   */
  get firstTick() {
    return first(this.ticksInAir);
  }

  /**
   * @returns {int|undefined}
   */
  get lastTick() {
    return last(this.ticksInAir);
  }

  /**
   * @returns {Coordinate3D}
   */
  get firstLocation() {
    return this.ticks[this.firstTick];
  }

  /**
   * @returns {Coordinate3D}
   */
  get lastLocation() {
    return this.ticks[this.lastTick];
  }

  /**
   * @returns {Coordinate3D[]}
   */
  get coordinates() {
    return Object.values(this.ticks);
  }

  /**
   * @param {int} tick
   * @returns {boolean}
   */
  isActiveAtTick(tick) {
    return this.ticksInAir.includes(parseInt(tick, 10));
  }

  /**
   * @param {int} tick
   * @returns {Coordinate3D}
   */
  at(tick) {
    return this.ticks[`${tick}`];
  }

  /**
   * @param {int} index
   * @returns {Coordinate3D}
   */
  atIndex(index) {
    return this.ticks[this.ticksInAir[parseInt(index, 10)]];
  }

  /**
   * @param {Coordinate3D} coordinate
   * @returns {boolean}
   */
  containsCoordinate(coordinate) {
    return this.coordinates.some((coord) => coord.xyz === coordinate.xyz);
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
    return new Path({ positions: rawPath });
  }

  /**
   * Subtracts all segments from path_to_subtract from path and returns the
   * path snippets that are exclusive to path
   * @param {Path} path
   * @param {Path} path_to_subtract
   * @returns {Path[]}
   */
  static subtract(path, path_to_subtract) {
    const path_segments = [];
    let segment_ticks = {};
    let off_segment = false;
    Object.entries(path.ticks).forEach(([tick, coordinate]) => {
      const distinct_path = !path_to_subtract.containsCoordinate(coordinate);
      if (distinct_path && !off_segment && path.isActiveAtTick(tick - 1)) {
        segment_ticks[tick - 1] = path.at(tick - 1);
      }
      if (distinct_path) {
        segment_ticks[tick] = coordinate;
      }
      if (!distinct_path && off_segment) {
        segment_ticks[tick] = coordinate;
        const path_segment = new Path({ positions: {} });
        path_segment.ticks = segment_ticks;
        path_segments.push(path_segment);
        segment_ticks = {};
        off_segment = false;
      }
      if (distinct_path) {
        off_segment = true;
      }
    });
    return path_segments;
  }
}
