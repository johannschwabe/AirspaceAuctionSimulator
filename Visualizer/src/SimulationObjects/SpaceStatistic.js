export default class SpaceStatistic {
  /**
   * @param {SpaceStatistics} spaceStatistic
   */
  constructor(spaceStatistic) {
    this.volume = spaceStatistic.volume;
    this.mean_volume = spaceStatistic.mean_volume;
    this.median_volume = spaceStatistic.median_volume;
    this.mean_height = spaceStatistic.mean_height;
    this.median_height = spaceStatistic.median_height;
    this.area = spaceStatistic.area;
    this.mean_area = spaceStatistic.mean_area;
    this.median_area = spaceStatistic.median_area;
    this.mean_time = spaceStatistic.mean_time;
    this.median_time = spaceStatistic.median_time;
    this.mean_height_above_ground = spaceStatistic.mean_height_above_ground;
    this.median_height_above_ground = spaceStatistic.median_height_above_ground;
  }
}
