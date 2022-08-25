import { uniqueNamesGenerator, starWars } from "unique-names-generator";

export const randomName = () => {
  return uniqueNamesGenerator({
    dictionaries: [starWars],
    style: "capital",
    separator: " ",
  });
};
