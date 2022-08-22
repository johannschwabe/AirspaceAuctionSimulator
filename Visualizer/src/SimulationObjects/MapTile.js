import axios from "axios";
import { fromLonLat } from "ol/proj";

export default class MapTile {
  constructor(tile_ids, resolution, bottomLeft, topRight) {
    this.x = tile_ids[1];
    this.y = tile_ids[2];
    this.y = tile_ids[2];
    this.z = tile_ids[0];
    this.bottomLeft = bottomLeft;
    this.bottomLeftPM = fromLonLat([bottomLeft.long, bottomLeft.lat]);
    this.topRight = topRight;
    this.topRightPM = fromLonLat([topRight.long, topRight.lat]);
    this.resolution = resolution;
    /**
     * @type {{height: number, coordinates: {x: number, y: number}}[]}
     */
    this.buildings = [];
  }

  get url() {
    return `https://data.osmbuildings.org/0.2/anonymous/tile/${this.z}/${this.x}/${this.y}.json`;
  }

  extractPolygon(coords) {
    const dimLat = (this.topRightPM[1] - this.bottomLeftPM[1]) / this.resolution;
    const dimLong = (this.topRightPM[0] - this.bottomLeftPM[0]) / this.resolution;
    console.log(dimLong, dimLat);
    const coordPM = fromLonLat(coords);
    // let z = (coordPM[0] - this.bottomLeftPM[0]) / this.resolution;
    // let x = dimLat - (coordPM[1] - this.bottomLeftPM[1]) / this.resolution;
    // x -= dimLat / 2;
    // z -= dimLong / 2;
    let x = (coordPM[0] - this.bottomLeftPM[0]) / this.resolution;
    let z = (coordPM[1] - this.bottomLeftPM[1]) / this.resolution;
    x -= dimLong / 2;
    z -= dimLat / 2;
    return { x, z };
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
        const inSubselection = feature.geometry.coordinates[0].some(
          ([long, lat]) =>
            this.bottomLeft.long < long &&
            this.bottomLeft.lat < lat &&
            this.topRight.long > long &&
            this.topRight.lat > lat
        );
        return isFeature && hasHeight && isPolygon && hasCoordinates && inSubselection;
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
