import axios from "axios";

export default class MapTile {
  constructor(tile_ids, dimensions, topLeft, bottomRight) {
    this.x = tile_ids[1];
    this.y = tile_ids[2];
    this.z = tile_ids[0];
    this.top_left_coordinate = topLeft;
    this.bottom_right_coordinate = bottomRight;
    this.dimensions = dimensions;

    /**
     * @type {{height: number, coordinates: {x: number, y: number}}[]}
     */
    this.buildings = [];
  }

  get url() {
    return `https://data.osmbuildings.org/0.2/anonymous/tile/${this.z}/${this.x}/${this.y}.json`;
  }

  extractPolygon([long, lat]) {
    const x =
      ((lat - this.top_left_coordinate.lat) / (this.bottom_right_coordinate.lat - this.top_left_coordinate.lat)) *
        this.dimensions.x -
      this.dimensions.x / 2;
    const y =
      ((long - this.top_left_coordinate.long) / (this.bottom_right_coordinate.long - this.top_left_coordinate.long)) *
        this.dimensions.z -
      this.dimensions.z / 2;
    return { x, y };
  }

  async load() {
    const { data } = await axios.get(this.url);
    if (!data) {
      this.buildings = [];
      return;
    }
    this.buildings = data.features
      .filter((feature) => {
        const isFeature = feature?.type === "Feature";
        const hasHeight = feature?.properties?.height > 0;
        const isPolygon = feature?.geometry?.type === "Polygon";
        const hasCoordinates =
          feature?.geometry?.coordinates?.length > 0 && feature?.geometry?.coordinates[0].length > 0;
        return isFeature && hasHeight && isPolygon && hasCoordinates;
      })
      .map((feature) => {
        const height = feature.properties.height;
        const coordinatesArray = feature.geometry.coordinates[0].map(([long, lat]) => this.extractPolygon([long, lat]));
        const holesArray = feature.geometry.coordinates.slice(1).map((hole) => {
          return hole.map(([long, lat]) => this.extractPolygon([long, lat]));
        });
        const coordinates = coordinatesArray;
        return {
          height,
          coordinates,
          holes: holesArray,
        };
      });
  }
}
