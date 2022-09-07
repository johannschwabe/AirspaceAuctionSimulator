export default class Statistics {
  /**
   * @param {SimulationStatistics} statistics
   */
  constructor(statistics) {
    this.totalNumberOfOwners = statistics.total_number_of_owners;
    this.totalNumberOfAgents = statistics.total_number_of_agents;
    this.totalValue = statistics.total_value;
    this.totalNumberOfCollisions = statistics.total_number_of_collisions;
    this.totalNumberOfReallocations = statistics.total_number_of_reallocations;
  }
}
