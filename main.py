import heapq
import sys
import time
import random
import statistics
from tabulate import tabulate

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[] for _ in range(vertices)]

    def add_edge(self, src, dest, weight):
        self.graph[src].append((dest, weight))
        self.graph[dest].append((src, weight))

    def prim_mst(self):
        mst = []
        visited = [False] * self.V
        min_heap = [(0, 0)]  # (weight, vertex)

        while min_heap:
            weight, vertex = heapq.heappop(min_heap)
            if visited[vertex]:
                continue

            visited[vertex] = True
            mst.append((vertex, weight))

            for neighbor, neighbor_weight in self.graph[vertex]:
                if not visited[neighbor]:
                    heapq.heappush(min_heap, (neighbor_weight, neighbor))

        return mst

def analyze_performance(graph):
    start_time = time.time()

    # Run Prim's Algorithm for adjacency list representation
    mst_adj_list = graph.prim_mst()

    end_time = time.time()
    execution_time_adj_list = end_time - start_time

    # Space Complexity for adjacency list
    space_complexity_adj_list = sys.getsizeof(graph.graph) + sys.getsizeof(mst_adj_list) + sys.getsizeof(
        heapq) + sys.getsizeof(set())

    # Graph Density
    edge_count = sum(len(adj_list) for adj_list in graph.graph)
    max_edges = (graph.V * (graph.V - 1)) // 2  # Complete graph
    density = edge_count / max_edges

    # Distribution of Edge Weights
    edge_weights = [weight for adj_list in graph.graph for _, weight in adj_list]
    weight_mean = statistics.mean(edge_weights)
    weight_median = statistics.median(edge_weights)
    weight_stdev = statistics.stdev(edge_weights)

    return [graph.V, "Undirected", execution_time_adj_list, space_complexity_adj_list, density, weight_mean,
            weight_median, weight_stdev]

# Example usage
if __name__ == "__main__":
    table_data = []

    # Vary the number of vertices to observe the performance
    for num_vertices in [10, 50, 100, 1000, 10000, 100000, 1000000]:
        # Create a graph with the specified number of vertices
        g = Graph(num_vertices)

        # Add random edges to the graph (adjust as needed)
        for _ in range(num_vertices * 2):  # Adjust the number of edges as needed
            src = random.randint(0, num_vertices - 1)
            dest = random.randint(0, num_vertices - 1)
            weight = random.randint(1, 100)  # Adjust the weight range as needed
            g.add_edge(src, dest, weight)

        # Analyze performance for the current graph size
        performance_data = analyze_performance(g)
        table_data.append(performance_data)

    # Print results in tabular format
    headers = ["Vertices", "Graph Type", "Execution Time (s)", "Space Complexity (bytes)", "Graph Density",
               "Mean Edge Weight", "Median Edge Weight", "Edge Weight Standard Deviation"]
    print(tabulate(table_data, headers=headers))