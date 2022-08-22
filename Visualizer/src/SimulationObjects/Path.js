import Coordinate3D from "./Coordinate3D";
import { first, last } from "lodash-es";
export default class Path {
  /**
   * @param {RawPath} rawPath
   */
  constructor(rawPath) {
    /**
     * @type {Object<int, Coordinate3D>}
     */
    this.ticks = {};
    Object.entries(rawPath.t).forEach(([t, loc]) => {
      const [x, y, z] = loc;
      this.ticks[t] = new Coordinate3D(x, y, z);
    });
  }

  get ticksInAir() {
    return Object.keys(this.ticks);
  }

  get firstTick() {
    const tick = first(this.ticksInAir);
    return tick !== undefined ? parseInt(tick, 10) : null;
  }

  get lastTick() {
    const tick = last(this.ticksInAir);
    return tick !== undefined ? parseInt(tick, 10) : null;
  }

  get firstLocation() {
    return this.ticks[this.firstTick];
  }

  get lastLocation() {
    return this.ticks[this.lastTick];
  }

  get coordinates() {
    return Object.values(this.ticks);
  }

  isActiveAtTick(tick) {
    return this.ticksInAir.includes(`${tick}`);
  }

  at(tick) {
    return this.ticks[`${tick}`];
  }

  atIndex(index) {
    return this.ticks[this.ticksInAir[parseInt(index, 10)]];
  }

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
    return new Path({ t: rawPath });
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
        const path_segment = new Path({ t: {} });
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
