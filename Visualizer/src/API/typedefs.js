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
 * @typedef {{t: RawArrayCoordinate}} RawTimeArrayCoordinate
 */

/**
 * @typedef {Object} RawPath
 * @property {RawTimeArrayCoordinate} t
 */

/**
 * @typedef {string} RawCollisionReason
 */

/**
 * @typedef {string} RawReason
 */

/**
 * @typedef {Object} RawCollision
 * @property {RawReason} reason
 * @property {int} agent_id
 * @property {int} blocker_id
 */

/**
 * @typedef {Object} RawBranch
 * @property {int} tick
 * @property {RawPath[]} paths
 * @property {float} value
 * @property {RawCollision} reason
 */

/**
 * @typedef {Object} RawAgent
 * @property {string} agent_type
 * @property {string} allocation_type
 * @property {string} id
 * @property {string} name
 * @property {int} speed
 * @property {int} near_radius
 * @property {int} far_radius
 * @property {float} utility
 * @property {int} battery
 * @property {int} time_in_air
 * @property {float} non_colliding_utility
 * @property {int} near_field_intersections
 * @property {int} far_field_intersections
 * @property {int} near_field_violations
 * @property {int} far_field_violations
 * @property {int} bid
 * @property {int} owner_id
 * @property {string} owner_name
 * @property {RawPath[]} paths
 * @property {RawBranch[]} branches
 * @property {{min: RawTimeCoordinate, max: RawTimeCoordinate}[]} spaces
 */

/**
 * @typedef {Object} RawOwner
 * @property {string} name
 * @property {string} id
 * @property {string} color
 * @property {RawAgent[]} agents
 * @property {int} total_time_in_air
 * @property {int} total_bid_value
 * @property {float} mean_bid_value
 * @property {float} median_bid_value
 * @property {float} max_bid_value
 * @property {float} min_bid_value
 * @property {float[]} bid_quantiles
 * @property {float[]} bid_outliers
 * @property {int} total_utility
 * @property {float} mean_utility
 * @property {float} median_utility
 * @property {float} max_utility
 * @property {float} min_utility
 * @property {float[]} utility_quantiles
 * @property {float[]} utility_outliers
 * @property {int} number_of_agents
 * @property {int} number_of_ab_agents
 * @property {int} number_of_aba_agents
 * @property {int} number_of_abc_agents
 * @property {int} number_of_stationary_agents
 */

/**
 * @typedef {Object} RawBlocker
 * @property {string} id
 * @property {string} blocker_type
 * @property {RawPath | undefined} [path]
 * @property {RawCoordinate | undefined} [location]
 * @property {RawCoordinate} dimension
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
 * @typedef {Object} RawEnvironment
 * @property {RawTimeCoordinate} dimensions
 * @property {RawBlocker[]} blockers
 */

/**
 * @typedef {Object} RawStatistics
 * @property {int} total_number_of_owners
 * @property {int} total_number_of_agents
 * @property {int} total_achieved_welfare
 * @property {int} total_number_of_collisions
 * @property {int} total_number_of_reallocations
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
