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

export function validStops(minLocations, maxLocations, ownerType) {
  const start = ownerType === "PathOwner";
  let min = minLocations;
  let max = maxLocations;
  if (start) {
    min -= 2;
    max -= 2;
  }
  return {
    min: min,
    max: max,
    start: start,
  };
}
