export default class Statistics {
  /**
   * @param {JSONStatistics} jsonStatistics
   */
  constructor(jsonStatistics) {
    this.totalNumberOfOwners = jsonStatistics.total_number_of_owners;
    this.totalNumberOfAgents = jsonStatistics.total_number_of_agents;
    this.totalValue = jsonStatistics.total_value;
    this.totalNumberOfCollisions = jsonStatistics.total_number_of_collisions;
    this.totalNumberOfReallocations = jsonStatistics.total_number_of_reallocations;
  }
}
