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
    this.utility = rawAgent.utility;
    this.nonCollidingUtility = rawAgent.non_colliding_utility;
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
