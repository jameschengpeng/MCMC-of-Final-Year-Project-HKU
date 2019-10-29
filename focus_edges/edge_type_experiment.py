import random
import coloring
import graph_generator as gg
import utils
import matplotlib.pyplot as plt
import copy
import numpy as np

# Hyper-parameters
method = 1
vertices = 200
max_iter = 70000
q = 20
edges_considered = 10 # how many types of edge we wish to consider
# use the same initial coloring but repeat the iteration and use the average
repeat = 5

edges_list = []
edge_type = random.sample([i for i in range(q)], 2)
edge_type.sort()
edge_type = tuple(edge_type)
edges_list.append(edge_type)
counter = 1
while (edge_type not in edges_list) or counter < 10:
  counter += 1
  edge_type = random.sample([i for i in range(q)], 2)
  edge_type.sort()
  edge_type = tuple(edge_type)
  edges_list.append(edge_type)

def graph_constructor(method):
    if method == 1:
        graph = gg.generate_m1(vertices=vertices, threshold=10)
        graph.add_edge()
    elif method == 2:
        graph = gg.generate_m2(vertices=vertices, max_subtree=4, max_added_edge=8)
        graph.tree_constructor()
        graph.add_more_edges()
    return graph

graph = graph_constructor(method = method)
adjacency_matrix = graph.adjacency_matrix
print("Graph constructed")

delta = gg.max_degree(adjacency_matrix)
print("Validity of graph: ")
print(gg.bfs_check(adjacency_matrix))
print("Maximum degree: ")
print(delta)
print("Average degree: ")
print(gg.avg_degree(adjacency_matrix))

color_graph = coloring.graph_coloring(adjacency_matrix, q)
color_graph.initial_coloring()

time = [i for i in range(max_iter)]
num_plots = 1 + len(edges_list)
colormap = plt.cm.gist_ncar
plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.jet(np.linspace(0, 1, num_plots))))
labels = []  # label for each curve in the plot
num_edges = len(utils.edge_pair(color_graph))
baseline = [((2*num_edges)/(q*(q-1))) for i in range(max_iter)]
plt.plot(time, baseline)
labels.append("baseline")
time_series_record = {}  # key is edges added, value is "adjusted_time_series_avg"


avg_occurance = utils.multi_thread_repeat(repeat, color_graph, max_iter, vertices)
#avg_occurance = utils.simple_repeat(repeat, color_graph, max_iter, vertices)
for edge_type in edges_list:
  time_series = utils.edge_type_time_series(edge_type, avg_occurance)
  plt.plot(time, time_series)
  labels.append("Edge type: " + str(edge_type))

plt.legend(labels, ncol=4, loc='upper center',
           bbox_to_anchor=[0.5, 1.1],
           columnspacing=1.0, labelspacing=0.0,
           handletextpad=0.0, handlelength=1.5,
           fancybox=True, shadow=True)

plt.show()
