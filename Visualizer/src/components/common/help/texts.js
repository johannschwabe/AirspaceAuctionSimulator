export const hEmpty = {
  title: "",
  abstract: "",
  content: ``,
};
export const hName = {
  title: "Model Name",
  abstract: "Name of model, used for Filenames.",
  content: `You can freely choose the name of your model, although it should not exceed 60 characters. Your model name
will serve as a filename for both your config and simulation output, hence you should avoid special characters.`,
};
export const hDescription = {
  title: "Model Description",
  abstract: "Full-Text description of your Model",
  content: `Use this text to freely describe your model as well as your ideas that lead to running this simulations.
You do not need to document your input parameters, they will be included in the simulation anyways.`,
};
export const hTimesteps = {
  title: "Timesteps",
  abstract: "Number of timesteps in which simulation must finish",
  content: `A simulation runs in timesteps. An agent with speed 1 can move 1 voxel per timestep. The number of
timesteps a simulation runs determines the timeframe in which all agents must take of and reach their
goal / destination. When you define bigger playing fields (e.g. larger maps), you should run the simulation for
more timesteps. Otherwise, agents can't possible reach their destinations on-time and will not be allocated by the
allocator. However, running longer simulations will lead to fewer collisions, since fewer agents are forced to be
in the air at the same time. To reach a high amount of collisions with large playfields, increase the voxel size.`,
};
export const hAllocator = {
  title: "Allocator",
  abstract: "Allocates paths to agents",
  content: `The allocator is responsible for allocating paths to agents based on the specified
bidding mechanism and payment function.`,
};
export const hPaymentRule = {
  title: "Payment Rule",
  abstract: "How agents pay for allocations",
  content: `The payment rule specifies how the agents compete for paths in a simulation. Not all
allocators can handle all payment rules, though.`,
};
export const hOwners = {
  title: "Owners",
  abstract: "Spawn agents of identical kind",
  content: `Owners act according to a bidding strategy and to maximize their value functions. They spawn
agents on the playing field and act on their best interrest.`,
};
export const hAddress = {
  title: "Address Query",
  abstract: "Real-World location of simulation",
  content: `Airspace simulations happen on a real map. By specifying an address here, you can choose
where your simulation will be centered. You can use any city as an input here, for example
"Zurich", "New York" or "Barcelona". Real 3D Data from buildings in that location will be loaded that
act as obstacles that the agents have to navigate.`,
};
export const hHeight = {
  title: "Height",
  abstract: "Maximum flight height of agents",
  content: `The maximum height your agents are allowed to fly.`,
};
export const hVoxelSize = {
  title: "Voxel Size",
  abstract: "Qubic voxel dimensions in meters",
  content: `This parameter lets you specify the resolution of your simulation. Per default, agents
can navigate through the map with a precision of 1m. By increasing this parameter, your
agents can navigate less precisely around buildings, but the simulation duration decreases drastically.`,
};
export const hSurroundingTiles = {
  title: "Surrounding Map Tiles",
  abstract: "Increases playfield size",
  content: `Per default, a ~800m by ~800m region around your address input is used for the
simulation - for technical reasons. By increasing the amount of neighbouring tiles,
you can increase the region to 2400m^2, 4000m^2 and 5600m^2.`,
};
export const hMinHeight = {
  title: "Minimum Flight Height",
  abstract: "Spawn height of agents",
  content: `The minimum height your agents must fly up to before navigating the map. Your agents will
appear at this height. Usually, this height is set to be slightly higher than the average
building in your city, since we want to prevent agents to fly accross balconies.`,
};
export const hAllocationPeriod = {
  title: "Alocation Period",
  abstract: "How long new agents spawn",
  content: `Agents should not be allowed to start their journey in the last timesteps, since they
will not reach their destination on-time. Hence, you need to specify for how long new
agents are allowed to enter the playing field. Usually, this parameter should be between
10 and 33 percent of the total number of timesteps you specified.`,
};
export const hOwnerColor = {
  title: "Owner Color",
  abstract: "Display color of Agents",
  content: `All agents spawned by this owner will appear in the specified color within the Simulation Visualizer.`,
}
export const hOwnerName = {
  title: "Owner Name",
  abstract: "Name of owner can be freely choosen",
  content: `The name of the owner can be arbitrarily choosen. It will also appear in the name of the agents.`,
};
export const hOwnerAgents = {
  title: "Owner number of Agents",
  abstract: "How many agents an owner will spawn",
  content: `This number indicates how many agents an owner will try to spawn within the allocation period.`,
};
export const hOwnerBidding = {
  title: "Owner Bidding Strategy",
  abstract: "How the owners agent will place bids",
  content: `The bidding strategy sets up the rules how agents compete for airspace using bids. Not all bidding strategies
are supported by all Allocators.`,
};
export const hOwnerValue = {
  title: "Owner Value Function",
  abstract: "How the owners agent calculate their value for airspace",
  content: `Thhe value function determines how the owners agents find out which path brings them what value. Based
on the value they get from a path, they will place a bid on it. Hence, the value function must be supported by
the bidding strategy.`,
};
export const hMapSelection = {
  title: "Map Area Selection",
  abstract: "Define sub-area of visible map as playfield",
  content: `You have the option to select a square from a map. Agents will only be allowed to spawn and fly within
this region, and only buildings that originate within this area will be considered for the route determination.`,
};
export const hStops = {
  title: "Owner Stops",
  abstract: "Route of locations for Path agents, area locations for space agents",
  content: `Path agents can have multiple stops that they want to fly towards. If you give a path agents 2 stop,
your agent will fly from the first location to the second location. If you give him more stops, he will start
at the first, visit all locations in order, until he de-spawns at the last. For space agents, the multiple locations
determine where agents will reserve their airspace. If you determine two locations, each agent will reserve reserve
space at both locations at the same time, with the exact same airspace dimensions and for the same time period.
For random locations or heatmap locations, the locations are drawn at random (or weighted random in the case of the
heatmap) for every agent.`,
};
export const hPositonMap = {
  title: "Position Location",
  abstract: "Select exact point as location",
  content: `Select an exact coordinate for this stop / location.`,
};
export const hHeatmap = {
  title: "Heatmap Location",
  abstract: "Define heatmap of possible locations",
  content: `Draw a heatmap - a location from the drawing will be selected based on the intensity of the heatmap.
Hence, you can only get points that you drew your heatmap on, and it is most likely that the point will be in a region
that appears dark in your drawing.`
};
