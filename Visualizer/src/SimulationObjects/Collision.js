import ReasonEnum from "./ReasonEnum";

export default class Collision {
  /**
   * @param {RawCollision} rawCollision
   */
  constructor(rawCollision) {
    this.reason = ReasonEnum.fromString(rawCollision.reason.reason);
    this.agentId = rawCollision.agent_id;
    this.blockerId = rawCollision.blocker_id;
  }
}
