export default class Agent {
  /**
   *
   * @param {JSONAgent} rawAgent
   * @param {Owner} owner
   * @param {Simulation} simulation
   * @param {AgentStatistics} agentStats
   */
  constructor(rawAgent, owner, simulation, agentStats) {
    this.agentType = rawAgent.agent_type;
    this.id = rawAgent.id;
    this.name = owner.name + "-" + rawAgent.id;
    this.utility = agentStats.value;
    this.nonCollidingUtility = agentStats.non_colliding_value;
    this.owner = owner;
    this.color = owner.color;
    this._simulation = simulation;
  }

  /**
   * Returns a list of all relevant events for the given agent over his lifetime
   * @returns {FlightEvent[]}
   */
  get events() {
    return [];
  }

  focus() {
    /* abstract method */
  }

  isActiveAtTick(tick) {
    return this.flyingTicks.includes(parseInt(tick, 10));
  }

  get flyingTicks() {
    /* abstract method */
    return [];
  }

  get segmentsStartEnd() {
    /* abstract method */
    return [];
  }

  get veryFirstTick() {
    /* abstract method */
    return -1;
  }

  get veryLastTick() {
    /* abstract method */
    return -1;
  }
}
