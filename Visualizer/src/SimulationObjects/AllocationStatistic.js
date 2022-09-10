import PathStatistic from "@/SimulationObjects/PathStatistic.js";

export default class AllocationStatistic {
  /**
   *
   * @param {AllocationStatistics} allocationStatistic
   */
  constructor(allocationStatistic) {
    this.tick = allocationStatistic.tick;
    this.compute_time = allocationStatistic.compute_time;
    this.utility = allocationStatistic.value;
    this.reason = allocationStatistic.reason;
    this.collidingAgentIds = allocationStatistic.colliding_agent_ids;
    this.pathStatistics = allocationStatistic.path ? new PathStatistic(allocationStatistic.path) : null;
  }
}
