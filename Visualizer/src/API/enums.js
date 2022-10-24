/**
 * ENUM containing all possible agent types
 * @type {{PATH: string, SPACE: string}}
 */
export const AgentType = {
  PATH: "path",
  SPACE: "space",
};

/**
 * ENUM containing all possible blocker types
 * @type {{STATIC: string, DYNAMIC: string}}
 */
export const BlockerType = {
  STATIC: "static",
  DYNAMIC: "dynamic",
};

/**
 * ENUM containing all possible branching reasons
 * @type {{FIRST_ALLOCATION: string, REALLOCATION: string, ALLOCATION_FAILED: string}}
 */
export const BRANCH_REASONS = {
  REALLOCATION: "REALLOCATION",
  ALLOCATION_FAILED: "ALLOCATION_FAILED",
  FIRST_ALLOCATION: "FIRST_ALLOCATION",
};
