import { computed, shallowRef, watch } from "vue";
import { useSimulationConfigStore } from "../../stores/simulationConfig";
import { fromLonLat } from "ol/proj";
import { boundingExtent } from "ol/extent";
import TileLayer from "ol/layer/Tile";
import OSM from "ol/source/OSM";
import { Feature, Map, View } from "ol";
import { Heatmap } from "ol/layer";
import VectorSource from "ol/source/Vector";
import VectorLayer from "ol/layer/Vector";
import { Point } from "ol/geom";

const HEATMAP_SCORE_PER_CLICK = 0.1;

export const useBaseLayer = () => {
  return new TileLayer({
    source: new OSM(),
    zIndex: 0,
  });
};

export const useHeatmapLayer = (features) => {
  return new Heatmap({
    source: new VectorSource({
      features,
    }),
  });
};

export const usePositionLayer = (features) => {
  return new VectorLayer({
    source: new VectorSource({
      features,
    }),
  });
};

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

export const restorePositionFeatures = (features, gridCoordinates) => {
  features.clear();
  gridCoordinates
    .map((coord) => {
      return new Feature(new Point([coord.lat, coord.long]));
    })
    .forEach((feat) => features.push(feat));
};

export const useMap = (mapRoot, layers) => {
  const simulationConfig = useSimulationConfigStore();

  const map = shallowRef(null);

  const topLeft = computed(() => {
    return fromLonLat([simulationConfig.map.topLeftCoordinate.long, simulationConfig.map.topLeftCoordinate.lat]);
  });
  const bottomRight = computed(() => {
    return fromLonLat([
      simulationConfig.map.bottomRightCoordinate.long,
      simulationConfig.map.bottomRightCoordinate.lat,
    ]);
  });
  const extent = computed(() => {
    return boundingExtent([topLeft.value, bottomRight.value]);
  });
  const min = computed(() => {
    return extent.value.slice(0, 2);
  });
  const max = computed(() => {
    return extent.value.slice(2, 4);
  });
  const dimensions = computed(() => {
    return [max.value[0] - min.value[0], max.value[1] - min.value[1]];
  });
  const meterCoordsRatio = computed(() => {
    return dimensions.value[0] / simulationConfig.dimension.x;
  });
  const center = computed(() => [
    (topLeft.value[0] + bottomRight.value[0]) / 2,
    (topLeft.value[1] + bottomRight.value[1]) / 2,
  ]);
  const zoom = computed(() => {
    return Math.floor(15 / Math.sqrt(simulationConfig.map.tiles.length));
  });

  const tileLayer = useBaseLayer();

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
    tileLayer,
    meterCoordsRatio,
    render,
  };
};

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
};
