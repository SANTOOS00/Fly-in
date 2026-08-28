
*This project has been created as part of the 42 curriculum by moerrais.*

# Fly-in Drones

## Description

**Fly-in Drones** is a pathfinding and simulation project developed as part of the 42 curriculum. The goal of the project is to move a given number of drones from a unique starting zone to a unique destination zone in the **minimum possible number of simulation turns**.

The environment is represented as a network of interconnected zones. Each zone has a name, integer coordinates, and optional metadata such as its type, color, and maximum drone capacity. Zones can be `normal`, `restricted`, `priority`, or `blocked`, and each type affects how drones can move through the network.

Connections between zones are bidirectional and can also have a maximum capacity, limiting the number of drones that can use the connection simultaneously. The simulation must therefore take into account both zone and connection capacities when scheduling drone movements.

The program parses a map file, validates its structure and metadata, builds a graph representing the network, and calculates efficient routes from the start zone to the destination. It then schedules the movement of all drones while allowing them to move simultaneously whenever possible.

The routing strategy considers several factors, including path length, zone movement costs, priority zones, zone capacities, connection capacities, and possible conflicts between drones. When a drone cannot move safely, it may wait until the required space or connection becomes available.

The simulation is performed turn by turn until all drones reach the destination. The program also provides a visual representation of the simulation through colored terminal output and/or graphical elements, allowing users to follow drone movements, zone states, and the evolution of the network during execution.

The project focuses on **graph algorithms, pathfinding, scheduling, parsing, simulation, capacity management, and optimization**, while ensuring that the solution can adapt to different network topologies and different numbers of drones.


## **Instructions**

### **Installation**

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd <project-directory>
```

Create and activate the Python virtual environment:

```bash
make env
```

Install the project dependencies:

```bash
make install
```

### **Running the Project**

To run the project with a map definition file, use:

```bash
make run MAP_DEF=<path-to-map-file>
```

For example:

```bash
make run MAP_DEF=maps/example.txt
```

The program reads and validates the map file, calculates efficient routes for the drones, and starts the simulation.

The map file must follow the format specified by the project requirements. It must contain the number of drones, one starting zone, one destination zone, the other zones, and their connections.

Example:

```text
nb_drones: 5
start_hub: hub 0 0 [color=green]
end_hub: goal 10 10 [color=yellow]
hub: roof1 3 4 [zone=restricted color=red]
hub: roof2 6 2 [zone=normal color=blue]
hub: corridorA 4 3 [zone=priority color=green max_drones=2]
connection: hub-roof1
connection: hub-corridorA
connection: roof1-roof2
connection: roof2-goal
connection: corridorA-goal
```

### **Makefile Commands**

The project provides several Makefile commands to simplify development and execution.

| Command                   | Description                                       |
| ------------------------- | ------------------------------------------------- |
| `make env`                | Creates the Python virtual environment.           |
| `make install`            | Installs the required project dependencies.       |
| `make`                    | Runs the default Makefile target.                 |
| `make run MAP_DEF=<path>` | Runs the simulation using the specified map file. |
| `make lint`               | Runs the project's code linter.                   |
| `make lint-strict`        | Runs the linter with stricter checks.             |
| `make debug`              | Runs the project in debug mode.                   |
| `make clean`              | Removes generated files and build artifacts.      |

## Resources

### References

The following resources were used during the development of the project:

* **Graph Theory** — [A Gentle Introduction to Graph Theory](https://medium.com/basecs/a-gentle-introduction-to-graph-theory-77969829ead8)
  Used to understand graphs, nodes, edges, and the representation of the drone network.

* **Dijkstra's Algorithm** — References and documentation about shortest-path algorithms.
  Used to understand and implement shortest-path finding in the drone network.

* **Yen's K-Shortest Paths Algorithm** — [Yen's Algorithm](https://www.linchenguang.com/2018/01/30/Yen-s-algorithm/)
  Used as inspiration for finding alternative paths. The project does not implement Yen's algorithm directly; instead, its general idea of finding alternative routes was adapted to the project's drone-routing strategy.


* **Color Depth** — [Wikipedia](https://en.wikipedia.org/wiki/Color_depth)
  Used as an additional reference for understanding digital color representation.

* **Color Depth and Channels** — [Renewed Vision](https://www.renewedvision.com/blog/color-depth-and-channels-explained)
  Used as an additional reference for understanding color channels and color representation.

### AI Usage

AI tools were used mainly as a learning and development aid during the project.

The main algorithmic strategy and implementation were developed by me. I used **Dijkstra's algorithm** as the main pathfinding algorithm to find the shortest path between the start and destination zones.

For finding alternative paths, I took inspiration from the idea behind **Yen's K-Shortest Paths algorithm**. I did not implement Yen's algorithm directly or as a complete implementation. Instead, I adapted the general idea to fit the specific requirements of this project.

My approach finds a path for a drone using Dijkstra's algorithm. After a path is selected, the graph is modified by removing selected edges from the chosen route. Dijkstra's algorithm is then run again to find another possible path for the next drone. This process is repeated to generate different routing possibilities.

The generated paths are evaluated according to the number of simulation turns required for all drones to reach the destination. The objective is to distribute the drones between suitable paths and minimize the total number of turns while respecting zone and connection capacity constraints.

AI was used for:

* Understanding and clarifying the project requirements.
* Learning and reviewing Dijkstra's algorithm.
* Understanding the general concept behind Yen's K-Shortest Paths algorithm.
* Discussing possible approaches for finding alternative paths.
* Understanding Python concepts and libraries.
* Helping identify and understand errors during development.
* Getting suggestions for debugging and code improvements.
* Organizing and improving the README documentation.

AI did not provide the complete implementation of the algorithm. The final algorithmic strategy, the adaptation of the pathfinding approach, the code, and the implementation decisions were developed and reviewed by me.



# Fly-in
![example](https://github.com/SANTOOS00/my_resource/blob/main/image/example_fly_in.png?raw=true)
GRaph explination: https://medium.com/basecs/a-gentle-introduction-to-graph-theory-77969829ead8
shortest path algo graph 


[algo yen's](https://www.linchenguang.com/2018/01/30/Yen-s-algorithm/)
[color](https://www.cambridgeincolour.com/tutorials/bit-depth.htm)
[color](https://en.wikipedia.org/wiki/Color_depth)
[color](https://www.renewedvision.com/blog/color-depth-and-channels-explained)






# Fly-in Drones

## Description

## Features

## Instructions

## Algorithm and Implementation Strategy

## Visual Representation

## Usage Example

## Error Handling

## Performance and Complexity

## Technical Choices

## Resources