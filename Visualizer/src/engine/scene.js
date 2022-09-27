import { Scene } from "@babylonjs/core/scene";
import { Color4, Vector3 } from "@babylonjs/core/Maths/math";
import { ArcRotateCamera } from "@babylonjs/core/Cameras/arcRotateCamera";
import { SSAORenderingPipeline } from "@babylonjs/core";

export function useScene({ engine }) {
  const scene = new Scene(engine);
  scene.clearColor = Color4.FromHexString("#101010");
  return scene;
}

export function useCamera({ x, y, z, scene, canvas }) {
  const target = new Vector3(0, y / 2, 0);
  const camera = new ArcRotateCamera("camera", -Math.PI / 2, Math.PI / 2.5, 3, target, scene);
  camera.attachControl(canvas, true);
  camera.setTarget(target);
  camera.setPosition(new Vector3(0, Math.max(x, y, z), -z));
  camera.lowerRadiusLimit = 5;
  camera.upperRadiusLimit = 1000;
  new SSAORenderingPipeline("ssaopipeline", scene, { ssaoRatio: 1, combineRatio: 1 });
  scene.postProcessRenderPipelineManager.attachCamerasToRenderPipeline("ssaopipeline", camera);
  return camera;
}
