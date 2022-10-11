import PathAgent from "./PathAgent";
import SpaceAgent from "./SpaceAgent";
import { AgentType } from "../API/enums.js";
import BoxplotStatistics from "@/SimulationObjects/BoxplotStatistics";

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
    this.numberOfAgents = ownerStats.number_of_agents;

    this.utilityStatistics = new BoxplotStatistics(ownerStats.values);
    this.paymentStatistics = new BoxplotStatistics(ownerStats.payments);
    this.nonCollidingUtilityStatistics = new BoxplotStatistics(ownerStats.non_colliding_values);

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

  /**
   * @returns {string}
   */
  get displayName() {
    return this.name;
  }
}
