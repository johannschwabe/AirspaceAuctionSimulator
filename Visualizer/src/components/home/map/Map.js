import { computed, shallowRef, watch } from "vue";
import { useSimulationConfigStore } from "../../../stores/simulationConfig";
import { fromLonLat } from "ol/proj";
import { boundingExtent } from "ol/extent";
import TileLayer from "ol/layer/Tile";
import OSM from "ol/source/OSM";
import { Feature, Map, View } from "ol";
import { Heatmap } from "ol/layer";
import VectorSource from "ol/source/Vector";
import VectorLayer from "ol/layer/Vector";
import { Point } from "ol/geom";

import PointSelectionMap from "@/components/home/map/PointSelectionMap.vue";
import HeatmapMap from "@/components/home/map/HeatmapMap.vue";

const HEATMAP_SCORE_PER_CLICK = 0.1;

/**
 * @type {{random: string, heatmap: HeatmapMap, position: PointSelectionMap}}
 */
export const useComponentMapping = () => {
  return {
    random: "span",
    position: PointSelectionMap,
    heatmap: HeatmapMap,
  };
};

/**
 * Base layer showing regular Map Texture
 * @returns {TileLayer<TileSourceType>}
 */
export const useBaseLayer = () => {
  return new TileLayer({
    source: new OSM(),
    zIndex: 0,
  });
};

/**
 * Heatmap Layer
 * @param {Collection} features - OL Collection storing Heatmap data
 * @returns {Heatmap}
 */
export const useHeatmapLayer = (features) => {
  return new Heatmap({
    source: new VectorSource({
      features,
    }),
  });
};

/**
 * Position Layer
 * @param {Collection} features - OL Collection storing Positional data
 * @returns {VectorLayer<VectorSourceType>}
 */
export const usePositionLayer = (features) => {
  return new VectorLayer({
    source: new VectorSource({
      features,
    }),
  });
};

/**
 * Restores heatmap features given a list of grid coordinates
 * @param {Collection} features
 * @param {GridCoordinateConfig[]} gridCoordinates
 */
export const restoreHeatmapFeatures = (features, gridCoordinates) => {
  features.clear();
  gridCoordinates
    .map((coord) => {
      return Array.from({ length: Math.round(coord.value / HEATMAP_SCORE_PER_CLICK) }).map(
        () => new Feature(new Point([coord.lat, coord.long]))
      );
    })
    .flat()
    .forEach((feat) => features.push(feat));
};

/**
 * Restores positional features given a list of grid coordinates
 * @param {Collection} features
 * @param {GridCoordinateConfig[]} gridCoordinates
 */
export const restorePositionFeatures = (features, gridCoordinates) => {
  features.clear();
  gridCoordinates
    .map((coord) => {
      return new Feature(new Point([coord.lat, coord.long]));
    })
    .forEach((feat) => features.push(feat));
};

/**
 * Setup of OpenLayer Map
 * @param {ref<HTMLInputElement | null>} mapRoot - HTML Element to mount OL to
 * @param {(TileLayer|VectorLayer|Heatmap)[]} layers - Layers to display
 */
export const useMap = (mapRoot, layers) => {
  const simulationConfig = useSimulationConfigStore();

  // Holds OL Map object
  const map = shallowRef(null);

  /**
   * Holds the coordinate at the top-left of the map
   * @type {ComputedRef<number[]>}
   */
  const topLeft = computed(() => {
    return fromLonLat([simulationConfig.map.topLeftCoordinate.long, simulationConfig.map.topLeftCoordinate.lat]);
  });

  /**
   * Holds the coordinate at the bottom-right of the map
   * @type {ComputedRef<number[]>}
   */
  const bottomRight = computed(() => {
    return fromLonLat([
      simulationConfig.map.bottomRightCoordinate.long,
      simulationConfig.map.bottomRightCoordinate.lat,
    ]);
  });

  /**
   * Holds the extent of the visible map section
   * An extent is array of numbers representing an extent: `[minx, miny, maxx, maxy]
   * @type {ComputedRef<number[]>}
   */
  const extent = computed(() => {
    return boundingExtent([topLeft.value, bottomRight.value]);
  });

  /**
   * Holds the minimum coordinate of the map extent [minx, miny]
   * @type {ComputedRef<number[]>}
   */
  const min = computed(() => {
    return extent.value.slice(0, 2);
  });

  /**
   * Holds the maximum coordinate of the map extent [maxx, maxy]
   * @type {ComputedRef<number[]>}
   */
  const max = computed(() => {
    return extent.value.slice(2, 4);
  });

  /**
   * Holds the dimensions of the visible map section in coordinate format
   * @type {ComputedRef<number[]>}
   */
  const dimensions = computed(() => {
    return [max.value[0] - min.value[0], max.value[1] - min.value[1]];
  });

  /**
   * Indicates how many meters there are per simulation config unit
   * @type {ComputedRef<number>}
   */
  const meterCoordsRatio = computed(() => {
    return dimensions.value[0] / simulationConfig.dimension.x;
  });

  /**
   * Holds the center of the visible map section in coordinate format
   * @type {ComputedRef<number[]>}
   */
  const center = computed(() => [
    (topLeft.value[0] + bottomRight.value[0]) / 2,
    (topLeft.value[1] + bottomRight.value[1]) / 2,
  ]);

  /**
   * Holds the zoom of the map
   * @type {ComputedRef<number>}
   */
  const zoom = computed(() => {
    return Math.floor(15 / Math.sqrt(simulationConfig.map.tiles.length));
  });

  watch(extent, () => {
    if (map.value !== null) {
      map.value.setView(
        new View({
          zoom: zoom.value,
          center: center.value,
          extent: extent.value,
          showFullExtent: true,
        })
      );
    }
  });

  /**
   * Function that mounts the OL Map to the provided HTML element.
   * This method should be called onMount
   */
  const render = () => {
    map.value = new Map({
      // the map will be created using the 'map-root' ref
      layers,
      target: mapRoot.value,
      controls: [],
      interactions: [],

      // the map view only shows the selected tiles
      view: new View({
        zoom: zoom.value,
        center: center.value,
        extent: extent.value,
        showFullExtent: true,
      }),
    });
  };

  return {
    map,
    topLeft,
    bottomRight,
    extent,
    min,
    max,
    dimensions,
    center,
    zoom,
    meterCoordsRatio,
    render,
  };
};

