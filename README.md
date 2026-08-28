
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


## Features

- **Dijkstra's Algorithm**: Efficient pathfinding to calculate the shortest routes between zones.
- **Multi-Drone Scheduling**: Simultaneous movement of multiple drones with conflict resolution.
- **Zone Type System**: Four zone types (normal, restricted, priority, blocked) with different traversal costs and behaviors.
- **Capacity Management**: Enforces maximum drone limits on both zones and connections.
- **Alternative Path Generation**: Inspired by Yen's K-Shortest Paths idea to find multiple viable routes.
- **Dynamic Drone Routing**: Assigns drones to paths that minimize total simulation turns while respecting capacities.
- **Turn-by-Turn Simulation**: Precise simulation with waiting logic when zones or connections are at capacity.
- **Colored Terminal Visualization**: Rich-formatted output with color-coded zones for enhanced readability.
- **Comprehensive Input Validation**: Validates map file structure, metadata, and graph connectivity with clear error messages.



## Algorithm and Implementation Strategy

### Pathfinding Core

The project uses Dijkstra's algorithm as the core pathfinding engine. The algorithm computes the lowest-cost route between the start and destination zones using a min-heap priority queue and distance table. Zone types translate into movement costs:

- `normal`: cost = 1
- `priority`: cost = 0 (treated as faster traversal)
- `restricted`: cost = 2 (higher traversal cost)
- `blocked`: impassable (infinite cost)

After finding a shortest path, the implementation can modify the graph (temporarily remove selected edges) and re-run Dijkstra to generate alternative routing options for subsequent drones. This is an adaptation of the general idea behind Yen's K-Shortest Paths algorithm but simplified for the project's constraints.

### Multi-Path Generation and Assignment

1. Generate the first shortest path with Dijkstra from start to end.
2. Temporarily remove or penalize edges used by that path and re-run Dijkstra to find another distinct path.
3. Repeat until enough alternative paths are available or no more routes exist.
4. Evaluate combinations of assigning drones to available paths and simulate to estimate total turns.
5. Choose the assignment that minimizes the total number of simulation turns while respecting capacity constraints.

### Scheduling and Simulation

- Simulation progresses in discrete turns. During each turn:
  - Each drone attempts to move forward along its assigned path.
  - Before moving, the simulation checks zone and edge capacities.
  - If a move would violate a capacity, the drone waits in place.
  - All moves for the turn are applied simultaneously (subject to capacity checks), preventing order-dependent advantages.
- The simulation ends when all drones have reached the destination.

### Conflict Resolution

- If multiple drones contend for the same zone or edge, priority is resolved by:
  1. Preserving previously occupied positions (a drone already in a zone keeps it unless it moves out).
  2. Allowing movement only when destination capacity permits.
  3. Breaking ties deterministically (for example, by drone ID order) to ensure reproducible results.

## Visual Representation

The program outputs a human-readable turn-by-turn log to the terminal, optionally enriched with color using the project's color utilities. Typical output includes:

- Colored zone names and coordinates (when color metadata is provided in the map file).
- Drone identifiers and their current positions each turn.
- The global turn counter and a final summary when the simulation ends.

Color metadata in the map file follows this form on hub lines: `[color=red]`. The code maps CSS-like color names (or hex values) to terminal colors.

## Usage Example

### Example Map File (maps/simple_example.txt)

```text
nb_drones: 4

start_hub: start 0 0 [color=green]
hub: junction 1 0 [color=yellow max_drones=2]
hub: path_a 2 1 [color=blue]
hub: path_b 2 -1 [color=blue]
end_hub: goal 3 0 [color=red]

connection: start-junction [max_link_capacity=2]
connection: junction-path_a
connection: junction-path_b
connection: path_a-goal
connection: path_b-goal
```

### Running the Simulation

```bash
make install
```


```bash
make run MAP_DEF=maps/simple_example.txt
```

Expected behavior:
- The program parses and validates the map file.
- It generates one or more paths from `warehouse` to `delivery`.
- It assigns the 3 drones to the available paths and runs the turn-by-turn simulation.
- The terminal prints each turn's movements and a final line with the minimum number of turns required for all drones to reach the destination.

Sample output fragment:

```
 D1-junction D2-junction
 D1-path_b D2-path_a D3-junction D4-junction
 D1-goal D2-goal D3-path_b D4-path_a
 D3-goal D4-goal
4

```

## Error Handling

The project includes focused error checking with descriptive messages. Common errors include:

- File not found or unreadable map file — check the path and permissions.
- Malformed map lines or invalid metadata — the parser reports the offending line and a message.
- Missing start or end hub — both are required and must be unique.
- Disconnected graph (no path from start to end) — ensure the map's connections create at least one route.
- Invalid zone types or metadata values — use only supported types and valid key=value pairs.

Errors are surfaced as human-readable messages and (where appropriate) the program exits with a non-zero status.

## Performance and Complexity

- Dijkstra's algorithm runs in O((V + E) log V) time per path computation (V = number of zones, E = number of connections).
- Generating multiple alternative paths (k paths) requires roughly O(k × (V + E) log V) due to repeated Dijkstra runs.
- The simulation advances turn-by-turn and costs O(T × D) time where T is total turns and D is number of drones.

Space complexity is O(V + E) for the adjacency representation plus O(D) for drone tracking.

Optimization notes:
- Using a binary heap (heapq) for Dijkstra's priority queue minimizes overhead.
- Avoiding full re-computation when only minor graph changes are needed can help (future improvement).

## Technical Choices

- Dijkstra's algorithm: chosen for guaranteed shortest-path results with non-negative weights and no heuristic requirement.
- Adjacency list: space-efficient representation for sparse graphs.
- Python `heapq`: simple and effective priority queue for Dijkstra.
- Custom exceptions and clear parser errors to improve debuggability.
- Rich-based terminal coloring (or equivalent) to keep output readable across platforms.

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