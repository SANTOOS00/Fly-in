# from hube import Hub
# from typing import List, Dict
# from edge import Edge
# from itertools import count
# from edge import Edge
# import heapq


# class PriorityQueue:
#     def __init__(self):
#         self.heap = []
#         self.counter = count()

#     def push(self, priority, hub):
#         heapq.heappush(self.heap, (priority, next(self.counter), hub))

#     def pop(self):
#         cost, _, vertex = heapq.heappop(self.heap)
#         return cost, vertex

#     def is_empty(self):
#         return len(self.heap) != 0



# class Dijstra:
#     def __init__(self, network: Network) -> None:
#         self.distances: Dict[Hub, int] = {vertex: float('inf') for vertex in network.hubs.values()}
#         self.distances[network.start_hube] = 0

#     def run(self,
#             graph: Dict[Hub, List[tuple[Hub, Edge]]], start, end
#             ) -> List[Hub]:

#         priority_queue = PriorityQueue()
#         priority_queue.push(0, start)
#         paths = {vertex: None for vertex in graph.keys()}
#         while priority_queue.is_empty():
#             cost, hub = priority_queue.pop()
#             if hub == end:
#                 break
#             if cost < self.distances[hub]:
#                 continue
#             for vertex, edgs in graph[hub]:
#                 distance = edgs.meta['max_link_capacity'] + cost
                
#                 if distance < self.distances[vertex]:
#                     self.distances[vertex] = distance
#                     priority_queue.push(distance, vertex)
#                     paths[vertex] = hub
#         path = []
#         current = end
#         while current is not None:
#             path.insert(0, current)
#             current = paths[current]
