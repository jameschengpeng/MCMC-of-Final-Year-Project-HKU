import random
import copy

# adjacency_matrix should be constructed beforehand
# q is the number of colors


class graph_coloring():
    def __init__(self, adjacency_matrix, q):
        self.adjacency_matrix = adjacency_matrix
        self.q = q
        self.neighbors = {}
        for i in range(len(self.adjacency_matrix)):
            i_neighbor = []
            for j in range(len(self.adjacency_matrix[i])):
                if self.adjacency_matrix[i][j] == 1:
                    i_neighbor.append(j)
            self.neighbors[i] = i_neighbor
        self.usable_colors = set(i for i in range(self.q))

    def initial_coloring(self):
        coloring = {key: None for key in range(len(self.adjacency_matrix))}
        # choose an arbitrary ordering of the vertices, and color them one at a time,
        # labeling each vertex with a color not already used by any of its neighbors
        vertices_idx = [i for i in range(len(self.adjacency_matrix))]
        random.shuffle(vertices_idx)
        for i in vertices_idx:
            invalid_colors = []
            for j in self.neighbors[i]:
                if coloring[j] != None:
                    invalid_colors.append(coloring[j])
            valid_colors = list(self.usable_colors - set(invalid_colors))
            if len(valid_colors) == 0:
                print("Error when assigning colors! Try again!")
                break
            coloring[i] = random.choice(valid_colors)
        # self.coloring is a dict, key is vertex index, value is color
        self.coloring = coloring
        # record the initial coloring for the repeat of experiment with the same initial coloring
        self.primitive_coloring = coloring

    def check_valid(self):
        for i in self.neighbors.keys():
            for j in self.neighbors[i]:
                if self.coloring[i] == self.coloring[j]:
                    return False
        return True

    # vertex_idx defines which vertex we wish to update
    def single_iteration(self, vertex_idx):
        invalid_colors = []
        for j in self.neighbors[vertex_idx]:
            if self.coloring[j] not in invalid_colors:
                invalid_colors.append(self.coloring[j])
        color_assigned = random.choice(list(self.usable_colors))
        if color_assigned not in invalid_colors:
            self.coloring[vertex_idx] = color_assigned
        else:
            pass

    def refresh(self):
        self.coloring = self.primitive_coloring.copy()
