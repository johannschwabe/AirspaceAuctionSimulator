export default class Statistics {
  /**
   * @param {SimulationStatistics} statistics
   */
  constructor(statistics) {
    this.totalNumberOfOwners = statistics.total_number_of_owners;
    this.totalNumberOfAgents = statistics.total_number_of_agents;
    this.totalValue = statistics.total_value;
    this.totalNonCollidingValue = statistics.total_non_colliding_value;
    this.totalNumberOfViolations = statistics.total_number_of_violations;
    this.totalNumberOfReallocations = statistics.total_number_of_reallocations;
    this.computeTimes = Object.values(statistics.step_compute_time);
    this.totalComputeTime = this.computeTimes.reduce((acc, curr) => acc + curr, 0);
  }
}
