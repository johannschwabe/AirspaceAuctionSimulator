import BoxplotStatistics from "@/SimulationObjects/BoxplotStatistics";

export default class Statistics {
  /**
   * @param {SimulationStatistics} statistics
   */
  constructor(statistics) {
    this.totalNumberOfOwners = statistics.total_number_of_owners;
    this.totalNumberOfAgents = statistics.total_number_of_agents;
    this.totalNumberOfViolations = statistics.total_number_of_violations;
    this.totalNumberOfReallocations = statistics.total_number_of_reallocations;
    this.computeTimes = Object.values(statistics.step_compute_time);
    this.totalComputeTime = this.computeTimes.reduce((acc, curr) => acc + curr, 0);

    this.totalNonCollidingValue = statistics.total_non_colliding_value;
    this.totalNonCollidingUtility = statistics.total_non_colliding_utility;
    this.value = new BoxplotStatistics(statistics.value_stats);
    this.utility = new BoxplotStatistics(statistics.utility_stats);
    this.payment = new BoxplotStatistics(statistics.payment_stats);
  }
}
