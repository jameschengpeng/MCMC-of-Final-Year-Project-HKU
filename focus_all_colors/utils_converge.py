import random
import math
import numpy as np
import copy
from multiprocessing import Pool

def dict_addition(dict1, dict2):
    new_dict = {}
    for key in dict1.keys():
        new_dict[key] = dict1[key] + dict2[key]
    return new_dict

def nested_dict_addition(n_dict1, n_dict2):
    for key in n_dict1.keys():
        n_dict1[key] = dict_addition(n_dict1[key], n_dict2[key])

# compute the number of occurances of each color in a certain coloring
# coloring is a dictionary, key is vertex, value is color


def color_in_graph(coloring, q):
    color_occurance = {key: 0 for key in range(q)}
    for vertex in coloring.keys():
        color_occurance[coloring[vertex]] += 1
    return color_occurance

# compute the occurance of each color after each single iteration
# call initial_coloring before passing color_graph into the function
# return a dictionary, key is iterator, value is another dictionary whose key is color idx and value is total number of occurence

def occurance_tracking(color_graph, q, max_iter, vertices, repeat):
    experiments_record = {}
    for i in range(repeat):
        # key is itr, value is a dictionary whose key is color index,
        # value is total occurance of this color up to this iteration
        aggregate_occurance = {}
        if i != 0:
            color_graph.refresh()
        for itr in range(max_iter):
            vertex_idx = itr % vertices
            color_graph.single_iteration(vertex_idx)
            new_coloring = color_graph.coloring.copy()
            color_occurance = color_in_graph(new_coloring, q)
            if itr == 0:
                aggregate_occurance[itr] = color_occurance
            else:
                pre = aggregate_occurance[itr-1].copy()
                aggregate_occurance[itr] = dict_addition(pre, color_occurance)
        experiments_record[i] = aggregate_occurance
    return experiments_record

################################################# This part is an alternative approach by using multiprocessing
def occurance_tracking_without_repeat(color_graph, q, max_iter, vertices):
    aggregate_occurance = {}
    color_graph.refresh()
    for itr in range(max_iter):
        vertex_idx = itr % vertices
        color_graph.single_iteration(vertex_idx)
        new_coloring = color_graph.coloring.copy()
        color_occurance = color_in_graph(new_coloring, q)
        if itr == 0:
            aggregate_occurance[itr] = color_occurance
        else:
            pre = aggregate_occurance[itr-1].copy()
            aggregate_occurance[itr] = dict_addition(pre, color_occurance)
    return aggregate_occurance 

def multiprocessing_occurance_tracking(color_graph, q, max_iter, vertices, repeat):
    param = [(color_graph, q, max_iter, vertices) for i in range(repeat)]
    pool = Pool()
    experiments_record = {}
    repeat_result = pool.starmap(occurance_tracking_without_repeat, param)
    for i in range(repeat):
        experiments_record[i] = repeat_result[i]
    return experiments_record
#################################################

# return a dictionary, key is iterator, value is another dictionary
# whose key is color idx, value is the average num of occurence up to this iteration

def average_tracking(experiments_record, q, max_iter, repeat):
    color_occurance = {key: 0 for key in range(q)}
    total_avg_occurance = {key: color_occurance for key in range(max_iter)}
    for aggregate_occurance in experiments_record.values():
        avg_occurance = {}
        for itr in aggregate_occurance.keys():
            avg_occurance[itr] = {color: aggregate_occurance[itr][color]/(itr+1) for color in range(q)}
        nested_dict_addition(total_avg_occurance, avg_occurance)
    for itr in total_avg_occurance.keys():
        total_avg_occurance[itr] = {k: (v/repeat) for k, v in total_avg_occurance[itr].items()}
    return total_avg_occurance

# dict1 dict2 are two dictionaries
# key is color idx, value is avg num of occurences

def total_variation_distance(dict1, dict2, q):
    return (1/q) * sum([abs(dict1[i] - dict2[i]) for i in dict1.keys()])

def distance_tracking(total_avg_occurance, vertices, q):
    expectation = {k: (vertices/q) for k in range(q)}
    distance = []
    for itr in total_avg_occurance.keys():
        distance.append(total_variation_distance(total_avg_occurance[itr], expectation, q))
    return distance
    