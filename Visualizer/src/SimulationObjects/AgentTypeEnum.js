export default class AgentTypeEnum {

  static AB = new AgentTypeEnum("ABAgent");
  static ABA = new AgentTypeEnum("ABAAgent");
  static ABC = new AgentTypeEnum("ABCAgent");
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
