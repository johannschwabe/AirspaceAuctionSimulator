import { Collection } from "ol";

export function createDefaultStop() {
  return {
    type: "random",
    position: {
      key: null,
      features: new Collection([]),
    },
    heatmap: {
      keys: {},
      features: new Collection([]),
    },
  };
}
