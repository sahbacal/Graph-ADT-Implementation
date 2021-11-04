# Course: CS261 - Data Structures
# Author: Austin Sahba
# Description: Graph Implementation

from collections import deque
import heapq


class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.flag = [0]
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        This method updates the previous vertex adjacency matrix to account for the new vertex, then adds a subarray
        for the new vertex.
        """

        holder = []

        for i in range(len(self.adj_matrix)):
            self.adj_matrix[i].append(0)

        for i in range(len(self.adj_matrix) + 1):
            holder.append(0)

        self.adj_matrix.append(holder)
        self.v_count += 1

        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        This method updates an edge location with the new edge weight.
        """

        if src < 0 or src >= self.v_count or dst < 0 or dst >= self.v_count or weight < 0 or src == dst:
            return

        self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        This method sets the edge at a certain location to zero.
        """

        if src < 0 or src >= self.v_count or dst < 0 or dst >= self.v_count:
            return

        self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        This method returns an array filled with integers corresponding to the vertices present.
        """
        output = []

        for i in range(len(self.adj_matrix)):
            output.append(i)

        return output

    def get_edges(self) -> []:
        """
        This method runs through all of the edges in the adjacency matrix and if any are greater than zero it
        adds a tuple containing the edge source, destination, and weight to the output array.
        """

        output = []

        for i in range(len(self.adj_matrix)):
            for j in range(len(self.adj_matrix[i])):

                if self.adj_matrix[i][j] != 0:
                    output.append((i, j, self.adj_matrix[i][j]))

        return output

    def is_valid_path(self, path: []) -> bool:
        """
        This method runs through the path array and checks the adjacency matrix to see if the adjacency list for the
        first node contains an edge to the node after it. If it doesnt, it returns False.
        """

        if len(path) == 0 or len(path) == 1:
            return True

        for i in range(len(path) - 1):

            if self.adj_matrix[path[i]][path[i + 1]] == 0:
                return False

        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        This method performs a depth first search starting with v_start. It adds all the current node children to
        the stack so they will be processed in ascending order. If a child has already been visited, it is not processed
        when pulled from a stack. If the v_end node is found, the visited array is returned.
        """

        if v_start < 0 or v_start >= len(self.adj_matrix):
            return []

        visited = []
        stack = [v_start]

        while len(stack) > 0:

            curr = stack.pop()
            if curr not in visited:

                visited.append(curr)
                if curr == v_end:
                    return visited

                for i in range(len(self.adj_matrix[curr]) - 1, -1, -1):

                    if self.adj_matrix[curr][i] > 0:
                        stack.append(i)

        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        This method performs a breadth first search of the graph. If v_end is found, the nodes visited array is
        immediately returned. Child nodes are added to the queue in ascending order.
        """

        if v_start < 0 or v_start >= len(self.adj_matrix):
            return []

        visited = []
        queue1 = deque([v_start])

        while len(queue1) > 0:

            curr = queue1.popleft()
            if curr not in visited:

                visited.append(curr)

                if curr == v_end:
                    return visited

                for i in range(len(self.adj_matrix[curr])):

                    if self.adj_matrix[curr][i] > 0:
                        queue1.append(i)

        return visited

    def has_cycle(self):
        """
        This method uses a backtracking helper function to determine if there are any cycles in the graph. For every
        starting node, it follows every path using backtracking and keeps a record of nodes visited in that current
        attempt. If it sees the same node twice in the same attempt, then it knows a cycle has occurred.
        """

        def backtracking(i, currDict):

            for j in range(len(self.adj_matrix[i])):

                if self.adj_matrix[i][j] > 0 and j in currDict:
                    self.flag = [1]

                elif self.adj_matrix[i][j] > 0 and j not in currDict:

                    currDict[j] = 1
                    backtracking(j, currDict)
                    del currDict[j]

        for i in range(len(self.adj_matrix)):

            currDict = {i: 1}
            backtracking(i, currDict)

        if self.flag == [0]:
            return False
        else:
            return True

    def dijkstra(self, src: int) -> []:
        """
        This method uses dijkstra's algorithm to find the shortest route from src to all other nodes it can reach.
        If it cannot find a path to a node, that distance is left as infinite. It uses a priority queue and only
        performs operations to a node if it hasn't been visited before, such as updating its distance and adding
        its children to the priority queue.
        """

        output = [float('inf')] * self.v_count
        visitedNodes = dict()
        priorityQueue1 = [(0, src)]

        while len(priorityQueue1) > 0:

            currDistance, currIndex = heapq.heappop(priorityQueue1)
            if currIndex not in visitedNodes:

                visitedNodes[currIndex] = currDistance
                for j in range(len(self.adj_matrix[currIndex])):

                    if self.adj_matrix[currIndex][j] != 0:

                        combinedDistance = currDistance + self.adj_matrix[currIndex][j]
                        heapq.heappush(priorityQueue1, (combinedDistance, j))

        for key in visitedNodes:
            output[key] = visitedNodes[key]

        return output


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)

    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')

    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))

    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')

    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)

    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
