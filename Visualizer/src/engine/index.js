import { Engine } from "@babylonjs/core/Engines/engine";

export function useEngine({ canvas }) {
  return new Engine(canvas.value, true, {
    preserveDrawingBuffer: true,
    stencil: true,
  });
}
