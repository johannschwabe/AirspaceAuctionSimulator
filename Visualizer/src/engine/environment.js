import { DirectionalLight, HemisphericLight } from "@babylonjs/core/Lights";
import { Color3, Vector3 } from "@babylonjs/core/Maths/math";
import { HEMISPHERE_LIGHT_INTENSITY, MAIN_LIGHT_INTENSITY } from "@/engine/constants";
import { CreateGround, CreateLines } from "@babylonjs/core/Meshes/Builders";
import { StandardMaterial } from "@babylonjs/core/Materials/standardMaterial";
import { AxesViewer } from "@babylonjs/core/Debug/axesViewer";
import { ShadowGenerator } from "@babylonjs/core/Lights/Shadows/shadowGenerator";

/**
 * Creates a directional light to illuminate the scene
 * @param {Object} args
 * @param {Scene} args.scene
 * @param {number} args.x - x dimension of playing field
 * @param {number} args.y - y dimension of playing field
 * @param {number} args.z - z dimension of playing field
 * @returns {DirectionalLight}
 */
export function useMainLight({ scene, x, y, z }) {
  const mainLight = new DirectionalLight("directionalLight", new Vector3(-1, -1, -1), scene);
  mainLight.diffuse = Color3.FromHexString("#ffffff");
  mainLight.specular = Color3.FromHexString("#63e2b7");
  mainLight.groundColor = Color3.FromHexString("#44ab87");
  mainLight.intensity = MAIN_LIGHT_INTENSITY;
  mainLight.position.x = x / 2;
  mainLight.position.y = y / 2;
  mainLight.position.z = z / 2;
  return mainLight;
}

/**
 * Creates a hemisphere light to illuminate the scene
 * @param {Object} args
 * @param {Scene} args.scene
 * @returns {HemisphericLight}
 */
export function useHemisphereLight({ scene }) {
  const hemisphereLight = new HemisphericLight("HemiLight", new Vector3(0, 1, 0), scene);
  hemisphereLight.intensity = HEMISPHERE_LIGHT_INTENSITY;
  return hemisphereLight;
}

/**
 * Creates thee axis arrows at the origin of the scene as indicators of the x-y-z axis directions
 * @param {Object} args
 * @param {Scene} args.scene
 * @param {number} args.x - x dimension of playing field
 * @param {number} args.y - y dimension of playing field
 * @param {number} args.z - z dimension of playing field
 * @returns {AxesViewer}
 */
export function useAxisIndicators({ scene, x, y, z }) {
  const lengthOfAxis = Math.max(x, y, z) / 10;
  const axes = new AxesViewer(scene, lengthOfAxis);
  axes.update(new Vector3(-x / 2, 0, -z / 2), new Vector3(1, 0, 0), new Vector3(0, 1, 0), new Vector3(0, 0, 1));
  return axes;
}

/**
 * Creates a shadow map that auto-updates with new drones
 * @param {Object} args
 * @param {DirectionalLight} args.mainLight
 * @returns {ShadowGenerator}
 */
export function useShadows({ mainLight }) {
  const shadows = new ShadowGenerator(2048, mainLight);
  shadows.usePoissonSampling = true;
  shadows.getShadowMap().refreshRate = 3;
  mainLight.autoUpdateExtends = false;
  return shadows;
}

/**
 * Creates a planar ground that is transparent when viewed from the bottom
 * @param {Object} args
 * @param {Scene} args.scene
 * @param {number} args.x - x dimension of playing field
 * @param {number} args.z - z dimension of playing field
 * @returns {GroundMesh}
 */
export function useGround({ scene, x, z }) {
  const ground = CreateGround("ground", { width: x, height: z });
  const groundMaterial = new StandardMaterial("ground-material", scene);
  groundMaterial.diffuseColor = Color3.FromHexString("#101010");
  groundMaterial.specularColor = Color3.FromHexString("#2b2b2c");
  groundMaterial.alpha = 1;
  ground.material = groundMaterial;
  ground.receiveShadows = true;
  return ground;
}

/**
 * Creates boundary lines around field to make borders more visible
 * @param {Object} args
 * @param {number} args.lineAlpha
 * @param {number} args.x - x dimension of playing field
 * @param {number} args.y - y dimension of playing field
 * @param {number} args.z - z dimension of playing field
 */
export function useOrientationLines({ lineAlpha, x, y, z }) {
  const stepX = Math.floor(x);
  const stepY = Math.floor(y / 10);
  const stepZ = Math.floor(z);

  for (let xi = 0; xi <= x; xi += stepX) {
    for (let yi = 0; yi <= y; yi += stepY) {
      const line = CreateLines(`line-x${xi}-y${yi}`, {
        points: [new Vector3(xi - x / 2, yi, 0 - z / 2), new Vector3(xi - x / 2, yi, z - z / 2)],
      });
      line.alpha = lineAlpha;
      line.color = Color3.White();
    }
  }
  for (let xi = 0; xi <= x; xi += stepX) {
    for (let zi = 0; zi <= z; zi += stepZ) {
      const line = CreateLines(`line-x${xi}-z${zi}`, {
        points: [new Vector3(xi - x / 2, 0, zi - z / 2), new Vector3(xi - x / 2, y, zi - z / 2)],
      });
      line.alpha = lineAlpha;
      line.color = Color3.White();
    }
  }

  for (let yi = 0; yi <= y; yi += stepY) {
    for (let zi = 0; zi <= z; zi += stepZ) {
      const line = CreateLines(`line-y${yi}-z${zi}`, {
        points: [new Vector3(0 - x / 2, yi, zi - z / 2), new Vector3(x - x / 2, yi, zi - z / 2)],
      });
      line.alpha = lineAlpha;
      line.color = Color3.White();
    }
  }
}
