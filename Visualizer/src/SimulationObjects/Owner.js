import Agent from "./Agent";

export default class Owner {
  /**
   * @param {RawOwner} rawOwner
   * @param {Simulation} simulation
   */
  constructor(rawOwner, simulation) {
    this.name = rawOwner.name;
    this.id = rawOwner.id;
    this.color = rawOwner.color;
    this.totalTimeInAir = rawOwner.total_time_in_air;
    this.totalBidValue = rawOwner.total_bid_value;
    this.meanBidValue = rawOwner.mean_bid_value;
    this.medianBidValue = rawOwner.median_bid_value;
    this.maxBidValue = rawOwner.max_bid_value;
    this.minBidValue = rawOwner.min_bid_value;
    this.bidQuantiles = rawOwner.bid_quantiles;
    this.bidOutliers = rawOwner.bid_outliers;
    this.totalWelfare = rawOwner.total_welfare;
    this.meanWelfare = rawOwner.mean_welfare;
    this.medianWelfare = rawOwner.median_welfare;
    this.minWelfare = rawOwner.max_welfare;
    this.maxWelfare = rawOwner.min_welfare;
    this.welfareQuantiles = rawOwner.welfare_quantiles;
    this.welfareOutliers = rawOwner.welfare_outliers;
    this.numberOfAgents = rawOwner.number_of_agents;
    this.numberOfABAgents = rawOwner.number_of_ab_agents;
    this.numberOfABAAgents = rawOwner.number_of_aba_agents;
    this.numberOfABCAgents = rawOwner.number_of_abc_agents;
    this.numberOfStationaryAgents = rawOwner.number_of_stationary_agents;

    /**
     * All agents belonging to this owner
     * @type {Agent[]}
     */
    this.agents = rawOwner.agents.map(
      (agent) => new Agent(agent, this, simulation)
    );

    this._simulation = simulation;
  }
}
