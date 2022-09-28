import Space from "./Space";

export default class Blocks {
  /**
   * @param {JSONBlocks} rawBranch
   * @param {RawAllocationStatistics} allocationStats
   */
  constructor(rawBranch, allocationStats) {
    this.tick = rawBranch.tick;
    this.spaces = rawBranch.spaces.map((space) => new Space(space));
    this.value = allocationStats.value;
    this.reason = allocationStats.reason;
    this.explanation = allocationStats.explanation;
  }
}
