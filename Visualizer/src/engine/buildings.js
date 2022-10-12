import { Vector3 } from "@babylonjs/core/Maths/math";
import { ExtrudePolygon } from "@babylonjs/core/Meshes/Builders";
import earcut from "earcut";

/**
 * Generates buildings from maptile information
 * @param {Object} args
 * @param {Scene} args.scene
 * @param {ShadowGenerator} args.shadows
 * @param {MapTile[]} args.mapTiles
 * @param {StandardMaterial} args.blockerMaterial
 */
export function useBuildings({ scene, shadows, mapTiles, blockerMaterial }) {
  mapTiles.forEach((mapTile, i) => {
    mapTile.buildings.forEach((building, j) => {
      const options = {
        shape: building.coordinates.map(({ x, z }) => new Vector3(x, 0, z)).reverse(),
        depth: building.height,
        holes: building.holes.map((hole) => hole.map(({ x, z }) => new Vector3(x, 0, z))).reverse(),
      };
      const buildingMesh = ExtrudePolygon(`tile-${i}-building-${j}`, options, scene, earcut);
      buildingMesh.material = blockerMaterial;
      buildingMesh.receiveShadows = true;
      buildingMesh.position.y = building.height;
      shadows.getShadowMap().renderList.push(buildingMesh);
    });
  });
}
