import { mdiAirplaneLanding, mdiAirplaneTakeoff, mdiSourceBranch } from "@mdi/js";

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
  constructor(tick) {
    super("Reservation Start", "default", mdiAirplaneLanding, tick);
  }
}

export class ReservationEndEvent extends FlightEvent {
  constructor(tick) {
    super("Reservation End", "success", mdiAirplaneLanding, tick);
  }
}

export class ReallocationEvent extends FlightEvent {
  /**
   * @param {int} tick
   * @param {Coordinate3D} location
   * @param {ReasonEnum} reallocationReason
   */
  constructor(tick, location, reallocationReason) {
    super("Reallocation", "warning", mdiSourceBranch, tick, reallocationReason.name);
    this.location = location;
  }
}

export default {
  FlightEvent,
  TakeOffEvent,
  ArrivalEvent,
  ReallocationEvent,
};
