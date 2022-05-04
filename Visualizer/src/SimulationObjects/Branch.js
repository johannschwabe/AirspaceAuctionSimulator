import Path from "./Path";
import Collision from "./Collision";

export default class Branch {
  /**
   *
   * @param {RawBranch} rawBranch
   */
  constructor(rawBranch) {
    this.tick = rawBranch.tick;
    this.paths = rawBranch.paths.map((path) => new Path(path));
    this.value = rawBranch.value;
    this.collision = new Collision(rawBranch.reason);
  }
}
