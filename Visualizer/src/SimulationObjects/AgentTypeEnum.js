export default class AgentTypeEnum {

  static AB = new AgentTypeEnum("AB");
  static ABA = new AgentTypeEnum("ABA");
  static ABC = new AgentTypeEnum("ABC");
  static STATIONARY = new AgentTypeEnum("STATIONARY");

  constructor(name) {
    this.name = name;
  }

  /**
   * @param {String} name
   * @returns {AgentTypeEnum}
   */
  static fromString(name) {
    return AgentTypeEnum[name];
  }

  toString() {
    return `AgentType.${this.name}`;
  }
}
