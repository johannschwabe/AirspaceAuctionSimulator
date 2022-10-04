import axios from "axios";

const EARTH_RADIUS = 6371008.8;

export default class MapTile {
  /**
   * @param {[int, int, int]} tile_ids
   * @param {int} resolution
   * @param {{long: float, lat: float}} bottomLeft
   * @param {{long: float, lat: float}} topRight
   */
  constructor(tile_ids, resolution, bottomLeft, topRight) {
    this.x = tile_ids[1];
    this.y = tile_ids[2];
    this.z = tile_ids[0];
    this.bottomLeft = bottomLeft;
    this.topRight = topRight;
    this.resolution = resolution;
    const { x, z } = this.haversin_lon_lat(this.topRight);
    this.dimZ = z;
    this.dimX = x;
    this.buildings = [];
  }

  /**
   * Returns URL needed to request building information from open street maps for current tile
   * @returns {string}
   */
  get url() {
    return `https://data.osmbuildings.org/0.2/anonymous/tile/${this.z}/${this.x}/${this.y}.json`;
  }

  /**
   * Converts degrees to radian
   * @param {number} degrees
   * @returns {number}
   */
  radian(degrees) {
    return (degrees * Math.PI) / 180;
  }

  /**
   * Converts a longitude-latitude coordinate to AAS Grid Coordinates
   * @param {{long: number, lat: number}} position
   * @returns {{x: number, z: number}}
   */
  haversin_lon_lat(position) {
    let x =
      (2 *
        EARTH_RADIUS *
        Math.asin(
          Math.sqrt(
            Math.cos(this.radian(this.bottomLeft.lat)) *
              Math.cos(this.radian(position.lat)) *
              Math.sin(this.radian(position.long - this.bottomLeft.long) / 2) ** 2
          )
        )) /
      this.resolution;
    let z =
      (2 * EARTH_RADIUS * Math.asin(Math.sqrt(Math.sin(this.radian((position.lat - this.bottomLeft.lat) / 2)) ** 2))) /
      this.resolution;

    if (position.long < this.bottomLeft.long) {
      x *= -1;
    }
    if (position.lat < this.bottomLeft.lat) {
      z *= -1;
    }
    return { x, z };
  }

  /**
   * Converts the building polygon to a building grid location
   * @param {[number, number]} position
   * @returns {{x: undefined, z: undefined}}
   */
  extractPolygon(position) {
    let { x, z } = this.haversin_lon_lat({ long: position[0], lat: position[1] });

    x -= this.dimX / 2;
    z -= this.dimZ / 2;
    return { x, z };
  }

  /**
   * Lodas OSM Building information and extracts building information as height, coordiantes and holes
   * @returns {Promise<void>}
   */
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
        const height = feature.properties.height / this.resolution;
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
