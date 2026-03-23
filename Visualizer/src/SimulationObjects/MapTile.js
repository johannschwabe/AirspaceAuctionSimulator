import axios from "axios";

const EARTH_RADIUS = 6371008.8;
const OVERPASS_URL = "https://overpass-api.de/api/interpreter";
const DEFAULT_BUILDING_HEIGHT_M = 10;
const METERS_PER_LEVEL = 3;

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
   * Returns the Overpass QL query to fetch buildings within this tile's bounding box.
   * Fetches both ways (simple buildings) and multipolygon relations (buildings with holes).
   * @returns {string}
   */
  get overpassQuery() {
    const s = this.bottomLeft.lat;
    const w = this.bottomLeft.long;
    const n = this.topRight.lat;
    const e = this.topRight.long;
    return `[out:json][timeout:30];(way["building"](${s},${w},${n},${e});relation["building"]["type"="multipolygon"](${s},${w},${n},${e}););out geom;`;
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
   * Parses building height in meters from OSM tags.
   * Falls back to building:levels * METERS_PER_LEVEL, then DEFAULT_BUILDING_HEIGHT_M.
   * @param {Object} tags
   * @returns {number} height in meters
   */
  _parseHeightMeters(tags) {
    if (tags.height) {
      const h = parseFloat(tags.height);
      if (!isNaN(h) && h > 0) return h;
    }
    if (tags["building:levels"]) {
      const levels = parseFloat(tags["building:levels"]);
      if (!isNaN(levels) && levels > 0) return levels * METERS_PER_LEVEL;
    }
    return DEFAULT_BUILDING_HEIGHT_M;
  }

  /**
   * Converts an Overpass geometry array [{lat, lon}] to simulation grid coordinates.
   * @param {{lat: number, lon: number}[]} geom
   * @returns {{x: number, z: number}[]}
   */
  _geomToGrid(geom) {
    return geom
      .filter((pt) => pt.lat !== undefined && pt.lon !== undefined)
      .map((pt) => this.extractPolygon([pt.lon, pt.lat]));
  }

  /**
   * Parses a simple OSM way element into a building object.
   * @param {Object} element
   * @returns {{height: number, coordinates: {x,z}[], holes: {x,z}[][]} | null}
   */
  _parseWay(element) {
    if (!element.geometry || element.geometry.length < 3) return null;
    const tags = element.tags || {};
    const height = this._parseHeightMeters(tags) / this.resolution;
    const coordinates = this._geomToGrid(element.geometry);
    if (coordinates.length < 3) return null;
    return { height, coordinates, holes: [] };
  }

  /**
   * Parses a multipolygon relation element into a building object.
   * Members with role "outer" form the exterior ring; "inner" members form holes.
   * @param {Object} element
   * @returns {{height: number, coordinates: {x,z}[], holes: {x,z}[][]} | null}
   */
  _parseRelation(element) {
    if (!element.members) return null;
    const tags = element.tags || {};
    const height = this._parseHeightMeters(tags) / this.resolution;

    const outers = element.members.filter((m) => m.role === "outer" && m.geometry?.length >= 3);
    const inners = element.members.filter((m) => m.role === "inner" && m.geometry?.length >= 3);

    if (outers.length === 0) return null;

    // Use first outer ring as the building footprint
    const coordinates = this._geomToGrid(outers[0].geometry);
    const holes = inners.map((m) => this._geomToGrid(m.geometry)).filter((h) => h.length >= 3);

    if (coordinates.length < 3) return null;
    return { height, coordinates, holes };
  }

  /**
   * Fetches building data from the Overpass API and populates this.buildings.
   * @returns {Promise<void>}
   */
  async load() {
    let data;
    try {
      const { data: responseData } = await axios.post(
        OVERPASS_URL,
        `data=${encodeURIComponent(this.overpassQuery)}`,
        { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
      );
      data = responseData;
    } catch (e) {
      this.buildings = [];
      return;
    }

    if (!data?.elements) {
      this.buildings = [];
      return;
    }

    this.buildings = data.elements
      .map((element) => {
        if (element.type === "way") return this._parseWay(element);
        if (element.type === "relation") return this._parseRelation(element);
        return null;
      })
      .filter(Boolean);
  }
}
