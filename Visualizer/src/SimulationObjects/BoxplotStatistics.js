import { round } from "lodash-es";

export default class BoxplotStatistics {
  /**
   * @param {FinanceStatistics} rawFinanceStatistics
   */
  constructor(rawFinanceStatistics) {
    this.values = rawFinanceStatistics.values;
    this.total = rawFinanceStatistics.total;
    this.mean = round(rawFinanceStatistics.mean);
    this.median = round(rawFinanceStatistics.median);
    this.min = round(rawFinanceStatistics.min);
    this.max = round(rawFinanceStatistics.max);
    this.quartiles = rawFinanceStatistics.quartiles.map((q) => round(q, 2));
    this.outliers = rawFinanceStatistics.outliers.map((q) => round(q, 2));
  }
}
