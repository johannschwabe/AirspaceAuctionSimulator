import "../API/typedefs.js";

import { useSimulationOutputStore } from "../stores/simulationOutputStore.js";

import Coordinate4D from "./Coordinate4D";
import Statistics from "./Statistics";
import Owner from "./Owner";
import MapTile from "./MapTile";
import { emitFocusOffAgent, emitFocusOnAgent, onAgentsSelected, onTick } from "../scripts/emitter.js";
import { BlockerType } from "../API/enums.js";
import StaticBlocker from "./StaticBlocker";
import DynamicBlocker from "./DynamicBlocker";
import PathAgent from "./PathAgent";
import SpaceAgent from "./SpaceAgent";

export default class Simulation {
  /**
   * @param {JSONSimulation} jsonSimulation
   * @param {JSONConfig} jsonConfig
   * @param {SimulationStatistics} simulationStats
   * @param {OwnerMap} ownerMap
   */
  constructor(jsonSimulation, jsonConfig, simulationStats, ownerMap) {
    this._simulationStore = useSimulationOutputStore();

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
          throw new Error(`Invalid blocker type ${blocker.blockerType}!`);
      }
    });

    /**
     * Path owners that were simulated
     * @type {Owner[]}
     */
    this.path_owners = jsonSimulation.path_owners
      .sort((o1, o2) => parseInt(o1.id, 10) - parseInt(o2.id, 10))
      .map((owner) => {
        const ownerStats = simulationStats.path_owners.find((ownerStat) => ownerStat.id === owner.id);
        return new Owner(owner, this, ownerStats, ownerMap[owner.id]);
      });

    /**
     * Path owners that were simulated
     * @type {Owner[]}
     */
    this.space_owners = jsonSimulation.space_owners
      .sort((o1, o2) => parseInt(o1.id, 10) - parseInt(o2.id, 10))
      .map((owner) => {
        const ownerStats = simulationStats.space_owners.find((ownerStat) => ownerStat.id === owner.id);
        return new Owner(owner, this, ownerStats, ownerMap[owner.id]);
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
     * Stores how many agents got reallocated at each possible tick
     * @type {int[]}
     */
    this.timelineReAllocations = [];

    /**
     * Stores how many agents violated the airspace of another agent at each possible tick
     * @type {int[]}
     */
    this.timelineViolations = [];

    /**
     * Stores how many agents violated the airspace of a blocker at each possible tick
     * @type {int[]}
     */
    this.timelineBlockerViolations = [];

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

  /**
   * @returns {Owner[]}
   */
  get owners() {
    return [...this.path_owners, ...this.space_owners]
      .sort((o1, o2) => parseInt(o1.id, 10) - parseInt(o2.id, 10));
  }

  /**
   * @returns {int}
   */
  get tick() {
    return this._simulationStore.tick;
  }

  /**
   * @param {int} tick
   */
  set tick(tick) {
    this._simulationStore.updateTick(tick);
  }

  /**
   * @returns {string[]}
   */
  get activeAgentIDs() {
    return this.activeAgents.map((agent) => agent.id);
  }

  /**
   * @returns {string[]}
   */
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
        if (!(tick.toString() in activeBlockerIndex)) {
          activeBlockerIndex[tick] = [];
        }
        activeBlockerIndex[tick].push(blocker);
      });
    });
    return activeBlockerIndex;
  }

  /**
   * Updates selected agent IDs according to data from store
   */
  updateSelectedAgents() {
    this.selectedAgents = this.agents.filter((agent) => this._simulationStore.selectedAgentIDs.includes(agent.id));
  }

  /**
   * Update active agents according to data from store
   */
  updateActiveAgents() {
    const currentActiveAgents = this.flyingAgentsPerTickIndex[this.tick] || [];
    this.activeAgents = currentActiveAgents.filter((agent) => {
      return this._simulationStore.selectedAgentIDs.includes(agent.id);
    });
  }

  /**
   * Update active blockers according to data from store
   */
  updateActiveBlockers() {
    this.activeBlockers = this.activeBlockersPerTickIndex[this.tick] || [];
  }

  /**
   * Build datastructure that holds timely event information, such as number of active
   * agents or re-allocation / violation events
   */
  updateTimeline() {
    const agentsPerTick = {};
    const reAllocationsPerTick = {};
    const violationsPerTick = {};
    const blockerViolationsPerTick = {};
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
      agent.reAllocationTimesteps.forEach((tick) => {
        if (!(tick in reAllocationsPerTick)) {
          reAllocationsPerTick[tick] = 0;
        }
        reAllocationsPerTick[tick] += 1;
      });
      agent.violationsTimesteps.forEach((tick) => {
        if (!(tick in violationsPerTick)) {
          violationsPerTick[tick] = 0;
        }
        violationsPerTick[tick] += 1;
      });

      agent.blockerViolationsTimesteps.forEach((tick) => {
        if (!(tick in blockerViolationsPerTick)) {
          blockerViolationsPerTick[tick] = 0;
        }
        blockerViolationsPerTick[tick] += 1;
      });
    });
    const timeline = Array(maxTick).fill(0);
    const timelineReAllocations = Array(maxTick).fill(0);
    const timelineViolations = Array(maxTick).fill(0);
    const timelineBlockerViolations = Array(maxTick).fill(0);
    Object.entries(agentsPerTick).forEach(([tick, numberOfAgents]) => {
      timeline[tick] = numberOfAgents;
    });
    Object.entries(reAllocationsPerTick).forEach(([tick, numberOfReallocations]) => {
      timelineReAllocations[tick] = numberOfReallocations;
    });
    Object.entries(violationsPerTick).forEach(([tick, numberOfViolations]) => {
      timelineViolations[tick] = numberOfViolations;
    });
    Object.entries(blockerViolationsPerTick).forEach(([tick, numberOfViolations]) => {
      timelineBlockerViolations[tick] = numberOfViolations;
    });
    this.timeline = timeline;
    this.timelineReAllocations = timelineReAllocations;
    this.timelineViolations = timelineViolations;
    this.timelineBlockerViolations = timelineBlockerViolations;
    this.maxTick = maxTick;
  }

  /**
   * Puts a new agent into focus
   * @param {PathAgent} agent
   */
  focusOnAgent(agent) {
    if (this.agentInFocus === agent) {
      return;
    }
    const previousAgentInFocus = this.agentInFocus;
    this._simulationStore.agentInFocus = true;
    this._simulationStore.agentInFocusId = agent.id;
    this._simulationStore.ownerInFocusId = agent.owner.id;
    this.agentInFocus = agent;
    emitFocusOnAgent(agent, previousAgentInFocus);
  }

  /**
   * Deactivate focus mode
   */
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
