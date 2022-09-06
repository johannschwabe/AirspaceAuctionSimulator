/**
 * @typedef {{x: int, y: int, z: int}} JSONCoordinate
 */

/**
 * @typedef {{x: int, y: int, z: int, t: int}} JSONTimeCoordinate
 */

/**
 * @typedef {Array<x: int, y: int, z: int>} JSONArrayCoordinate
 */

/**
 * @typedef {Object} JSONPath
 * @property {int: JSONArrayCoordinate} positions
 */

/**
 * @typedef {Object} JSONSpace
 * @property {JSONTimeCoordinate} min
 * @property {JSONTimeCoordinate} max
 */

/**
 * @typedef {Object} JSONBranch
 * @property {int} tick
 * @property {JSONPath[]} paths
 * @property {float} value
 * @property {string} reason
 * @property {string[]} colliding_agent_ids
 * @property {int} compute_time
 */

/**
 * @typedef {Object} JSONViolations
 * @property {{string: JSONTimeCoordinate}} violations
 * @property {int} total_violations
 */

/**
 * @typedef {Object} JSONAgent
 * @property {string} agent_type
 * @property {string} id
 * @property {float} value
 * @property {float} non_colliding_value
 * @property {JSONViolations} violations
 * @property {int} total_reallocations
 * Space-Agent:
 * @property {JSONSpace[]} [spaces]
 * Path-Agent:
 * @property {int} [speed]
 * @property {int} [near_radius]
 * @property {int} [battery]
 * @property {int} [time_in_air]
 * @property {JSONPath[]} [paths]
 * @property {JSONBranch[]} [branches]
 */

/**
 * @typedef {Object} JSONValues
 * @property {float[]} values
 * @property {float} total
 * @property {float} mean
 * @property {float} median
 * @property {float} max
 * @property {float} min
 * @property {float[]} quartiles
 * @property {float[]} outliers
 */

/**
 * @typedef {Object} JSONOwner
 * @property {string} name
 * @property {string} id
 * @property {string} color
 * @property {JSONAgent[]} agents
 * @property {int} total_time_in_air
 * @property {JSONValues} values
 * @property {JSONValues} non_colliding_values
 * @property {int} number_of_agents
 * @property {{string: int}} number_per_type
 */

/**
 * @typedef {Object} JSONBlocker
 * @property {string} id
 * @property {string} blocker_type
 * @property {JSONTimeCoordinate[]} [locations]
 * @property {JSONCoordinate} [location]
 * @property {JSONCoordinate} dimension
 */

/**
 * @typedef {Object} JSONEnvironment
 * @property {JSONTimeCoordinate} dimensions
 * @property {JSONBlocker[]} blockers
 */

/**
 * @typedef {Object} JSONStatistics
 * @property {int} total_number_of_owners
 * @property {int} total_number_of_agents
 * @property {float} total_value
 * @property {float} total_non_colliding_value
 * @property {int} total_number_of_collisions
 * @property {int} total_number_of_reallocations
 */

/*
 * Config
 */

/**
 * @typedef {Object} JSONSimpleCoordinate
 * @property {number} lat
 * @property {number} long
 */

/**
 * @typedef {Object} JSONMap
 * @property {JSONSimpleCoordinate} coordinates
 * @property {string} locationName
 * @property {int} neighbouringTiles
 * @property {int} resolution
 * @property {JSONSimpleCoordinate} bottomLeftCoordinate
 * @property {int[][]} tiles
 */

/**
 * @typedef {Object} JSONMeta
 * @property {string} key
 * @property {string} name
 * @property {string} description
 * @property {string} type
 * @property {string|number|boolean} value
 */

/**
 * @typedef {Object} JSONAvailableOwner
 * @property {string} label
 * @property {string} name
 * @property {string} description
 * @property {string} type
 * @property {string} allocator
 * @property {int} minLocations
 * @property {int} maxLocations
 * @property {JSONMeta[]} meta
 */

/**
 * @typedef {Object} JSONConfig
 * @property {string} name
 * @property {string} description
 * @property {string} allocator
 * @property {dimension} JSONTimeCoordinate
 * @property {JSONMap} map
 * @property {JSONOwner[]} owners
 * @property {string[]} availableAllocators
 * @property {JSONAvailableOwner[]} availableOwnersForAllocator
 */

/**
 * @typedef {Object} JSONSimulation
 * @property {JSONEnvironment} environment
 * @property {JSONOwner[]} owners
 */

/**
 * @typedef {Object} JSONResponse
 * @property {JSONConfig} config
 * @property {JSONStatistics} statistics
 * @property {JSONSimulation} simulation
 */
