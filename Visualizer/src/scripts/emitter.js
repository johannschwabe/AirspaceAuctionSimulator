import mitt from "mitt";
const emitter = mitt();
export const useEmitter = () => {
  return emitter;
};

const TICK_EVENT = "tick";
const AGENTS_SELECTED_EVENT = "agents-selected";
const AGENT_FOCUS_ON_EVENT = "focus-on-agent";
const AGENT_FOCUS_OFF_EVENT = "focus-off-agent";
const CONFIG_LOADED = "config-loaded";
const ALLOCATOR_SWITCHED = "allocator-switched";
const ALL_EVENTS = [
  TICK_EVENT,
  AGENTS_SELECTED_EVENT,
  AGENT_FOCUS_ON_EVENT,
  AGENT_FOCUS_OFF_EVENT,
  CONFIG_LOADED,
  ALLOCATOR_SWITCHED,
];

/**
 * @param {number} tick
 */
export function emitTickEvent(tick) {
  emitter.emit(TICK_EVENT, tick);
}

/**
 * @param {string[]} selectedIds
 */
export function emitAgentsSelectedEvent(selectedIds) {
  emitter.emit(AGENTS_SELECTED_EVENT, selectedIds);
}

/**
 * @param {Agent} agentInFocus
 * @param {Agent|null} previousAgentInFocus
 */
export function emitFocusOnAgent(agentInFocus, previousAgentInFocus) {
  emitter.emit(AGENT_FOCUS_ON_EVENT, { agentInFocus, previousAgentInFocus });
}

/**
 * @param {Agent} agent
 */
export function emitFocusOffAgent(agent) {
  emitter.emit(AGENT_FOCUS_OFF_EVENT, agent);
}

export function emitConfigLoaded() {
  emitter.emit(CONFIG_LOADED);
}

export function emitAllocatorSwitched() {
  emitter.emit(ALLOCATOR_SWITCHED);
}

export function onTick(callback) {
  emitter.on(TICK_EVENT, callback);
}

export function onAgentsSelected(callback) {
  emitter.on(AGENTS_SELECTED_EVENT, callback);
}

export function onFocusOnAgent(callback) {
  emitter.on(AGENT_FOCUS_ON_EVENT, callback);
}

export function onFocusOffAgent(callback) {
  emitter.on(AGENT_FOCUS_OFF_EVENT, callback);
}

export function onConfigLoaded(callback) {
  emitter.on(CONFIG_LOADED, callback);
}

export function onAllocatorSwitched(callback) {
  emitter.on(ALLOCATOR_SWITCHED, callback);
}

export function offTick(callback) {
  emitter.on(TICK_EVENT, callback);
}

export function offAgentsSelected() {
  emitter.off(AGENTS_SELECTED_EVENT);
}

export function offFocusOnAgent() {
  emitter.off(AGENT_FOCUS_ON_EVENT);
}

export function offFocusOffAgent() {
  emitter.off(AGENT_FOCUS_OFF_EVENT);
}

export function offConfigLoaded() {
  emitter.off(CONFIG_LOADED);
}

export function offAllocatorSwitched() {
  emitter.off(ALLOCATOR_SWITCHED);
}

export function offAll() {
  ALL_EVENTS.forEach((event) => {
    emitter.off(event);
  });
}
