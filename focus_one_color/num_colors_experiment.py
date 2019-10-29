import numpy as np
import graph_generator as gg
import coloring
import matplotlib.pyplot as plt
import random
import copy
import utils_converge as uc

# Hyper-parameters
q_range = [30, 70]  # number of color from 10 to 20
method = 1
vertices = 200
max_iter = 40000
# use the same initial coloring but repeat the iteration and use the average
repeat = 50

if method == 1:
    graph = gg.generate_m1(vertices=vertices, threshold=10)
    graph.add_edge()
    adjacency_matrix = graph.adjacency_matrix
elif method == 2:
    graph = gg.generate_m2(vertices=vertices, max_subtree=4, max_added_edge=8)
    graph.tree_constructor()
    graph.add_more_edges()
    adjacency_matrix = graph.adjacency_matrix

# delta is the maximum degree of the graph
delta = gg.max_degree(adjacency_matrix)
print("Validity of graph: ")
print(gg.bfs_check(adjacency_matrix))
print("Maximum degree: ")
print(delta)
print("Average degree: ")
print(gg.avg_degree(graph.adjacency_matrix))

time = [i for i in range(max_iter)]
num_plots = len(q_range)
colormap = plt.cm.gist_ncar
plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.jet(np.linspace(0, 1, num_plots))))
labels = []  # label for each curve in the plot
baseline = [0 for i in range(max_iter)]
plt.plot(time, baseline)
labels.append("baseline")
time_series_record = {}  # key is q, value is "adjusted_time_series_avg"

for q in q_range:
    color_graph = coloring.graph_coloring(adjacency_matrix, q)
    color_graph.initial_coloring()
    #experiments_record = uc.occurance_tracking(color_graph, q, max_iter, vertices, repeat)
    experiments_record = uc.multiprocessing_occurance_tracking(color_graph, q, max_iter, vertices, repeat)
    total_avg_occurance = uc.average_tracking(
        experiments_record, q, max_iter, repeat)
    objective_color = random.choice([i for i in range(q)])
    time_series_avg = uc.avg_of_one_color(total_avg_occurance, objective_color)
    adjusted_time_series_avg = [(i-(vertices/q)) for i in time_series_avg]
    time_series_record[q] = adjusted_time_series_avg
    plt.plot(time, adjusted_time_series_avg)
    labels.append("Num colors = " + str(q))
    print("Num of color: " + str(q))

plt.legend(labels, ncol=4, loc='upper center',
           bbox_to_anchor=[0.5, 1.1],
           columnspacing=1.0, labelspacing=0.0,
           handletextpad=0.0, handlelength=1.5,
           fancybox=True, shadow=True)

plt.show()
