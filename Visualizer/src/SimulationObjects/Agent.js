import PathStatistic from "@/SimulationObjects/PathStatistic.js";
import AllocationStatistic from "@/SimulationObjects/AllocationStatistic.js";

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

    this.timeInAir = agentStats.time_in_air;

    this.totalReallocations = agentStats.total_reallocations;

    this.violations = agentStats.violations.violations;
    this.totalViolations = agentStats.violations.total_violations;

    this.pathStatistics = agentStats.path ? new PathStatistic(agentStats.path) : null;
    this.allocationStatistics = agentStats.allocations.map((a) => new AllocationStatistic(a));

    this.reAllocationTimesteps = [];
    this.violationsTimesteps = Object.values(this.violations).map((loc) => loc.t);

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

  locationAtTick(tick) {
    /* abstract method */
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
