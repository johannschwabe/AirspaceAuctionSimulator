/**
 * Ligthens a hex color input by X percent
 * @param {string} color
 * @param {number} percent
 * @returns {`#${string}`}
 */
export const lightenColor = function (color, percent) {
  const col = color.startsWith("#") ? color.slice(1) : color;
  const num = parseInt(col, 16),
    amt = Math.round(2.55 * percent),
    R = (num >> 16) + amt,
    B = ((num >> 8) & 0x00ff) + amt,
    G = (num & 0x0000ff) + amt;

  const hex = (
    0x1000000 +
    (R < 255 ? (R < 1 ? 0 : R) : 255) * 0x10000 +
    (B < 255 ? (B < 1 ? 0 : B) : 255) * 0x100 +
    (G < 255 ? (G < 1 ? 0 : G) : 255)
  )
    .toString(16)
    .slice(1);
  return `#${hex}`;
};

/**
 * Returns a random hex color
 * @returns {`#${string}`}
 */
export const randomColor = () => "#" + ((Math.random() * 0xffffff) << 0).toString(16).padStart(6, "0");
