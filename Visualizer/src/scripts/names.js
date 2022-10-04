import { uniqueNamesGenerator, starWars, countries } from "unique-names-generator";

/**
 * Returns a random name for an owner
 * @returns {string}
 */
export const randomName = () => {
  return uniqueNamesGenerator({
    dictionaries: [
      [...starWars, "Johann", "Paul", "Thomas", "Joel", "Ludwig", "Sven Seuken", "PolygonSoftware - Daniel"],
    ],
    style: "capital",
    separator: " ",
  });
};

/**
 * Returns a random name for a simulation
 * @returns {string}
 */
export const randomSimulationName = () => {
  return uniqueNamesGenerator({
    dictionaries: [[...countries, "Risotto", "Atlantis", "Westeros", "Arrakis", "Shire", "Gondor"]],
    style: "capital",
    separator: " ",
  });
};
