import AllocationStatistic from "./AllocationStatistic";

export default class Agent {
  /**
   * @param {JSONAgent} rawAgent
   * @param {Owner} owner
   * @param {Simulation} simulation
   * @param {AgentStatistics} agentStats
   */
  constructor(rawAgent, owner, simulation, agentStats) {
    this.agentType = rawAgent.agent_type;
    this.id = rawAgent.id;
    this.name = owner.name + "-" + rawAgent.id;
    this.value = agentStats.value;
    this.nonCollidingValue = agentStats.non_colliding_value;
    this.utility = agentStats.utility;
    this.nonCollidingUtility = agentStats.non_colliding_utility;
    this.payment = agentStats.payment;
    this.owner = owner;
    this.color = owner.color;

    this.timeInAir = agentStats.time_in_air;

    this.totalReallocations = agentStats.total_reallocations;

    this.violations = agentStats.violations.violations;
    this.totalViolations = agentStats.violations.total_violations;
    this.blockerViolations = agentStats.violations.blocker_violations;
    this.totalBlockerViolations = agentStats.violations.total_blocker_violations;

    this.incompleAllocation = agentStats.violations.incomplete_allocation;

    this.reAllocationTimesteps = [];
    this.violationsTimesteps = Object.values(this.violations)
      .flat()
      .map((loc) => loc.t);
    this.blockerViolationsTimesteps = this.blockerViolations
      ? Object.values(this.blockerViolations)
          .flat()
          .map((loc) => loc.t)
      : [];

    this._simulation = simulation;
    this.allocationStatistics = agentStats.allocations.map((a) => new AllocationStatistic(a));
  }

  /**
   * @returns {string}
   */
  get displayName() {
    return this.id;
  }

  /**
   * Returns a list of all relevant events for the given agent over his lifetime
   * @returns {FlightEvent[]}
   */
  get events() {
    return [];
  }

  /**
   * @abstract
   */
  focus() {
    /* abstract method */
  }

  /**
   * @param {number} tick
   * @returns {boolean}
   */
  isActiveAtTick(tick) {
    return this.flyingTicks.includes(parseInt(tick, 10));
  }

  /**
   * @abstract
   * @param {number} tick
   */
  locationAtTick(tick) {
    /* abstract method */
  }

  /**
   * @abstract
   * @returns {number[]}
   */
  get flyingTicks() {
    /* abstract method */
    return [];
  }

  /**
   * @abstract
   * @returns {[number, number][]}
   */
  get segmentsStartEnd() {
    /* abstract method */
    return [];
  }

  /**
   * @abstract
   * @returns {number}
   */
  get veryFirstTick() {
    /* abstract method */
    return -1;
  }

  /**
   * @abstract
   * @returns {number}
   */
  get veryLastTick() {
    /* abstract method */
    return -1;
  }
}
