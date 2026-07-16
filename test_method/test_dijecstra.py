import heapq

def dijkstra(graph, start, end):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    
    priority_queue = [(0, start)]
    predecessors = {node: None for node in graph}
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_node == end:
            break
            
        if current_distance > distances[current_node]:
            continue
            
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = predecessors[current]
        
    return distances[end], path

graph = {
    1: [[2, 7], [3, 9], [6, 14]],
    2: [[1, 7], [3, 10], [4, 15]],
    3: [[1, 9], [2, 10], [6, 2], [4, 11]],
    4: [[3, 11], [2, 15], [5, 6]],
    5: [[6, 9], [4, 6]],
    6: [[1, 14], [3, 2], [5, 9]]
}

                
start_node = 1
end_node = 5

min_distance, shortest_path = dijkstra(graph, start_node, end_node)

print(graph)
print(min_distance, shortest_path)