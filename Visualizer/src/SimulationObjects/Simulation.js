import "../API/typedefs.js";

import { useSimulationStore } from "../stores/simulation";

import Coordinate4D from "./Coordinate4D";
import Statistics from "./Statistics";
import Owner from "./Owner";
import MapTile from "./MapTile";
import { emitFocusOffAgent, emitFocusOnAgent, onAgentsSelected, onTick } from "../scripts/emitter";
import { BlockerType } from "../API/enums";
import StaticBlocker from "./StaticBlocker";
import DynamicBlocker from "./DynamicBlocker";
import PathAgent from "./PathAgent";
import SpaceAgent from "./SpaceAgent";

export default class Simulation {
  /**
   * @param {JSONSimulation} jsonSimulation
   * @param {JSONConfig} jsonConfig
   * @param {SimulationStatistics} simulationStats
   */
  constructor(jsonSimulation, jsonConfig, simulationStats) {
    this._simulationStore = useSimulationStore();

    this.name = jsonConfig.name;
    this.description = jsonConfig.description;

    /**
     * Simulated dimension. Note: The dimension t describes how long new agents
     * were spawned. Agents might have flight-times exceeding t!
     * @type {Coordinate4D}
     */
    this.dimensions = new Coordinate4D(
      jsonSimulation.environment.dimensions.x,
      jsonSimulation.environment.dimensions.y,
      jsonSimulation.environment.dimensions.z,
      jsonSimulation.environment.dimensions.t
    );

    /**
     * Object containing statistics about the simulation
     * @type {Statistics}
     */
    this.statistics = new Statistics(simulationStats);

    /**
     * Blockers living in the simulated environment
     * @type {Blocker[]}
     */
    this.blockers = jsonSimulation.environment.blockers.map((blocker) => {
      switch (blocker.blocker_type) {
        case BlockerType.DYNAMIC:
          return new DynamicBlocker(blocker);
        case BlockerType.STATIC:
          return new StaticBlocker(blocker, this.dimensions.t);
        default:
          throw new Error("Invalid blocker type!");
      }
    });

    /**
     * All owners that were simulated
     * @type {Owner[]}
     */
    this.owners = jsonSimulation.owners.map((owner) => {
      const ownerStats = simulationStats.owners.find((ownerStat) => ownerStat.id === owner.id);
      return new Owner(owner, this, ownerStats);
    });

    /**
     * Flattened list of all agents belonging to any owner
     * @type {Agent[]}
     */
    this.agents = this.owners
      .map((owner) => owner.agents)
      .flat()
      .sort((a, b) => {
        return a.veryFirstTick < b.veryFirstTick ? -1 : 1;
      });

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
     * Agents that is selected through the UI and is now in focus
     * @type {PathAgent|null}
     */
    this.agentInFocus = null;

    /**
     * Index of which agents are in air at which ticks
     * @type {Object<int, Agent[]>}
     */
    this.flyingAgentsPerTickIndex = this.buildFlyingAgentsPerTickIndex();

    /**
     * @type {Blocker[]}
     */
    this.activeBlockersPerTickIndex = this.buildActiveBlockersPerTickIndex();

    /**
     * @type {MapTile[]}
     */
    this.mapTiles = jsonConfig.map.tiles.map(
      (tile) =>
        new MapTile(
          tile,
          jsonConfig.map.resolution,
          jsonConfig.map.subselection?.bottomLeft || jsonConfig.map.bottomLeftCoordinate,
          jsonConfig.map.subselection?.topRight || jsonConfig.map.topRightCoordinate
        )
    );

    /**
     * Stores how many active agents are present over all possible ticks
     * @type {int[]}
     */
    this.timeline = [];

    /**
     * Holds a list of events at each timestep
     * @type {*[]}
     */
    this.timelineEvents = [];

    /**
     * The maximum tick at which any active agent is still active / flying
     * @type {number}
     */
    this.maxTick = -1;

    this.registerCallbacks();
    this.updateSelectedAgents();
    this.updateActiveAgents();
    this.updateActiveBlockers();
    this.updateTimeline();
  }

  get tick() {
    return this._simulationStore.tick;
  }

  set tick(tick) {
    this._simulationStore.updateTick(tick);
  }

  get activeAgentIDs() {
    return this.activeAgents.map((agent) => agent.id);
  }

  get activeBlockerIDs() {
    return this.activeBlockers.map((blocker) => blocker.id);
  }

  /**
   * @returns {Owner|null}
   */
  get ownerInFocus() {
    return this.agentInFocus?.owner || null;
  }

  /**
   * @returns {PathAgent[]}
   */
  get activePathAgents() {
    return this.activeAgents.filter((agent) => agent instanceof PathAgent);
  }

  /**
   * @returns {SpaceAgent[]}
   */
  get activeSpaceAgents() {
    return this.activeAgents.filter((agent) => agent instanceof SpaceAgent);
  }

  registerCallbacks() {
    onTick(() => {
      this.updateActiveAgents();
      this.updateActiveBlockers();
    });
    onAgentsSelected(() => {
      this.updateSelectedAgents();
      this.updateActiveAgents();
      this.updateTimeline();
    });
  }

  /**
   * @returns {Object<int, Agent[]>}
   */
  buildFlyingAgentsPerTickIndex() {
    const flyingAgentsPerTick = {};
    this.agents.forEach((agent) => {
      agent.flyingTicks.forEach((t) => {
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
      blocker.ticksInAir.forEach((tick) => {
        if (!(tick in activeBlockerIndex)) {
          activeBlockerIndex[tick] = [];
        }
        activeBlockerIndex[tick].push(blocker);
      });
    });
    return activeBlockerIndex;
  }

  updateSelectedAgents() {
    this.selectedAgents = this.agents.filter((agent) => this._simulationStore.selectedAgentIDs.includes(agent.id));
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

  updateTimeline() {
    const agentsPerTick = {};
    let maxTick = 0;
    this.selectedAgents.forEach((agent) => {
      agent.flyingTicks.forEach((tick) => {
        if (!(tick in agentsPerTick)) {
          agentsPerTick[tick] = 0;
        }
        agentsPerTick[tick] += 1;
        if (parseInt(tick, 10) > maxTick) {
          maxTick = parseInt(tick, 10);
        }
      });
    });
    const timeline = Array(maxTick).fill(0);
    Object.entries(agentsPerTick).forEach(([tick, numberOfAgents]) => {
      timeline[tick] = numberOfAgents;
    });
    this.timeline = timeline;
    this.maxTick = maxTick;
  }

  /**
   * Puts a new agent into focus
   * @param {PathAgent} agent
   */
  focusOnAgent(agent) {
    if (this.agentInFocus === agent || !agent.isActiveAtTick(this.tick)) {
      return;
    }
    this._simulationStore.agentInFocus = true;
    this._simulationStore.agentInFocusId = agent.id;
    this._simulationStore.ownerInFocusId = agent.owner.id;
    this.agentInFocus = agent;
    emitFocusOnAgent(agent);
  }

  focusOff() {
    emitFocusOffAgent(this.agentInFocus);
    this._simulationStore.agentInFocus = false;
    this.agentInFocus = null;
  }

  /**
   * @returns {Promise<Simulation>}
   */
  async load() {
    const promises = this.mapTiles.map((maptile) => maptile.load());
    await Promise.all(promises);
    return this;
  }
}
