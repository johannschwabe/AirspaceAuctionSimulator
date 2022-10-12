import { round } from "lodash-es";

export default class BoxplotStatistics {
  /**
   * @param {FinanceStatistics} rawFinanceStatistics
   */
  constructor(rawFinanceStatistics) {
    this.values = rawFinanceStatistics.values;
    this.total = rawFinanceStatistics.total;
    this.mean = round(rawFinanceStatistics.mean, 2);
    this.median = round(rawFinanceStatistics.median, 2);
    this.min = round(rawFinanceStatistics.min, 2);
    this.max = round(rawFinanceStatistics.max, 2);
    this.quartiles = rawFinanceStatistics.quartiles.map((q) => round(q, 2));
    this.outliers = rawFinanceStatistics.outliers.map((q) => round(q, 2));
  }
}
