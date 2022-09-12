import PathStatistic from "@/SimulationObjects/PathStatistic.js";

export default class AllocationStatistic {
  /**
   *
   * @param {RawAllocationStatistics} allocationStatistic
   */
  constructor(allocationStatistic) {
    this.tick = allocationStatistic.tick;
    this.compute_time = allocationStatistic.compute_time;
    this.utility = allocationStatistic.value;
    this.bid = allocationStatistic.bid;
    this.reason = allocationStatistic.reason;
    this.explanation = allocationStatistic.explanation;
    this.collidingAgentIds = allocationStatistic.colliding_agent_ids;
    this.displacingAgentIds = allocationStatistic.displacing_agent_ids;
    this.pathStatistics = allocationStatistic.path ? new PathStatistic(allocationStatistic.path) : null;
  }
}
