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
  title: "",
  abstract: "",
  content: ``,
};
export const hVoxelSize = {
  title: "",
  abstract: "",
  content: ``,
};
export const hSurroundingTiles = {
  title: "",
  abstract: "",
  content: ``,
};
export const hMinHeight = {
  title: "",
  abstract: "",
  content: ``,
};
export const hAllocationPeriod = {
  title: "",
  abstract: "",
  content: ``,
};
