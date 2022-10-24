/**
 * @typedef {Object} JSONResponse
 * @property {JSONConfig} config
 * @property {OwnerMap} owner_map
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
 * @typedef {{str: JSONConfigOwner}} OwnerMap
 */

/**
 * @typedef {Object} JSONConfigOwner
 * @property {string} name
 * @property {string} color
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
 * @typedef {Object} JSONBlock
 * @property {int} tick
 * @property {JSONSpace[]} spaces
 */

/**
 * @typedef {Object} JSONAgent
 * @property {string} agent_type
 * @property {string} id
 * @property {JSONBranch[] | JSONBlock[]} [intermediate_allocations]
 * Space-Agent:
 * @property {JSONSpace[]} [blocks]
 * Path-Agent:
 * @property {int} [speed]
 * @property {int} [near_radius]
 * @property {int} [battery]
 * @property {JSONPath[]} [paths]
 */

/**
 * @typedef {Object} JSONOwner
 * @property {string} id
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
 * @property {OwnerStatistics[]} path_owners
 * @property {OwnerStatistics[]} space_owners
 * @property {int} total_number_of_owners
 * @property {int} total_number_of_agents
 * @property {FinanceStatistics} value_stats
 * @property {FinanceStatistics} payment_stats
 * @property {FinanceStatistics} utility_stats
 * @property {float} total_non_colliding_value
 * @property {float} total_non_colliding_utility
 * @property {int} total_number_of_violations
 * @property {int} total_number_of_reallocations
 * @property {{int: int}} step_compute_time
 */

/**
 * @typedef {Object} OwnerStatistics
 * @property {string} id
 * @property {AgentStatistics[]} agents
 * @property {int} total_time_in_air
 * @property {FinanceStatistics} values
 * @property {FinanceStatistics} payments
 * @property {FinanceStatistics} utilities
 * @property {FinanceStatistics} non_colliding_values
 * @property {FinanceStatistics} non_colliding_utility
 * @property {int} number_of_agents
 */

/**
 * @typedef {Object} FinanceStatistics
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
 * @property {float} payment
 * @property {float} utility
 * @property {float} non_colliding_value
 * @property {float} non_colliding_utility
 * @property {ViolationStatistics} violations
 * @property {int} total_reallocations
 * @property {?RawAllocationStatistics[]} allocations
 **/

/**
 * @typedef {AgentStatistics} SpaceAgentStatistics
 * @property {?SpaceStatistics} space
 **/

/**
 * @typedef {AgentStatistics} PathAgentStatistics
 * @property {?PathStatistics} path
 * @property {?int} time_in_air
 * @property {?int} battery_unused
 * @property {?int[]} delayed_starts
 * @property {?int[]} delayed_arrivals
 * @property {?int[]} re_delayed_arrivals
 */

/**
 * @typedef {object} RawBid
 * @property {Object<string: Any>} data
 * @property {{string: string|number|boolean}} display
 */

/**
 * @typedef {Object} RawAllocationStatistics
 * @property {int} tick
 * @property {float} value
 * @property {float} payment
 * @property {float} utility
 * @property {RawBid} bid
 * @property {string} reason
 * @property {string} explanation
 * @property {{string: RawBid}} colliding_agent_bids - maps agent_ids to bids
 * @property {{string: RawBid}} displacing_agent_bids - maps agent_ids to bids
 * @property {int} compute_time
 * @property {PathStatistics} path
 * @property {SpaceStatistics} space
 */

/**
 * @typedef {Object} ViolationStatistics
 * @property {{string: JSONTimeCoordinate[]}} violations
 * @property {int} total_violations
 * @property {{int: JSONTimeCoordinate[]}} blocker_violations
 * @property {int} total_blocker_violations
 * @property {boolean} incomplete_allocation
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
 * @property {JSONTimeCoordinate} dimensions
 * @property {JSONMap} map
 * @property {JSONConfigOwner[]} owners
 * @property {string[]} availableAllocators
 * @property {JSONAvailableOwner[]} availableOwnersForAllocator
 */

/**
 * @typedef {Object} JSONSimulation
 * @property {JSONEnvironment} environment
 * @property {JSONOwner[]} path_owners
 * @property {JSONOwner[]} space_owners
 */
