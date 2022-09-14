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
const ALL_EVENTS = [AGENTS_SELECTED_EVENT, AGENT_FOCUS_ON_EVENT, AGENT_FOCUS_OFF_EVENT, CONFIG_LOADED];

export function emitTickEvent(tick) {
  emitter.emit(TICK_EVENT, tick);
}

export function emitAgentsSelectedEvent(selectedIds) {
  emitter.emit(AGENTS_SELECTED_EVENT, selectedIds);
}

export function emitFocusOnAgent(agentInFocus, previousAgentInFocus) {
  emitter.emit(AGENT_FOCUS_ON_EVENT, { agentInFocus, previousAgentInFocus });
}

export function emitFocusOffAgent(agent) {
  emitter.emit(AGENT_FOCUS_OFF_EVENT, agent);
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

export function onConfigLoaded(callback) {
  emitter.on(CONFIG_LOADED, callback);
}

export function offConfigLoaded() {
  emitter.off(CONFIG_LOADED);
}

export function emitConfigLoaded() {
  emitter.emit(CONFIG_LOADED);
}

export function onAllocatorSwitched(callback) {
  emitter.on(ALLOCATOR_SWITCHED, callback);
}

export function offAllocatorSwitched() {
  emitter.off(ALLOCATOR_SWITCHED);
}

export function emitAllocatorSwitched() {
  emitter.emit(ALLOCATOR_SWITCHED);
}

export function offAll() {
  ALL_EVENTS.forEach((event) => {
    emitter.off(event);
  });
}
