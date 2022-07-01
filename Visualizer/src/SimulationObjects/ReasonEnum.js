export default class ReasonEnum {
  static FIRST_ALLOCATION = new ReasonEnum("FIRST_ALLOCATION");
  static AGENT = new ReasonEnum("AGENT");
  static BLOCKER = new ReasonEnum("BLOCKER");
  static OWNER = new ReasonEnum("OWNER");
  static NOT_IMPLEMENTED = new ReasonEnum("NOT_IMPLEMENTED");
  static ALLOCATION_FAILED = new ReasonEnum("ALLOCATION_FAILED");
  constructor(name) {
    this.name = name;
  }

  toString() {
    return `Reason.${this.name}`;
  }

  /**
   * @param {String} name
   * @returns {ReasonEnum}
   */
  static fromString(name) {
    return ReasonEnum[name];
  }
}
