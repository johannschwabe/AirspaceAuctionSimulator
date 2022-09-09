import { uniqueNamesGenerator, starWars, countries } from "unique-names-generator";

export const randomName = () => {
  return uniqueNamesGenerator({
    dictionaries: [starWars],
    style: "capital",
    separator: " ",
  });
};

export const randomSimulationName = () => {
  return uniqueNamesGenerator({
    dictionaries: [countries],
    style: "capital",
    separator: " ",
  });
};
