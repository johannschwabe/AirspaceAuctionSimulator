import axios from "axios";

export default class MapTile {
  /**
   * @param {RawMapTile} rawMapTile
   */
  constructor(rawMapTile) {
    this.x = rawMapTile.x;
    this.y = rawMapTile.y;
    this.z = rawMapTile.z;
    this.top_left_coordinate = rawMapTile.top_left_coordiante;
    this.bottom_right_coordinate = rawMapTile.bottom_right_coordiante;
    this.dimensions = rawMapTile.dimensions;

    /**
     * @type {*[]}
     */
    this.buildings = [];
  }

  get url() {
    return `https://data.osmbuildings.org/0.2/anonymous/tile/${this.z}/${this.x}/${this.y}.json`;
  }

  async load() {
    const { data } = axios.get(this.url);
    this.buildings = data.features
      .filter((feature) => {
        const isFeature = feature?.type === "Feature";
        const hasHeight = feature?.properties?.height > 0;
        const isPolygon = feature?.geometry?.type === "Polygon";
        const hasCoordinates = feature?.geometry?.coordinates?.length > 0;
        return isFeature && hasHeight && isPolygon && hasCoordinates;
      })
      .map((feature) => {
        const height = feature.properties.height;
        const coordinates = feature.geometry.coordinates.map(([long, lat]) => {
          const x =
            ((long - this.top_left_coordinate.long) /
              (this.bottom_right_coordinate.long - this.top_left_coordinate.long)) *
            this.dimensions.x;
          const z =
            ((lat - this.top_left_coordinate.lat) / (this.bottom_right_coordinate.lat - this.top_left_coordinate.lat)) *
            this.dimensions.z;
          return { x, y: 0, z };
        });
        return {
          height,
          coordinates,
        };
      });
  }
}
