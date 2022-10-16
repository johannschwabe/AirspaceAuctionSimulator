import PathStatistic from "@/SimulationObjects/PathStatistic.js";
import SpaceStatistic from "@/SimulationObjects/SpaceStatistic.js";

export default class AllocationStatistic {
  /**
   * @param {RawAllocationStatistics} allocationStatistic
   */
  constructor(allocationStatistic) {
    this.tick = allocationStatistic.tick;
    this.compute_time = allocationStatistic.compute_time;
    this.value = allocationStatistic.value;
    this.utility = allocationStatistic.utility;
    this.payment = allocationStatistic.payment;
    this.bid = allocationStatistic.bid;
    this.reason = allocationStatistic.reason;
    this.explanation = allocationStatistic.explanation;
    this.collidingAgentBids = allocationStatistic.colliding_agent_bids;
    this.displacingAgentBids = allocationStatistic.displacing_agent_bids;
    this.pathStatistics = allocationStatistic.path ? new PathStatistic(allocationStatistic.path) : null;
    this.spaceStatistics = allocationStatistic.space ? new SpaceStatistic(allocationStatistic.space) : null;
  }
}
