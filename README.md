# MCMC-of-Final-Year-Project-HKU
This repository mainly studies the Gibbs Sampler and vertex coloring problem (given a connected graph and q colors, we need to assign colors to each vertex such that no two adjacent vertices share the same color). Former scholars mainly focused on the minimum number of colors that could be used to color the graph, but here we focus on the application of Gibbs sampler on this problem. All the code was implemented from scratch.

## Construction of the graph:
I used two methods to construct the graph:
### Method 01
We first random shuffle the vertices list (i.e. [0, 1, 2, ..., n-1]). Then iterate the vertices list. Each time we pop the head of the list (return the first element of the list and delete it). For the ith vertex, randomly connect it with k vertices among the first i-1 vertices.
### Method 02
Since for every connected graph, we can always delete some edges and let it become a tree, first, we generate a tree (which is already connected). When generating the tree, the number of subtrees for each non-leaf node is randomly assigned. Then, we add some more edges to this tree. 

## Assignment of colors
Initially, we set Null to all vertices' colors. Then
