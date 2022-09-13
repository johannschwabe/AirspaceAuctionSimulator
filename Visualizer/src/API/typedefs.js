/**
 * @typedef {Object} JSONResponse
 * @property {JSONConfig} config
 * @property {SimulationStatistics} statistics
 * @property {JSONSimulation} simulation
 * @property {int} statistics_compute_time
 * @property {int} simulation_compute_time
 */

/*
 * Simulation
 */

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
 * @property {{int: JSONArrayCoordinate}} positions
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
 */

/**
 * @typedef {Object} JSONAgent
 * @property {string} agent_type
 * @property {string} id
 * Space-Agent:
 * @property {JSONSpace[]} [spaces]
 * Path-Agent:
 * @property {int} [speed]
 * @property {int} [near_radius]
 * @property {int} [battery]
 * @property {JSONPath[]} [paths]
 * @property {JSONBranch[]} [branches]
 */

/**
 * @typedef {Object} JSONOwner
 * @property {string} name
 * @property {string} id
 * @property {string} color
 * @property {JSONAgent[]} agents
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

/*
 * Statistics
 */

/**
 * @typedef {Object} SimulationStatistics
 * @property {OwnerStatistics[]} owners
 * @property {int} total_number_of_owners
 * @property {int} total_number_of_agents
 * @property {float} total_value
 * @property {float} total_non_colliding_value
 * @property {int} total_number_of_collisions
 * @property {int} total_number_of_reallocations
 * @property {{int: int}} step_compute_time
 */

/**
 * @typedef {Object} OwnerStatistics
 * @property {string} id
 * @property {AgentStatistics[]} agents
 * @property {int} total_time_in_air
 * @property {ValueStatistics} values
 * @property {ValueStatistics} non_colliding_values
 * @property {int} number_of_agents
 */

/**
 * @typedef {Object} ValueStatistics
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
 * @typedef {Object} AgentStatistics
 * @property {string} id
 * @property {float} value
 * @property {float} non_colliding_value
 * @property {ViolationStatistics} violations
 * @property {int} total_reallocations
 * Space-Agent:
 * @property {SpaceStatistics} [space]
 * Path-Agent:
 * @property {int} [time_in_air]
 * @property {PathStatistics} [path]
 * @property {AllocationStatistics[]} [allocations]
 */

/**
 * @typedef {Object} AllocationStatistics
 * @property {int} tick
 * @property {float} value
 * @property {string} reason
 * @property {string} explanation
 * @property {string[]} colliding_agent_ids
 * @property {int} compute_time
 */

/**
 * @typedef {Object} ViolationStatistics
 * @property {{string: JSONTimeCoordinate[]}} violations
 * @property {int} total_violations
 */

/**
 * @typedef {Object} SpaceStatistics
 * @property {int} volume
 * @property {float} mean_volume
 * @property {int} median_volume
 * @property {float} mean_height
 * @property {int} median_height
 * @property {int} area
 * @property {float} mean_area
 * @property {int} median_area
 * @property {float} mean_time
 * @property {int} median_time
 * @property {float} mean_height_above_ground
 * @property {int} median_height_above_ground
 */

/**
 * @typedef {Object} PathStatistics
 * @property {int} l1_distance
 * @property {float} l2_distance
 * @property {int} l1_ground_distance
 * @property {float} l2_ground_distance
 * @property {int} height_difference
 * @property {int} time_difference
 * @property {int} ascent
 * @property {int} descent
 * @property {int} distance_traveled
 * @property {int} ground_distance_traveled
 * @property {float} mean_height
 * @property {int} median_height
 * @property {int[]} heights
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
