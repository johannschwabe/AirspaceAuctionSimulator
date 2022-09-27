import { computed, shallowRef, watch } from "vue";
import { useSimulationConfigStore } from "../../../stores/simulationConfigStore";
import { fromLonLat, toLonLat } from "ol/proj";
import { boundingExtent } from "ol/extent";
import TileLayer from "ol/layer/Tile";
import OSM from "ol/source/OSM";
import { Feature, Map, View } from "ol";
import { Heatmap } from "ol/layer";
import VectorSource from "ol/source/Vector";
import VectorLayer from "ol/layer/Vector";
import { Point } from "ol/geom";

import PointSelectionMap from "@/components/common/map/PointSelectionMap.vue";
import HeatmapMap from "@/components/common/map/HeatmapMap.vue";
import ViewOnlyMap from "@/components/common/map/ViewOnlyMap.vue";

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
 * @type {{random: ViewOnlyMap, heatmap: HeatmapMap, position: PointSelectionMap}}
 */
export const useComponentMappingWithRandomMap = () => {
  return {
    random: ViewOnlyMap,
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
 * @param {HeatmapConfig} points
 */
export const restoreHeatmapFeatures = (features, points) => {
  features.clear();
  points
    .map((coord) => {
      return new Feature(new Point(fromLonLat([coord.long, coord.lat])));
    })
    .flat()
    .forEach((feat) => features.push(feat));
};

/**
 * Restores positional features given a list of grid coordinates
 * @param {Collection} features
 * @param {WeightedCoordinate[]} coordinate
 */
export const restorePositionFeatures = (features, coordinate) => {
  features.clear();
  if (coordinate && coordinate.length > 0) {
    features.push(new Feature({ geometry: new Point(fromLonLat([coordinate[0].long, coordinate[0].lat])) }));
  }
};

/**
 * Setup of OpenLayer Map
 * @param {ref<HTMLInputElement | null>} mapRoot - HTML Element to mount OL to
 * @param {(TileLayer|VectorLayer|Heatmap)[]} layers - Layers to display
 * @param {boolean} subselection - Show full extent or just the subselection
 * @param {Number} width - width of map in pixels
 */
export const useMap = (mapRoot, layers, subselection = false, width = 400) => {
  const simulationConfig = useSimulationConfigStore();

  // Holds OL Map object
  const map = shallowRef(null);

  /**
   * Holds the extent of the visible map section
   * An extent is array of numbers representing an extent: `[minx, miny, maxx, maxy]
   * @type {ComputedRef<number[]>}
   */
  const extent = computed(() => {
    if (subselection && simulationConfig.map.subselection?.bottomLeft && simulationConfig.map.subselection?.topRight) {
      return boundingExtent([
        fromLonLat([
          simulationConfig.map.subselection.bottomLeft.long,
          simulationConfig.map.subselection.bottomLeft.lat,
        ]),
        fromLonLat([simulationConfig.map.subselection.topRight.long, simulationConfig.map.subselection.topRight.lat]),
      ]);
    }
    return boundingExtent([
      fromLonLat([simulationConfig.map.bottomLeftCoordinate.long, simulationConfig.map.bottomLeftCoordinate.lat]),
      fromLonLat([simulationConfig.map.topRightCoordinate.long, simulationConfig.map.topRightCoordinate.lat]),
    ]);
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
   * Holds the center of the visible map section in coordinate format
   * @type {ComputedRef<number[]>}
   */
  const center = computed(() => [(extent.value[0] + extent.value[2]) / 2, (extent.value[0] + extent.value[2]) / 2]);

  /**
   * Holds the zoom of the map
   * @type {ComputedRef<number>}
   */
  const zoom = computed(() => {
    return Math.floor(15 / (1 + 2 * simulationConfig.map.neighbouringTiles));
  });

  const size = computed(() => {
    const ratio = (max.value[0] - min.value[0]) / (max.value[1] - min.value[1]);
    return { width, height: width / ratio };
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
    extent,
    min,
    max,
    dimensions,
    center,
    zoom,
    render,
    size,
  };
};

/**
 * Registers interaction with the OL map with adding heatmap features on click and drag of the map
 * @param {ShallowRef<Map>} map
 * @param {Collection} features
 * @param {LocationConfig} location
 */
export const useHeatmapInteraction = (map, features, location) => {
  const onClickOrDrag = (event) => {
    const coords = event.coordinate;
    const [long, lat] = toLonLat(coords);

    let fittingEntry = location.points.find((coord) => coord.long === long && coord.lat === lat);
    if (!fittingEntry) {
      const newLocation = { lat, long, value: 0.0 };
      location.points.push(newLocation);
      fittingEntry = newLocation;
    }
    fittingEntry.value = Math.min(fittingEntry.value + HEATMAP_SCORE_PER_CLICK, 1.0);
    if (fittingEntry.value <= 1.0) {
      features.push(new Feature(new Point(coords)));
    }
  };
  map.value.on("click", onClickOrDrag);
  map.value.on("pointerdrag", onClickOrDrag);
};

/**
 * Registers interaction with the OL map with adding position features on click of the map
 * @param {ShallowRef<Map>} map
 * @param {Collection} features
 * @param {LocationConfig} location
 */
export const usePositionInteraction = (map, features, location) => {
  const onClickOrDrag = (event) => {
    const coords = event.coordinate;
    const [long, lat] = toLonLat(coords);
    location.points = [{ lat, long, value: 1.0 }];
    features.pop();
    features.push(new Feature(new Point(coords)));
  };

  map.value.on("click", onClickOrDrag);
  map.value.on("pointerdrag", onClickOrDrag);
};
