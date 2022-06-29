import mitt from "mitt";
const emitter = mitt();
export const useEmitter = () => {
  return emitter;
};

const TICK_EVENT = "tick";
const AGENTS_SELECTED_EVENT = "agents-selected";
const AGENT_FOCUS_ON_EVENT = "focus-on-agent";
const AGENT_FOCUS_OFF_EVENT = "focus-off-agent";
const ALL_EVENTS = [AGENTS_SELECTED_EVENT, AGENT_FOCUS_ON_EVENT, AGENT_FOCUS_OFF_EVENT];

export function emitTickEvent(tick) {
  emitter.emit(TICK_EVENT, tick);
}

export function emitAgentsSelectedEvent(selectedIds) {
  emitter.emit(AGENTS_SELECTED_EVENT, selectedIds);
}

export function emitFocusOnAgent(agent) {
  emitter.emit(AGENT_FOCUS_ON_EVENT, agent);
}

export function emitFocusOffAgent() {
  emitter.emit(AGENT_FOCUS_OFF_EVENT);
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

export function offAll() {
  ALL_EVENTS.forEach((event) => {
    emitter.off(event);
  });
}
