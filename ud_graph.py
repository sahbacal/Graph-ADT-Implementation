# Course: 261 Data Structures
# Author: Austin Sahba
# Description: Graph Implementation

from collections import deque


class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        This method adds a vertex to the dictionary listed as self.adj_list. If the vertex was already present
        in the dictionary, the method does not do anything.
        """

        if v not in self.adj_list:
            self.adj_list[v] = []

    def add_edge(self, u: str, v: str) -> None:
        """
        This method first confirms that the vertexes are not equal to each other. It then adds both vertexes to the
        dictionary as keys if they are not already present. Lastly it adds each vertex to the other vertex adjacency
        list.
        """

        if u != v:

            self.add_vertex(u)
            self.add_vertex(v)

            if v not in self.adj_list[u]:
                self.adj_list[u].append(v)

            if u not in self.adj_list[v]:
                self.adj_list[v].append(u)

    def remove_edge(self, v: str, u: str) -> None:
        """
        This method checks to see if both v and u are keys in the dictionary. If so, then if they are present as
        values in each others adjacency list, they are removed.
        """

        if v in self.adj_list and u in self.adj_list:

            if v in self.adj_list[u]:
                self.adj_list[u].remove(v)

            if u in self.adj_list[v]:
                self.adj_list[v].remove(u)

    def remove_vertex(self, v: str) -> None:
        """
        This method checks if v is a key in the dictionary. If so, it first deletes that key entry. Then it checks
        all other keys in the dictionary if v is a value for them, and removes v each time.
        """

        if v in self.adj_list:

            del self.adj_list[v]
            for key in self.adj_list:

                if v in self.adj_list[key]:
                    self.adj_list[key].remove(v)

    def get_vertices(self) -> []:
        """
        This method creates an empty array named output, then runs through the dictionary and adds each key to the
        array. It then returns output.
        """

        output = []

        for key in self.adj_list:
            output.append(key)

        return output

    def get_edges(self) -> []:
        """
        This function creates an output array and a dictionary named already used. It then runs through all keys
        in the self.adj_list dictionary and runs through all corresponding values. If the tuple (key, value) is not in
        the dictionary already used, then it adds the tuple to the output array and adds the reverse tuple (value, key)
        to the already used dictionary to prevent repeats from occurring.
        """

        output = []
        alreadyUsed = dict()

        for key in self.adj_list:

            for value in self.adj_list[key]:

                if (key, value) not in alreadyUsed:
                    output.append((key, value))
                    alreadyUsed[(value, key)] = 1

        return output

    def is_valid_path(self, path: []) -> bool:
        """
        This method first checks path inputs of length 1 and confirms that the vertex is in the dictionary, or else
        it returns false. It then runs through the path array and checks each vertex and its neighbor. If all pairs are
        both in the dictionary and the second vertex is in the first vertexes adjacency list, the method will return
        True. If not, it will return false.
        """

        if len(path) == 1:

            if path[0] not in self.adj_list:
                return False

        for i in range(len(path) - 1):

            if path[i] not in self.adj_list or path[i + 1] not in self.adj_list:
                return False

            if path[i + 1] not in self.adj_list[path[i]]:
                return False

        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        This method creates a visited dictionary. It then checks the case where the given starting node is not in
        the self.adj_list, to which is would return an empty array. It then initiates a stack with the starting node
        and proceeds to do a depth first search, keeping track of the order visited. Children are added to the
        stack in alphabetical order. If a target node was included and it is found in the search, a visited order
        array is returned. Otherwise, this array is returned at the end.
        """

        visited = dict()

        if v_start not in self.adj_list:
            return []

        stack1 = [v_start]

        while len(stack1) > 0:

            curr = stack1.pop()

            if curr not in visited:
                visited[curr] = 1

                if curr == v_end:
                    output = []

                    for key in visited:
                        output.append(key)

                    return output

                children = []

                for child in self.adj_list[curr]:
                    children.append(child)

                sortedChildren = sorted(children)

                for i in range(len(sortedChildren) - 1, -1, -1):
                    stack1.append(sortedChildren[i])

        output = []

        for key in visited:
            output.append(key)

        return output

    def bfs(self, v_start, v_end=None) -> []:
        """
        This method creates a visited dictionary and checks for the case where the node is not in self.adj_list. It
        then creates a deque with the start node in it. It proceeds to do a breadth first search. If it finds the
        provided end node, it returns an array with all visited nodes. For the children of a node, it sorts them then
        adds them to the end of the queue.
        """

        visited = dict()

        if v_start not in self.adj_list:
            return []

        queue1 = deque([v_start])

        while len(queue1) > 0:

            curr = queue1.popleft()

            if curr not in visited:
                visited[curr] = 1

                if curr == v_end:
                    output = []

                    for key in visited:
                        output.append(key)

                    return output

                children = []

                for child in self.adj_list[curr]:
                    children.append(child)

                sortedChildren = sorted(children)

                for i in range(len(sortedChildren)):
                    queue1.append(sortedChildren[i])

        output = []

        for key in visited:
            output.append(key)

        return output

    def count_connected_components(self):
        """
        This method creates a dictionary to keep track of which nodes have been visited already. It then goes
        through every node in the self.adj_list and checks if it has been visited already. If it hasn't, it increases
        the component number and performs a breadth first search at that node. For each node visited in the BFS, it
        adds this node to the visited already dictionary. Once the whole process is complete, it returns the component
        number.
        """

        numberOfComponents = 0

        nodesVisitedAlready = dict()

        for key in self.adj_list:

            if key not in nodesVisitedAlready:

                numberOfComponents += 1
                bfsNodes = self.bfs(key)

                for element in bfsNodes:
                    if element not in nodesVisitedAlready:
                        nodesVisitedAlready[element] = 1

        return numberOfComponents

    def has_cycle(self):
        """
        This method uses a breadth first search on every self.adj_list element that it hasn't visited yet to ensure
        it does not miss any separate components. In the BFS, once it adds a child node to the queue, it deletes
        the child node's reference back to the previous node. Therefore, if that specific BFS returns to a node
        previously visited, we know a cycle exists.
        """

        nodesVisitedAlready = dict()

        for key in self.adj_list:

            if key not in nodesVisitedAlready:

                currVisited = dict()
                queue1 = deque(key)

                while len(queue1) > 0:

                    curr = queue1.popleft()

                    if curr not in nodesVisitedAlready:
                        nodesVisitedAlready[curr] = 1

                    if curr in currVisited:
                        return True

                    elif curr not in currVisited:
                        currVisited[curr] = 1

                        for child in self.adj_list[curr]:
                            queue1.append(child)
                            if curr in self.adj_list[child]:
                                self.adj_list[child].remove(curr)

        return False


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)

    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)

    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')

    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))

    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')

    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()

    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
