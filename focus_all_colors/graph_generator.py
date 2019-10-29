import numpy as np
import random

# In this method, we first random shuffle the vertices list
# Then iterate the vertices list, each time pick a new vertex
# At time n, randomly connect the new vertex with k vertices among the first n-1 vertices


class generate_m1:
    def __init__(self, vertices, threshold):
        self.vertices = vertices  # vertices is the number of vertices
        self.adjacency_matrix = np.array([np.zeros(vertices, dtype=int) for i in range(
            vertices)])  # initialize the adacency matrix
        self.threshold = threshold  # threshold is actually k

    def add_edge(self):
        vertices_list = [i for i in range(self.vertices)]
        random.shuffle(vertices_list)
        explored = []
        for i in range(len(vertices_list)):
            if i == 0:
                explored.append(vertices_list[i])
            else:
                if len(explored) <= self.threshold:
                    picked_vertex = random.choice(explored)
                    self.adjacency_matrix[picked_vertex][vertices_list[i]] = 1
                    self.adjacency_matrix[vertices_list[i]][picked_vertex] = 1
                else:
                    picked_idx = np.random.choice(
                        len(explored), self.threshold, replace=False)
                    for idx in picked_idx:
                        picked_vertex = explored[idx]
                        self.adjacency_matrix[picked_vertex][vertices_list[i]] = 1
                        self.adjacency_matrix[vertices_list[i]
                                              ][picked_vertex] = 1
                explored.append(vertices_list[i])

    def show(self):
        print(self.adjacency_matrix)

    def add_connectivity(self, edges_added):
        vertices_list = [i for i in range(self.vertices)]
        for i in range(edges_added):
            pair = random.sample(vertices_list, 2)
            while self.adjacency_matrix[pair[0]][pair[1]] == 1:
                pair = random.sample(vertices_list, 2)
            self.adjacency_matrix[pair[0]][pair[1]] = 1


# First, generate a tree (which is already connected)
# Then, add some more edges to this tree
class generate_m2():
    def __init__(self, vertices, max_subtree, max_added_edge):
        self.vertices = vertices  # number of vertices
        self.adjacency_matrix = np.array([np.zeros(vertices, dtype=int) for i in range(
            vertices)])  # initialize the adjacency matrix
        self.max_subtree = max_subtree  # maximum subtree of each vertex
        # maximum edges added after tree contruction
        self.max_added_edge = max_added_edge

    def tree_constructor(self):
        vertices_list = [i for i in range(self.vertices)]
        random.shuffle(vertices_list)
        i = j = 0
        ending = False
        while i < self.vertices and ending == False:
            if self.vertices - i - 1 >= self.max_subtree:
                subtree = random.randint(1, self.max_subtree)
            elif self.vertices - i - 1 > 0 and self.vertices - i - 1 < self.max_subtree:
                subtree = random.randint(1, (self.vertices-i-1))
            else:
                subtree = 0
                ending = True
            i += subtree
            for itr in range(subtree):
                self.adjacency_matrix[j][i-itr] = 1
                self.adjacency_matrix[i-itr][j] = 1
            j += 1

    def add_more_edges(self):
        for i in range(self.max_added_edge):
            vertex_pair = np.random.choice(self.vertices, 2, replace=False)
            while self.adjacency_matrix[vertex_pair[0]][vertex_pair[1]] == 1:
                vertex_pair = np.random.choice(self.vertices, 2, replace=False)
            self.adjacency_matrix[vertex_pair[0]][vertex_pair[1]] = 1
            self.adjacency_matrix[vertex_pair[1]][vertex_pair[0]] = 1

    def show(self):
        print(self.adjacency_matrix)

    def add_connectivity(self, edges_added):
        vertices_list = [i for i in range(self.vertices)]
        for i in range(edges_added):
            pair = random.sample(vertices_list, 2)
            while self.adjacency_matrix[pair[0]][pair[1]] == 1:
                pair = random.sample(vertices_list, 2)
            self.adjacency_matrix[pair[0]][pair[1]] = 1

# use BFS to check if the graph is connected
# connected iff from the first vertex, we can go to any other vertex


def bfs_check(adjacency_matrix):
    visited = {}
    queue = []
    for i in range(len(adjacency_matrix)):
        visited[i] = False
    queue.append(0)
    visited[0] = True
    while len(queue) != 0:
        head = queue.pop(0)
        for j in range(len(adjacency_matrix[head])):
            if j != head and visited[j] == 0:
                queue.append(j)
                visited[j] = True
    for vertex in visited.keys():
        if visited[vertex] == False:
            return False
    return True

# This function checks the average degree of a graph
# We do not want the average degree to be too large


def avg_degree(adjacency_matrix):
    return adjacency_matrix.sum()/len(adjacency_matrix)

# This function returns the maximum degree of a graph


def max_degree(adjacency_matrix):
    largest = 0
    for i in range(len(adjacency_matrix)):
        i_degree = 0
        for j in range(len(adjacency_matrix[i])):
            if adjacency_matrix[i][j] == 1:
                i_degree += 1
        if i_degree > largest:
            largest = i_degree
    return largest