/**
 * Registers interaction with the OL map with adding heatmap features on click and drag of the map
 * @param {ShallowRef<Map>} map
 * @param {ComputedRef<number[]>} min
 * @param {ComputedRef<number>} meterCoordsRatio
 * @param {Collection} features
 * @param {LocationConfig} location
 */
export const useHeatmapInteraction = (map, min, meterCoordsRatio, features, location) => {
  const simulationConfig = useSimulationConfigStore();

  const onClickOrDrag = (event) => {
    const coords = event.coordinate;
    const [lat, long] = coords;
    const gridCoords = [
      Math.floor((lat - min.value[0]) / meterCoordsRatio.value),
      Math.floor((long - min.value[1]) / meterCoordsRatio.value),
    ];
    if (
      gridCoords[0] >= 0 &&
      gridCoords[1] >= 0 &&
      gridCoords[1] < simulationConfig.dimension.x &&
      gridCoords[0] < simulationConfig.dimension.z
    ) {
      // Inverted x coordinate
      const [x, y] = [simulationConfig.dimension.x - gridCoords[1], gridCoords[0]];
      let fittingEntry = location.gridCoordinates.find((coord) => coord.x === x && coord.y === y);
      if (!fittingEntry) {
        const newLocation = { x, y, lat, long, value: 0.0 };
        location.gridCoordinates.push(newLocation);
        fittingEntry = newLocation;
      }
      fittingEntry.value = Math.min(fittingEntry.value + HEATMAP_SCORE_PER_CLICK, 1.0);
      if (fittingEntry.value <= 1.0) {
        features.push(new Feature(new Point(coords)));
      }
    }
  };
  map.value.on("click", onClickOrDrag);
  map.value.on("pointerdrag", onClickOrDrag);
};

/**
 * Registers interaction with the OL map with adding position features on click of the map
 * @param {ShallowRef<Map>} map
 * @param {ComputedRef<number[]>} min
 * @param {ComputedRef<number>} meterCoordsRatio
 * @param {Collection} features
 * @param {LocationConfig} location
 */
export const usePositionInteraction = (map, min, meterCoordsRatio, features, location) => {
  const simulationConfig = useSimulationConfigStore();

  const onClickOrDrag = (event) => {
    const coords = event.coordinate;
    const [lat, long] = coords;
    const gridCoords = [
      Math.floor((lat - min.value[0]) / meterCoordsRatio.value),
      Math.floor((long - min.value[1]) / meterCoordsRatio.value),
    ];
    if (
      gridCoords[0] >= 0 &&
      gridCoords[1] >= 0 &&
      gridCoords[1] < simulationConfig.dimension.x &&
      gridCoords[0] < simulationConfig.dimension.z
    ) {
      // Inverted x coordinate
      const [x, y] = [simulationConfig.dimension.x - gridCoords[1], gridCoords[0]];
      location.gridCoordinates = [{ x, y, lat, long, value: 1 }];
      features.pop();
      features.push(new Feature(new Point(coords)));
    }
  };

  map.value.on("click", onClickOrDrag);
  map.value.on("pointerdrag", onClickOrDrag);
};
