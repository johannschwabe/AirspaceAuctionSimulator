import {
  mdiAirplaneLanding,
  mdiAirplaneTakeoff,
  mdiSourceBranchCheck,
  mdiSourceBranchSync,
  mdiSourceBranchRemove,
} from "@mdi/js";
import { BRANCH_REASONS } from "@/API/enums";

export class FlightEvent {
  /**
   * @param {string} title
   * @param {string} type
   * @param {string} icon
   * @param {int} tick
   * @param {?string} content
   */
  constructor(title, type, icon, tick, content = "") {
    this.title = title;
    this.type = type;
    this.icon = icon;
    this.tick = tick;
    this.time = `Tick: ${this.tick}`;
    this.content = content;
  }

  /**
   * @returns {(function(FlightEvent, FlightEvent): number)}
   */
  static get sortEventsFunction() {
    return (e1, e2) => {
      if (e1.tick === e2.tick) {
        return e1 instanceof TakeOffEvent ? 1 : -1;
      }
      return e1.tick > e2.tick ? 1 : -1;
    };
  }
}

export class TakeOffEvent extends FlightEvent {
  /**
   * @param {int} tick
   * @param {Coordinate3D} location
   */
  constructor(tick, location) {
    super("Take Off", "default", mdiAirplaneTakeoff, tick);
    this.location = location;
  }
}

export class ArrivalEvent extends FlightEvent {
  /**
   * @param {int} tick
   * @param {Coordinate3D} location
   */
  constructor(tick, location) {
    super("Arrival", "success", mdiAirplaneLanding, tick);
    this.location = location;
  }
}

export class ReservationStartEvent extends FlightEvent {
  /**
   * @param {int} tick
   * @param {int} start - Indicates when the reservation starts
   */
  constructor(tick, start = 1) {
    super(`Reservation Start ${start > 1 ? "x" + start.toString() : ""}`, "default", mdiAirplaneLanding, tick);
  }
}

export class ReReservationEvent extends FlightEvent {
  constructor(tick) {
    super("Reservation changed", "warning", mdiSourceBranchSync, tick);
  }
}
export class FirstReservationEvent extends FlightEvent {
  /**
   * @param {int} tick
   */
  constructor(tick) {
    super("First Allocation", "warning", mdiSourceBranchCheck, tick);
  }
}
export class FailedReservationEvent extends FlightEvent {
  /**
   * @param {int} tick
   */
  constructor(tick) {
    super("Failed Allocation", "warning", mdiSourceBranchRemove, tick);
  }
}

export class ReservationEndEvent extends FlightEvent {
  /**
   * @param {int} tick
   * @param {int} end - Indicates when the reservation ends
   */
  constructor(tick, end = 1) {
    super(`Reservation End ${end > 1 ? "x" + end : ""}`, "success", mdiAirplaneLanding, tick);
  }
}

export class FirstAllocationEvent extends FlightEvent {
  /**
   * @param {int} tick
   * @param {Coordinate3D} location
   * @param {string} explanation
   */
  constructor(tick, location, explanation) {
    super("First Allocation", "default", mdiSourceBranchCheck, tick, explanation);
    this.location = location;
  }
}

export class ReallocationEvent extends FlightEvent {
  /**
   * @param {int} tick
   * @param {Coordinate3D} location
   * @param {string} explanation
   */
  constructor(tick, location, explanation) {
    super("Reallocation", "warning", mdiSourceBranchSync, tick, explanation);
    this.location = location;
  }
}

export class FailedAllocationEvent extends FlightEvent {
  /**
   * @param {int} tick
   * @param {Coordinate3D} location
   * @param {string} explanation
   */
  constructor(tick, location, explanation) {
    super("Failed Allocation", "error", mdiSourceBranchRemove, tick, explanation);
    this.location = location;
  }
}

/**
 * Resolves a path reason to a flight event
 * @param {string} reason
 * @returns {FlightEvent}
 */
export function pathAllocationEventFactory(reason) {
  switch (reason) {
    case BRANCH_REASONS.FIRST_ALLOCATION:
      return FirstAllocationEvent;
    case BRANCH_REASONS.REALLOCATION:
      return ReallocationEvent;
    case BRANCH_REASONS.ALLOCATION_FAILED:
      return FailedAllocationEvent;
    default:
      console.error(`Unknown allocation reason: ${reason}`);
      throw new Error("Unknown allocation reason");
  }
}

/**
 * Resolves a space allocation reason to a flight event
 * @param {string} reason
 * @returns {FlightEvent}
 */
export function spaceAllocationEventFactory(reason) {
  switch (reason) {
    case BRANCH_REASONS.FIRST_ALLOCATION:
      return FirstReservationEvent;
    case BRANCH_REASONS.REALLOCATION:
      return ReReservationEvent;
    case BRANCH_REASONS.ALLOCATION_FAILED:
      return FailedReservationEvent;
    default:
      console.error(`Unknown allocation reason: ${reason}`);
      throw new Error("Unknown allocation reason");
  }
}

export default {
  FlightEvent,
  TakeOffEvent,
  ArrivalEvent,
  ReallocationEvent,
};
