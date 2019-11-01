# MCMC-of-Final-Year-Project-HKU
This repository mainly studies the Gibbs Sampler and vertex coloring problem (given a connected graph which consists of n vertices and q colors, we need to assign colors to each vertex such that no two adjacent vertices share the same color). Former scholars mainly focused on the minimum number of colors that could be used to color the graph, but here we focus on the application of Gibbs sampler on this problem. All the code was implemented from scratch.



## Reasons for using MCMC

We call a certain valid way to assign colors to each vertex in the graph as one valid configuration. Then, when we increase the number of vertices or the number of colors, the number of valid configurations increase in a large scale and it is really hard to count using combinatorics, which makes it really difficult if we wish to study some interesting things related to this problem. MCMC gives a feasible way to tackle this issue. Assume X<sub>1</sub> ... X<sub>N</sub> denote all valid configurations (note that N can be extramely large) and h(x) is a function whose domain is {X<sub>1</sub> .. X<sub>N</sub>}, then according to the theory that E(h(x)) = $\lim_{n\rightarrow+\infty} \frac{1}{n} \sum_{i=1}^n{h(x_i)}$ , we can "simulate" the process and use the average value to estimate the expectation. However, the main problem is, how to do the sampling (i.e. get $x_1 ... x_n$). 



## Questions we are concerned about
### About vertices
Then, assume the valid configurations are uniformly distributed, what is the average number of vertices which all occupy a same certain color (say, red)? What if we compute this quantity for every color and take the average? Intuitively, we may think that the average number of vertices which occupy a same certain color should be the same among each color, which is $$\frac{n}{q}$$. Then how do we prove it? If there is a method to "traverse" the configurations, will the average number of vertices occupying the same color converge during the traversal?

### About edges

If we define the type of an edge by the colors of the two vertices it connects, then  

##  

## Reasons of doing this research
When we increase the number of vertices or number of colors, the total number of valid configurations increase in a large scale which could hardly be counted. Thus

## Construction of the graph:
I used two methods to construct the graph:
### Method 01
We first random shuffle the vertices list (i.e. [0, 1, 2, ..., n-1]). Then iterate the vertices list. Each time we pop the head of the list (return the first element of the list and delete it). For the ith vertex, randomly connect it with k vertices among the first i-1 vertices.
### Method 02
Since for every connected graph, we can always delete some edges and let it become a tree, first, we generate a tree (which is already connected). When generating the tree, the number of subtrees for each non-leaf node is randomly assigned. Then, we add some more edges to this tree. 

## Initialization of colors
Initially, we set Null to all vertices' colors. We assign the colors to vertices in a random order. Every time we pick a vertex, search the colors of its neighbours and uniformly choose one from all the valid colors. 

## Iteration
