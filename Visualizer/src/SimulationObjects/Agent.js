export default class Agent {
  /**
   *
   * @param {RawAgent} rawAgent
   * @param {Owner} owner
   * @param {Simulation} simulation
   */
  constructor(rawAgent, owner, simulation) {
    this.agentType = rawAgent.agent_type;
    this.allocationType = rawAgent.allocation_type;
    this.id = rawAgent.id;
    this.name = rawAgent.name;
    this.welfare = rawAgent.welfare;
    this.nonCollidingWelfare = rawAgent.non_colliding_welfare;
    this.bid = rawAgent.bid;
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
}
