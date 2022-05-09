export default class Statistics {
  /**
   * @param {RawStatistics} rawStatistics
   */
  constructor(rawStatistics) {
    this.totalNumberOfOwners = rawStatistics.total_number_of_owners;
    this.totalNumberOfAgents = rawStatistics.total_number_of_agents;
    this.totalAchievedWelfare = rawStatistics.total_achieved_welfare;
    this.totalNumberOfCollisions = rawStatistics.total_number_of_collisions;
    this.totalNumberOfReallocations =
      rawStatistics.total_number_of_reallocations;
  }
}
