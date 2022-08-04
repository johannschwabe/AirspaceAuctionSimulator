import { defineStore } from "pinia";
import { createDefaultStop } from "../scripts/stops";
import { cloneDeep } from "lodash-es";

export const useConfigStore = defineStore({
  id: "config",
  state: () => ({
    name: "",
    description: "",
    mechanism: undefined,
    dimension: {
      x: 100,
      y: 20,
      z: 100,
      t: 1500,
    },
    map: {
      locationName: "",
      numberOfNeighbouringTiles: 0,
      tiles: [],
    },
    owners: [
      {
        color: "#00559d",
        name: "Digitec",
        agents: 20,
        type: "",
        locations: [],
      },
    ],
    availableMechanisms: {},
    availableOwnersForMechanism: [],
  }),
  getters: {
    asJson() {
      return {
        name: this.name,
        description: this.description,
        mechanism: this.mechanism,
        dimension: cloneDeep(this.dimension),
        map: {
          numberOfNeighbouringTiles: this.map.numberOfNeighbouringTiles,
          tiles: cloneDeep(this.map.tiles),
        },
        owners: cloneDeep(this.owners),
      };
    },
  },
  actions: {
    setMap(map) {
      this.map.locationName = map.locationName;
      this.map.numberOfNeighbouringTiles = map.numberOfNeighbouringTiles;
      this.map.tiles = map.tiles;
    },
    setDimension(dimension) {
      this.dimension.x = dimension.x;
      this.dimension.y = dimension.y;
      this.dimension.z = dimension.z;
    },
    overwrite(data) {
      this.name = data.name;
      this.description = data.description;
      this.mechanism = data.mechanism;
      this.setDimension(data.dimension);
      this.setMap(data.map);
      this.owners = [...data.owners];
    },
  },
});
