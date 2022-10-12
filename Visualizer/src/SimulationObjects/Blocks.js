import Space from "./Space";

export default class Blocks {
  /**
   * @param {JSONBlock} rawBlock
   * @param {RawAllocationStatistics} allocationStats
   */
  constructor(rawBlock, allocationStats) {
    this.tick = rawBlock.tick;
    this.spaces = rawBlock.spaces.map((space) => new Space(space));
    this.value = allocationStats.value;
    this.reason = allocationStats.reason;
    this.explanation = allocationStats.explanation;
  }
}
