/**
 * @typedef {{x: int, y: int, z: int}} RawCoordiante
 */

/**
 * @typedef {{x: int, y: int, z: int, t: int}} RawTimeCoordiante
 */

/**
 * @typedef {Array<x: int, y: int, z: int>} RawArrayCoordiante
 */

/**
 * @typedef {{t: RawArrayCoordiante}} RawTimeArrayCoordinate
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
 * @property {int} id
 * @property {string} name
 * @property {int} speed
 * @property {int} near_radius
 * @property {int} far_radius
 * @property {float} welfare
 * @property {int} battery
 * @property {int} time_in_air
 * @property {float} non_colliding_welfare
 * @property {int} near_field_intersections
 * @property {int} far_field_intersections
 * @property {int} near_field_violations
 * @property {int} far_field_violations
 * @property {int} bid
 * @property {int} owner_id
 * @property {string} owner_name
 * @property {RawPath[]} paths
 * @property {RawBranch[]} branches
 */

/**
 * @typedef {Object} RawOwner
 * @property {string} name
 * @property {int} id
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
 * @property {int} total_welfare
 * @property {float} mean_welfare
 * @property {float} median_welfare
 * @property {float} max_welfare
 * @property {float} min_welfare
 * @property {float[]} welfare_quantiles
 * @property {float[]} welfare_outliers
 * @property {int} number_of_agents
 * @property {int} number_of_ab_agents
 * @property {int} number_of_aba_agents
 * @property {int} number_of_abc_agents
 * @property {int} number_of_stationary_agents
 */

/**
 * @typedef {Object} RawBlocker
 * @property {int} id
 * @property {string} type
 * @property {RawPath | undefined} [path]
 * @property {RawCoordiante | undefined} [location]
 * @property {RawCoordiante} dimension
 */

/**
 * @typedef {Object} RawMapTile
 * @property {int} x
 * @property {int} y
 * @property {int} z
 * @property {{long: number, lat: number}} top_left_coordinate
 * @property {{long: number, lat: number}} bottom_right_coordinate
 * @property {RawTimeCoordiante} dimensions
 */

/**
 * @typedef {Object} RawEnvironment
 * @property {RawTimeCoordiante} dimensions
 * @property {RawBlocker[]} blockers
 * @property {RawMapTile[]} maptiles
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
 * @typedef {Object} RawSimulation
 * @property {string} name
 * @property {string} description
 * @property {RawEnvironment} environment
 * @property {RawStatistics} statistics
 * @property {RawOwner[]} owners
 */
