import "../API/typedefs.js";

import { first } from "lodash-es";

import { useSimulationStore } from "../stores/simulation.js";

import TimeCoordinate from "./TimeCoordinate";
import Blocker from "./Blocker";
import Statistics from "./Statistics";
import Owner from "./Owner";
import { onAgentsSelected, onTick } from "../scripts/emitter";

export default class Simulation {
  /**
   * @param {RawSimulation} rawSimulation
   */
  constructor(rawSimulation) {
    this._simulationStore = useSimulationStore();

    this.name = rawSimulation.name;
    this.description = rawSimulation.description;

    /**
     * Simulated dimension. Note: The dimension t describes how long new agents
     * were spawned. Agents might have flight-times exceeding t!
     * @type {TimeCoordinate}
     */
    this.dimensions = new TimeCoordinate(
      ...Object.values(rawSimulation.environment.dimensions)
    );

    /**
     * Object containing statistics about the simulation
     * @type {Statistics}
     */
    this.statistics = new Statistics(rawSimulation.statistics);

    /**
     * Blockers living in the simulated environment
     * @type {Blocker[]}
     */
    this.blockers = rawSimulation.environment.blockers.map(
      (blocker) => new Blocker(blocker)
    );

    /**
     * All owners that were simulated
     * @type {Owner[]}
     */
    this.owners = rawSimulation.owners.map((owner) => new Owner(owner, this));

    /**
     * Flattened list of all agents belonging to any owner
     * @type {Agent[]}
     */
    this.agents = this.owners
      .map((owner) => owner.agents)
      .flat()
      .sort((a, b) =>
        first(Object.keys(a.combinedPath.ticks)) <
        first(Object.keys(b.combinedPath.ticks))
          ? -1
          : 1
      );

    /**
     * List of agents that are selected in the User Interface
     * @type {Agent[]}
     */
    this.selectedAgents = [];

    /**
     * List of agents that are currently in the air based on the current tick
     * and also selected
     * @type {Agent[]}
     */
    this.activeAgents = [];

    /**
     * List of blockers that are displayed based on the current tick
     * @type {Blocker[]}
     */
    this.activeBlockers = [];

    /**
     * Agent that is selected through the UI and is now in focus
     * @type {Agent|null}
     */
    this.focusAgent = null;

    /**
     * Index of which agents are in air at which ticks
     * @type {Object<int, Agent[]>}
     */
    this.flyingAgentsPerTickIndex = this.buildFlyingAgentsPerTickIndex();

    /**
     * @type {Blocker[]}
     */
    this.activeBlockersPerTickIndex = this.buildActiveBlockersPerTickIndex();

    this.registerCallbacks();
    this.updateActiveBlockers();
    this.updateActiveAgents();

    console.log({ CreatedStore: this });
  }

  registerCallbacks() {
    onTick(() => {
      this.updateActiveAgents();
      this.updateActiveBlockers();
      console.log({ UpdatedSimulation: this });
    });
    onAgentsSelected(() => {
      this.updateSelectedAgents();
      this.updateActiveAgents();
      console.log({ UpdatedSimulation: this });
    });
  }

  get tick() {
    return this._simulationStore.tick;
  }

  set tick(tick) {
    this._simulationStore.tick = tick;
  }

  get activeAgentIDs() {
    return this.activeAgents.map((agent) => agent.id);
  }

  get activeBlockerIDs() {
    return this.activeBlockers.map((blocker) => blocker.id);
  }

  get focusOwner() {
    return this.focusAgent?.owner || null;
  }

  /**
   * @returns {Object<int, Agent[]>}
   */
  buildFlyingAgentsPerTickIndex() {
    const flyingAgentsPerTick = {};
    this.agents.forEach((agent) => {
      Object.keys(agent.combinedPath.ticks).forEach((t) => {
        if (!(t in flyingAgentsPerTick)) {
          flyingAgentsPerTick[t] = [];
        }
        flyingAgentsPerTick[t].push(agent);
      });
    });
    return flyingAgentsPerTick;
  }

  /**
   * @returns {Object<int, Blocker[]>}
   */
  buildActiveBlockersPerTickIndex() {
    const activeBlockerIndex = {};
    this.blockers.forEach((blocker) => {
      blocker.path.ticksInAir.forEach((tick) => {
        if (!(tick in activeBlockerIndex)) {
          activeBlockerIndex[tick] = [];
        }
        activeBlockerIndex[tick].push(blocker);
      });
    });
    return activeBlockerIndex;
  }

  updateSelectedAgents() {
    this.selectedAgents = this.agents.filter((agent) =>
      this._simulationStore.selectedAgentIDs.includes(agent.id)
    );
  }

  updateActiveAgents() {
    const currentActiveAgents = this.flyingAgentsPerTickIndex[this.tick] || [];
    this.activeAgents = currentActiveAgents.filter((agent) => {
      return this._simulationStore.selectedAgentIDs.includes(agent.id);
    });
  }

  updateActiveBlockers() {
    this.activeBlockers = this.activeBlockersPerTickIndex[this.tick] || [];
  }

  /**
   * Puts a new agent into focus
   * @param {Agent} agent
   */
  focusOnAgent(agent) {
    this.focusAgent = agent;
  }
}
