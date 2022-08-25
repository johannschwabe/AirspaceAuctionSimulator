import PathAgent from "./PathAgent";
import SpaceAgent from "./SpaceAgent";
import { AgentType } from "../API/enums";

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
    this.totalUtility = rawOwner.total_utility;
    this.meanUtility = rawOwner.mean_utility;
    this.medianUtility = rawOwner.median_utility;
    this.minUtility = rawOwner.max_utility;
    this.maxUtility = rawOwner.min_utility;
    this.utilityQuantiles = rawOwner.utility_quantiles;
    this.utilityOutliers = rawOwner.utility_outliers;
    this.numberOfAgents = rawOwner.number_of_agents;
    this.numberOfABAgents = rawOwner.number_of_ab_agents;
    this.numberOfABAAgents = rawOwner.number_of_aba_agents;
    this.numberOfABCAgents = rawOwner.number_of_abc_agents;
    this.numberOfStationaryAgents = rawOwner.number_of_stationary_agents;

    /**
     * All agents belonging to this owner
     * @type {PathAgent|SpaceAgent[]}
     */
    this.agents = rawOwner.agents.map((agent) => {
      switch (agent.agent_type) {
        case AgentType.SPACE:
          return new SpaceAgent(agent, this, simulation);
        case AgentType.PATH:
          return new PathAgent(agent, this, simulation);
        default:
          throw new Error("Invalid agent type!");
      }
    });

    this._simulation = simulation;
  }
}
