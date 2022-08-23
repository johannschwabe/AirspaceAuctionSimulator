import axios from "axios";
import { fromLonLat } from "ol/proj";

const EARTH_RADIUS = 6371008.8;

export default class MapTile {
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
    /**
     * @type {{height: number, coordinates: {x: number, y: number}}[]}
     */
    this.buildings = [];
  }

  get url() {
    return `https://data.osmbuildings.org/0.2/anonymous/tile/${this.z}/${this.x}/${this.y}.json`;
  }

  radian(degrees) {
    return (degrees * Math.PI) / 180;
  }

  haversin_lon_lat(pos) {
    let x =
      (2 *
        EARTH_RADIUS *
        Math.asin(
          Math.sqrt(
            Math.cos(this.radian(this.bottomLeft.lat)) *
              Math.cos(this.radian(pos.lat)) *
              Math.sin(this.radian(pos.long - this.bottomLeft.long) / 2) ** 2
          )
        )) /
      this.resolution;
    let z =
      (2 * EARTH_RADIUS * Math.asin(Math.sqrt(Math.sin(this.radian((pos.lat - this.bottomLeft.lat) / 2)) ** 2))) /
      this.resolution;

    if (pos.long < this.bottomLeft.long) {
      x *= -1;
    }
    if (pos.lat < this.bottomLeft.lat) {
      z *= -1;
    }
    return { x, z };
  }

  extractPolygon(coords) {
    let { x, z } = this.haversin_lon_lat({ long: coords[0], lat: coords[1] });

    x -= this.dimX / 2;
    z -= this.dimZ / 2;
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
