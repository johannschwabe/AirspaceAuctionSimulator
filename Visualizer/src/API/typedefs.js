/**
 * @typedef {{x: int, y: int, z: int}} RawCoordinate
 */

/**
 * @typedef {{x: int, y: int, z: int, t: int}} RawTimeCoordinate
 */

/**
 * @typedef {Array<x: int, y: int, z: int>} RawArrayCoordinate
 */

/**
 * @typedef {Object} RawPath
 * @property {int: RawArrayCoordinate} positions
 */

/**
 * @typedef {Object} RawSpace
 * @property {RawTimeCoordinate} min
 * @property {RawTimeCoordinate} max
 */

/**
 * @typedef {Object} RawBranch
 * @property {int} tick
 * @property {RawPath[]} paths
 * @property {float} value
 * @property {string} reason
 * @property {string[]} colliding_agent_ids
 * @property {int} compute_time
 */

/**
 * @typedef {Object} RawViolations
 * @property {{string: RawTimeCoordinate}} violations
 * @property {int} total_violations
 */

/**
 * @typedef {Object} RawAgent
 * @property {string} agent_type
 * @property {string} id
 * @property {float} value
 * @property {float} non_colliding_value
 * @property {RawViolations} violations
 * @property {int} total_reallocations
 * Space-Agent:
 * @property {RawSpace[]} [spaces]
 * Path-Agent:
 * @property {int} [speed]
 * @property {int} [near_radius]
 * @property {int} [battery]
 * @property {int} [time_in_air]
 * @property {RawPath[]} [paths]
 * @property {RawBranch[]} [branches]
 */

/**
 * @typedef {Object} RawValues
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
 * @typedef {Object} RawOwner
 * @property {string} name
 * @property {string} id
 * @property {string} color
 * @property {RawAgent[]} agents
 * @property {int} total_time_in_air
 * @property {RawValues} values
 * @property {RawValues} non_colliding_values
 * @property {int} number_of_agents
 * @property {{string: int}} number_per_type
 */

/**
 * @typedef {Object} RawBlocker
 * @property {string} id
 * @property {string} blocker_type
 * @property {RawTimeCoordinate[]} [locations]
 * @property {RawCoordinate} [location]
 * @property {RawCoordinate} dimension
 */

/**
 * @typedef {Object} RawEnvironment
 * @property {RawTimeCoordinate} dimensions
 * @property {RawBlocker[]} blockers
 */

/**
 * @typedef {Object} RawStatistics
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
 * @typedef {Object} RawSimpleCoordinate
 * @property {number} lat
 * @property {number} long
 */

/**
 * @typedef {Object} RawMap
 * @property {RawSimpleCoordinate} coordinates
 * @property {string} locationName
 * @property {int} neighbouringTiles
 * @property {int} resolution
 * @property {RawSimpleCoordinate} bottomLeftCoordinate
 * @property {int[][]} tiles
 */

/**
 * @typedef {Object} RawMeta
 * @property {string} key
 * @property {string} name
 * @property {string} description
 * @property {string} type
 * @property {string|number|boolean} value
 */

/**
 * @typedef {Object} RawAvailableOwner
 * @property {string} label
 * @property {string} name
 * @property {string} description
 * @property {string} type
 * @property {string} allocator
 * @property {int} minLocations
 * @property {int} maxLocations
 * @property {RawMeta[]} meta
 */

/**
 * @typedef {Object} RawConfig
 * @property {string} name
 * @property {string} description
 * @property {string} allocator
 * @property {dimension} RawTimeCoordinate
 * @property {RawMap} map
 * @property {RawOwner[]} owners
 * @property {string[]} availableAllocators
 * @property {RawAvailableOwner[]} availableOwnersForAllocator
 */

/**
 * @typedef {Object} RawSimulation
 * @property {RawConfig} config
 * @property {RawEnvironment} environment
 * @property {RawStatistics} statistics
 * @property {RawOwner[]} owners
 */
