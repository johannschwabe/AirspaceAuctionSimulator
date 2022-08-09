import { computed, shallowRef, watch } from "vue";
import { useSimulationConfigStore } from "../../stores/simulationConfig";
import { fromLonLat } from "ol/proj";
import { boundingExtent } from "ol/extent";
import TileLayer from "ol/layer/Tile";
import OSM from "ol/source/OSM";
import { Feature, Map, View } from "ol";
import { onMounted } from "vue";
import { Heatmap } from "ol/layer";
import VectorSource from "ol/source/Vector";
import VectorLayer from "ol/layer/Vector";
import { Point } from "ol/geom";

export const useBaseLayer = () => {
  return new TileLayer({
    source: new OSM(),
    zIndex: 0,
  });
};

export const useHeatmapLayer = (heatmap) => {
  return new Heatmap({
    source: new VectorSource({
      features: heatmap.features,
    }),
  });
};

export const usePositionLayer = (position) => {
  return new VectorLayer({
    source: new VectorSource({
      features: position.features,
    }),
  });
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

export const useHeatmapInteraction = (map, min, meterCoordsRatio, heatmap) => {
  const simulationConfig = useSimulationConfigStore();

  const emit = defineEmits(["update:heatmap"]);

  const onClickOrDrag = (event) => {
    const coords = event.coordinate;
    const gridCoords = [
      Math.floor((coords[0] - min.value[0]) / meterCoordsRatio.value),
      Math.floor((coords[1] - min.value[1]) / meterCoordsRatio.value),
    ];
    if (
      gridCoords[0] >= 0 &&
      gridCoords[1] >= 0 &&
      gridCoords[1] < simulationConfig.dimension.x &&
      gridCoords[0] < simulationConfig.dimension.z
    ) {
      // Inverted x coordinate
      const key = `${simulationConfig.dimension.x - gridCoords[1]}_${gridCoords[0]}`;
      if (heatmap.keys[key] !== undefined) {
        if (heatmap.keys[key] === 0) {
          heatmap.keys[key] = Math.round(heatmap.keys[key] * 10 + 1) / 10;
        }
      } else {
        heatmap.keys[key] = 0.1;
      }
      heatmap.features.push(new Feature(new Point(coords)));
      emit("update:heatmap", heatmap);
    }
  };

  map.on("click", onClickOrDrag);
  map.on("pointerdrag", onClickOrDrag);
};

export const usePositionInteraction = (map, min, meterCoordsRatio, position) => {
  const simulationConfig = useSimulationConfigStore();
  const emit = defineEmits(["update:position"]);

  const onClickOrDrag = (event) => {
    const coords = event.coordinate;
    const gridCoords = [
      Math.floor((coords[0] - min.value[0]) / meterCoordsRatio.value),
      Math.floor((coords[1] - min.value[1]) / meterCoordsRatio.value),
    ];
    if (
      gridCoords[0] >= 0 &&
      gridCoords[1] >= 0 &&
      gridCoords[1] < simulationConfig.dimension.x &&
      gridCoords[0] < simulationConfig.dimension.z
    ) {
      // Inverted x coordinate
      const key = `${simulationConfig.dimension.x - gridCoords[1]}_${gridCoords[0]}`;
      position.key = key;
      position.features.pop();
      position.features.push(new Feature(new Point(coords)));
      emit("update:position", position);
    }
  };

  map.on("click", onClickOrDrag);
  map.on("pointerdrag", onClickOrDrag);
};
