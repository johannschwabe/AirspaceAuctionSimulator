export default class ReasonEnum {

  static AGENT = new ReasonEnum("AGENT");
  static BLOCKER = new ReasonEnum("BLOCKER");
  static OWNER = new ReasonEnum("OWNER");
  static NOT_IMPLEMENTED = new ReasonEnum("NOT_IMPLEMENTED");

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
