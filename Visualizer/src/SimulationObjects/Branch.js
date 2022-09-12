import Path from "./Path";

export default class Branch {
  /**
   *
   * @param {JSONBranch} rawBranch
   * @param {AllocationStatistics} allocationStats
   */
  constructor(rawBranch, allocationStats) {
    this.tick = rawBranch.tick;
    this.paths = rawBranch.paths.map((path) => new Path(path));
    this.value = allocationStats.value;
    this.reason = allocationStats.reason;
    this.explanation = allocationStats.explanation;
  }
}
