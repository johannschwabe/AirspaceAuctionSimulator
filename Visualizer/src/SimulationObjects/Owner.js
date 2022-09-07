import PathAgent from "./PathAgent";
import SpaceAgent from "./SpaceAgent";
import { AgentType } from "../API/enums";

export default class Owner {
  /**
   * @param {JSONOwner} rawOwner
   * @param {Simulation} simulation
   * @param {OwnerStatistics} ownerStats
   */
  constructor(rawOwner, simulation, ownerStats) {
    this.name = rawOwner.name;
    this.id = rawOwner.id;
    this.color = rawOwner.color;
    this.totalTimeInAir = ownerStats.total_time_in_air;
    this.totalUtility = ownerStats.values.total;
    this.meanUtility = ownerStats.values.mean;
    this.medianUtility = ownerStats.values.median;
    this.minUtility = ownerStats.values.min;
    this.maxUtility = ownerStats.values.max;
    this.utilityQuartiles = ownerStats.values.quartiles;
    this.utilityOutliers = ownerStats.values.outliers;
    this.numberOfAgents = ownerStats.number_of_agents;

    /**
     * All agents belonging to this owner
     * @type {PathAgent|SpaceAgent[]}
     */
    this.agents = rawOwner.agents.map((agent) => {
      const agentStats = ownerStats.agents.find((agentStat) => agentStat.id === agent.id);
      switch (agent.agent_type) {
        case AgentType.SPACE:
          return new SpaceAgent(agent, this, simulation, agentStats);
        case AgentType.PATH:
          return new PathAgent(agent, this, simulation, agentStats);
        default:
          throw new Error("Invalid agent type!");
      }
    });

    this._simulation = simulation;
  }
}
