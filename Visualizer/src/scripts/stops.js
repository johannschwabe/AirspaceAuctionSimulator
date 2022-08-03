import { Collection } from "ol";

export function createDefaultStop() {
  return {
    stop: {
      type: "random",
      position: {
        key: null,
        features: new Collection([]),
      },
      heatmap: {
        keys: {},
        features: new Collection([]),
      },
    },
  };
}

export function validStops(raw_positions, ownertype) {
  const res = {
    min: 1,
    max: undefined,
    start: ownertype === "PathOwner",
  };
  raw_positions
    .split(";")
    .map((cond) => cond.trim())
    .forEach((condition) => {
      if (condition.startsWith(">")) {
        res.min = parseInt(condition.substring(1)) + 1 - (res.start ? 2 : 0);
      } else if (condition.startsWith("<")) {
        res.max = parseInt(condition.substring(1)) - 1 - (res.start ? 2 : 0);
      } else {
        res.max = parseInt(condition) - (res.start ? 2 : 0);
        res.min = parseInt(condition) - (res.start ? 2 : 0);
      }
    });
  return res;
}
