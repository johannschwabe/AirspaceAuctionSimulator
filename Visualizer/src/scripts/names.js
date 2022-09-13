import { uniqueNamesGenerator, starWars, countries } from "unique-names-generator";

export const randomName = () => {
  return uniqueNamesGenerator({
    dictionaries: [
      [...starWars, "Johann", "Paul", "Thomas", "Joel", "Ludwig", "Sven Seuken", "PolygonSoftware - Daniel"],
    ],
    style: "capital",
    separator: " ",
  });
};

export const randomSimulationName = () => {
  return uniqueNamesGenerator({
    dictionaries: [[...countries, "Risotto", "Atlantis", "Westeros", "Arrakis", "Shire", "Gondor"]],
    style: "capital",
    separator: " ",
  });
};
