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

# compute the occurance of a color after each single iteration
# call initial_coloring before passing color_graph into the function


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

def average_tracking(experiments_record, q, max_iter, repeat):
    color_occurance = {key: 0 for key in range(q)}
    total_avg_occurance = {key: color_occurance for key in range(max_iter)}
    for aggregate_occurance in experiments_record.values():
        avg_occurance = {}
        for itr in aggregate_occurance.keys():
            avg_occurance[itr] = {
                color: aggregate_occurance[itr][color]/(itr+1) for color in range(q)}
        nested_dict_addition(total_avg_occurance, avg_occurance)
    for itr in total_avg_occurance.keys():
        total_avg_occurance[itr] = {
            k: v/repeat for k, v in total_avg_occurance[itr].items()}
    return total_avg_occurance


def avg_of_one_color(total_avg_occurance, color):
    time_series_avg = []
    for itr in total_avg_occurance.keys():
        time_series_avg.append(total_avg_occurance[itr][color])
    return time_series_avg


def series_fluctuation(time_series_avg):
    fluctuate = [time_series_avg[i+1] - time_series_avg[i]
                 for i in range(len(time_series_avg)-1)]
    return fluctuate


def variance(time_series_avg):
    return np.var(time_series_avg)

# return the position where the previous 1000 elements are all <= threshold
# in this case we determine that this sequence has converged


def converge_stop(sequence, threshold):
    for i in range(len(sequence)):
        if i >= 100:
            checker = True
            for j in sequence[i-100:i]:
                if abs(j) > threshold:
                    checker = False
                    break
            if checker == True:
                return i
    return 0


def converge_stop_test(sequence_A, sequence_B):
    return converge_stop(sequence_A, 0.01), converge_stop(sequence_B, 0.01)

# test the ratio of An/Bn, if it converges to 1, same speed
# if positive infinity, then B converges faster
# if zero, then A converges faster


def ratio_test(sequence_A, sequence_B):
    for i in range(len(sequence_A)):
        if sequence_A[i] == 0:
            sequence_A[i] += 0.001
        if sequence_B[i] == 0:
            sequence_B[i] += 0.001
    ratio = [abs(sequence_A[i]/sequence_B[i]) for i in range(len(sequence_A))]
    return ratio
