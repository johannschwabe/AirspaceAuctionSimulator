export default class PathStatistic {
  /**
   * @param {PathStatistics} pathStatistic
   */
  constructor(pathStatistic) {
    this.distanceL1 = pathStatistic.l1_distance;
    this.distanceL2 = pathStatistic.l2_distance;
    this.distanceTraveled = pathStatistic.distance_traveled;
    this.groundDistanceL1 = pathStatistic.l1_ground_distance;
    this.groundDistanceL2 = pathStatistic.l2_ground_distance;
    this.groundDistanceTraveled = pathStatistic.ground_distance_traveled;
    this.heightDifference = pathStatistic.height_difference;
    this.timeDifference = pathStatistic.time_difference;
    this.ascent = pathStatistic.ascent;
    this.descent = pathStatistic.descent;
    this.meanHeight = pathStatistic.mean_height;
    this.medianHeight = pathStatistic.median_height;
    this.heightProfile = pathStatistic.heights;
  }
}
