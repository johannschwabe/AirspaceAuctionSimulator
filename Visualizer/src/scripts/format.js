import { format, set } from "date-fns";

export function formatComputeTime(compute_time_ns) {
  const milliseconds = compute_time_ns / 1e6;
  const date = set(new Date(), {
    year: 0,
    month: 0,
    date: 0,
    hours: 0,
    minutes: 0,
    seconds: 0,
    milliseconds,
  });
  if (compute_time_ns < 1000) {
    return `${compute_time_ns} ns`;
  }
  if (milliseconds < 1000) {
    return `${milliseconds} ms`;
  }
  if (milliseconds < 60 * 1000) {
    return `${format(date, "s")}s`;
  }
  if (milliseconds < 60 * 60 * 1000) {
    return `${format(date, "m")}min ${format(date, "ss")}s`;
  }
  return `${format(date, "H")}h ${format(date, "mm")}min ${format(date, "ss")}s`;
}
