import { Engine } from "@babylonjs/core/Engines/engine";

/**
 * Creates a new instance of a babylon game engine
 * @param {Object} args
 * @param {Ref<HTMLCanvasElement>} args.canvas
 * @returns {Engine}
 */
export function useEngine({ canvas }) {
  return new Engine(canvas.value, true, {
    preserveDrawingBuffer: true,
    stencil: true,
  });
}
