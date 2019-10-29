import random
import math
import numpy as np
import copy
from multiprocessing import Pool

def dict_addition(dict1, dict2):
    added = {}
    for k in dict1.keys():
        added[k] = dict1[k]
    for k in dict2.keys():
        if k in added.keys():
            added[k] += dict2[k]
        else:
            added[k] = dict2[k]
    return added

def avg_list_dict(list_dict):
    avg = {}
    for elem_dict in list_dict:
        avg = dict_addition(avg, elem_dict)
    for k in avg.keys():
        avg[k] = avg[k] / len(list_dict)
    return avg

def edge_pair(color_graph):
    num_vertices = len(color_graph.adjacency_matrix)
    edges = []
    for i in range(num_vertices-1):
        for j in range(i+1, num_vertices):
            if color_graph.adjacency_matrix[i][j] == 1:
                edges.append((i,j))
    return edges

# for an edge, if the two vertices it connects are in colors p & q (p < q)
# then we define this edge as type (p,q)
# this function returns a dictionary, key is edge type, value is occurences in this graph

def count_edge_type(color_graph, edges):
    edge_type_book = {}
    for pair in edges:
        edge_type = [color_graph.coloring[pair[0]], color_graph.coloring[pair[1]]]
        edge_type.sort()
        edge_type = tuple(edge_type)
        if edge_type in edge_type_book.keys():
            edge_type_book[edge_type] += 1
        else:
            edge_type_book[edge_type] = 1
    return edge_type_book

def edge_tracking(color_graph, max_iter, vertices, seq_repeat):
    aggregate_occurance = {}
    color_graph.refresh()
    edges = edge_pair(color_graph)
    for itr in range(max_iter):
        vertex_idx = itr % vertices
        color_graph.single_iteration(vertex_idx)
        edge_type_book = count_edge_type(color_graph, edges)
        if itr == 0:
            aggregate_occurance[itr] = edge_type_book
        else:
            pre = aggregate_occurance[itr-1].copy()
            aggregate_occurance[itr] = dict_addition(pre, edge_type_book)
    print("Finished the " + str(seq_repeat) + "th repeat")
    return aggregate_occurance

def multi_thread_repeat(repeat, color_graph, max_iter, vertices):
    param = [(color_graph, max_iter, vertices, i) for i in range(repeat)]
    pool = Pool()
    repeat_result = pool.starmap(edge_tracking, param)
    avg_occurance = {} # key: itr, value: a dictionary whose key is type of edge, value is average num of occurence
    for itr in range(max_iter):
        list_dict = [single_result[itr] for single_result in repeat_result]
        avg_aggregate_occurance = avg_list_dict(list_dict)
        avg_occurance[itr] = {k: v/(itr+1) for k, v in avg_aggregate_occurance.items()}
    return avg_occurance

def simple_repeat(repeat, color_graph, max_iter, vertices):
    repeat_result = []
    for i in range(repeat):
        repeat_result.append(edge_tracking(color_graph, max_iter, vertices, i))
    avg_occurance = {} # key: itr, value: a dictionary whose key is type of edge, value is average num of occurence
    for itr in range(max_iter):
        list_dict = []
        for single_result in repeat_result:
            list_dict.append(single_result[itr])
        avg_aggregate_occurance = avg_list_dict(list_dict)
        avg_occurance[itr] = {k: v/(itr+1) for k, v in avg_aggregate_occurance.items()}
    return avg_occurance

def edge_type_time_series(edge, avg_occurance):
    return [avg_occurance[k][edge] for k in avg_occurance.keys()]
