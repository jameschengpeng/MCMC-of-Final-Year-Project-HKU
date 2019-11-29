# MCMC-of-Final-Year-Project-HKU

This repository mainly studies the Gibbs Sampler and vertex coloring problem (There is a connected graph which consists of $\bold{n}$ vertices, $\bold{e}$ edges and $\bold{q}$ colors are offered, we need to assign colors to each vertex such that no two adjacent vertices share the same color). Former scholars mainly focused on the minimum number of colors that could be used to color the graph, but here we focus on the application of Gibbs sampler on this problem. All the code was implemented from scratch.



## What we are concerned about

### About vertices

We call a certain valid way to assign colors to each vertex as one configuration. Assume all valid configurations are uniformly distributed, what is the average number of vertices which all occupy a same certain color (say, red)? Intuitively, we may think that the average number of vertices which occupy a same certain color should be the same among each color, which is $$\frac{n}{q}$$. Then how do we prove it? If there is a method to "traverse" the configurations, even if the traverse is not complete (i.e. do not traverse exactly every configuration), will the average number of vertices occupying the same color converge during the traversal? 

### About edges

We define the type of an edge by the colors of the two vertices it connects (e.g. an edge connecting two vertices of color 0 and color 1 respectively is called type (0,1)). If the assignment of colors is "randomized" enough (i.e. uniformly distributed), then the expected number of edges of type (x,y) should be $\frac{e}{qC2}$ where $e$ is the total number of edges in the graph. How do we show this?

## 

## Reasons for using MCMC

Obviously, this is an NP-Hard question because when we increase the number of vertices or the number of colors, the number of valid configurations grows exponentially. Thus, it is really hard to count using combinatorics, which makes it really difficult if we wish to prove our assumptions above. MCMC gives a feasible way to tackle this issue. Assume $X_1 ... X_N$ denote all valid configurations (note that $N$ can be extramely large) and $h(x)$ is a function whose domain is ${X_1 .. X_N}$, then according to the theory that  $E(h(x)) = \lim_{n\rightarrow+\infty}$  $\frac{1}{n}$ $\sum_{i=1}^n{h(x_i)}$ , we can "simulate" the process by drawing a sample from the domain each time and continue this process for a large number of iterations and use the average value to estimate the expectation. However, the main problem is, how to do the sampling (i.e. get $x_1$ ... $x_n$)? According to the theory of MCMC, first of all, we need to construct a "transition mechanism" satisfying the Markov property (i.e.  $P(x_{i+1}|x_{i},x_{i-1}...x_0) = P(x_{i+1}|x_i) \forall i \in N$ ). After that, we can run this Markov chain and get a series of samples.



##Transition mechanism in Gibbs Sampler

Suppose $\bold Q$ is the set of all colors. Generally, when Gibbs sampler is applied to this problem, in every iteration, we randomly pick one vertex, search the set of colors of its neighbors so that we can fixed the set $\bold Q'$ of all the valid colors to this vertex. Then, we uniformly pick one color from $\bold Q'$ and update the color of this vertex. However, for simplicity, we can update the vertices sequentially rather than randomly. That is, in the $i-th$ iteration, we update the $(i$ $mod$ $n$) th​ vertex. The updating mechanism remains the same. 

The sufficient condition of MCMC is the $\bold {aperiodicity}$ and $\bold {irreducibility}$ of the Markov Chain. For aperiodicity, since $\bold {Q'}$ contains the current color of the vertex we are updating, the probability of staying in the same state is non-zero. Hence, aperiodicity is satisfied. For irreducibility, basically, the number of colors really matters. For example, if the graph is fully connected and $\bold{q} = \bold{n}$ (i.e. each vertex occupies a unique color and there is no more color. Recall that $\bold{q}$ is the number of colors and $\bold{n}$ is the number of vertices), then there is no way to update the configuration of this graph because any time you pick a vertex, the only valid color for this vertex is the current color and you cannot change it to a different one. Thus, here we set a secure lower bound for the number of colors. Denote $\bold{d}$ as the maximum degree among the vertices in the graph, let $\bold{q} > 2 * \bold{d}$. The following presents an algorithm to find a series of transitions from a configuration $\bold{A}$ to another configuration $\bold{B}$. 

Suppose $\bold{V}$ is the set of vertices of the graph, then $\bold{A}$ = $\{a_{v_i} | v_i \in \bold{V} \}$ and $\bold{B}$ = $\{b_{v_i} | v_i \in \bold{V} \}$. Suppose $\bold{C}$ is the set of vertices which occupy different colors in $\bold{A}$ and $\bold{B}$ and let $|\bold{C}|$ = $m$ (i.e. There are totally $m$ vertices in the graph which occupy different colors in $\bold{A}$ and $\bold{B}$.)  Let $\bold{A'}$ = $\{a_{c_i} | c_i \in \bold{C} \}$ and $\bold{B'}$ = $\{b_{c_i} | c_i \in \bold{C}\}$.  

##### Algorithm: 

$transitionAB$ $(\bold{A}, \bold{B}, c_i):$

​		$if$ $c_i$ $has$ $been$ $modified:$

​				$break$

​		$else$ $if$ ( $\bold{A}$ \ $\{a_{c_i}\}$ ) $\bigcup$ $\{b_{c_i}\}$  $is$ $valid:$

​				$\bold{A}$ =  ( $\bold{A}$ \ $\{a_{c_i}\}$ ) $\bigcup$ $\{b_{c_i}\}$ 

​		$else:$

​				$randomly$ $pick$ $one$ $color$ $which$ $is$ $not$ $occupied$ $by$ $the$ $neighbors$ $of$ $b_{c_i}$	

​				$assign$ $the$ $picked$ $color$ $to$ $a_{c_i}$

​				$transitionAB(\bold{A}, \bold{B}, c_j)$

​				$\bold{A}$ =  ( $\bold{A}$ \ $\{a_{c_i}\}$ ) $\bigcup$ $\{b_{c_i}\}$ 

Then we apply the algorithm to each vertex in $\bold{C}$ in order. Here are some notations to the algorithm:

1. The function is applied to one single vertex
2. In the third case, since we have assumed that $\bold{q}$ > $2*\bold{d}$, we can always find a valid color which not occupied by the neighbors of $b_{c_i}$.
3. In the third case (changing the color of $c_i$ to the objective color in $\bold{B}$ directly is invalid), then the adjacent vertex which occupy the objective color in $\bold{A}$ must be in $\bold{C}$. Or, $\bold{A}$ is no longer valid because $\bold{A}$ $\bold{B}$ share the same color assignment in vertices other than $\bold{C}$.

Using this algorithm, we can always find a series of transitions between any two valid configurations. Thus, the Markov Chain is $\bold{irreducible}$ and $\bold{aperiodic}$, which proves that the Gibbs sampler is a valid MCMC method to do the simulation task. 

​						

## Objectives of doing this research

Now that we have proved that Gibbs sampler is a good method to do simulation for this problem, we wish to find something interesting related to vertices and edges. The process is mainly to initialize the coloring of the graph randomly (i.e. to generate $X_0$ randomly), then run the Markov Chain to generate samples $X_1$, $X_2$, $X_3$ ...... The state at time $t$ (i.e. $X_t$) should be generated based on the posterior distribution given the state at time $t-1$ (i.e. $X_{t-1}$). Based on the samples, simulations can be done in a lower computational cost compared with traversing all valid configurations. Thus, as we have discussed before, 

in terms of vertices, we will mainly discover:

1. For a certain graph, when changing the total number of colors we use or when changing the connectivity of the graph (i.e. to add some more edges to the original graph), if we only focus on the vertices occupying a same color, how will the speed of convergence of the average number of such vertices be affected?
2. If we focus on all colors and construct a $\bold{1*q}$ vector, the $i$ th entry represents the average number of vertices which occupy the color $i$. Then we focus on the average absolute distance between this vector and the vector of expectation (i.e. a $\bold{1*q}$ vector in which every entry has value $\frac{1}{q}$). What will the speed of convergence of the average absolute distance be affected this time?  

In terms of edges, we will mainly discover:

1. Will the number of each type of edges converge to $\frac{e}{qC2}$?
2. If so, will there be any difference in the speed of convergence between different colors?



## Experiment

###Construction of the graph

I implemented two algorithms to construct the graph:

####Method 01

We first random shuffle the vertices list (i.e. [0, 1, 2, ..., n-1]). Then iterate the vertices list. Each time we pop the head of the list (return the first element of the list and delete it). For the ith vertex, randomly connect it with k vertices among the first i-1 vertices. k is a random integer between 1 and a threshold which is set as a hyperparameter. 

####Method 02

Since for every connected graph, we can always delete some edges so that it can become a tree. We can generate a tree (which is already connected) and then add some more edges randomly afterwards. When generating the tree, we also random shuffle the vertices list (i.e. [0, 1, 2, ..., n-1]). Then every time we pop the list and set the poped vertex as the right-most node of the current tree. The number of subtrees for each non-leaf node is randomly assigned. After the construction of the tree, we add some more edges to this tree.

Generally, Method 01 can generate a graph with larger connectivity (measured by average degree).

###Initialization of colors

As we have stated before, denote the maximum degree among the vertices in a graph as $\bold{d}$, then for security, we let $\bold{q} > \bold{2}*\bold{d}$.  Initially, we set Null to all vertices' colors. We assign the colors to vertices in a random order. (i.e. Random shuffle the list [0, 1, 2, ..., n-1]) Then we iterate the shuffled list. Each time we search the colors of the neighbours of the current vertex and uniformly choose one from all the valid colors. Since $\bold{q} > \bold{2} * \bold{d}$, there must exist available colors in every iteration.



###Iteration

Basically, when running the Markov Chain, every time we need to select a vertex $i$ randomly and update its color. Let $\bold{Q_i}$ be the set of colors occupied by the neighbors of vertex $i$. The new color is selcted uniformly from $\bold{Q}/\bold{Q_i}$. Thus, it is possible to stay in the same configuration after an iteration. Without the loss of generally, we update the colors of vertices sequentially (i.e. Update the color of vertex $i$ $\bold{mod}$ $n$ in the $i$ th iteration). 



### Methods to compare speed of convergence of two sequences

Since we are concerned about convergence, we need a practical method to compare the speed of convergence of sequences which are generated when running the Markov Chain. The method that I have tried are as follows.

####Order of convergence

Mathematically, a practical method to calculate the order of convergence is to calculate the following sequence which converges to $q$ :

$q$ ≈ $\frac{log|\frac{x_{k+1} - x_k}{x_k - x_{k-1}}|}{log|\frac{x_k - x_{k-1}}{x_{k-1} - x_{k-2}}|}$

For two convergent sequences, it is feasible to compare their speed of convergence by computing their order of convergence respectively as long as $q$ converges for when $k$ becomes large.

#### Ratio test

It is also feasible to employ ratio test when comparing the speed of convergence of two convergent sequences. Suppose there are two convergent positive sequences $\{a_n\}$ and $\{b_n\}$, if the sequence $\{\frac{a_n}{b_n}\}$ converges to 0, then $\{a_n\}$ converges faster. If it converges to any positive real number, then the speed of convergence for the two sequences are similar. If it diverges, then $\{b_n\}$ converges faster. 

#### Show by plots

The most intuitive and straightforward way to compare the speed of convergence is by ploting the sequences and compare them directly.



According to the results of some tentative experiments, it is impractical to compute the order of convergence because there is always no such a $q$ which is stable when $k$ becomes large. Meanwhile, ratio test is also proved impractical because the sequence of ratio neither converge nor diverge to positive infinity. Thus, the only way we can use is to show by plots.



### Initialization of the graph

Before doing the experiments, I tested the two methods for the initialization of the graph. The setting of hyper-parameters are as follows. Please note that this procedure aims to compare the two methods rather than finding the best hyper-parameters. Meanwhile, the setting of hyper-parameters is not the focus of this research:

#### Result of Method 01

| Num of Vertices | Max connection with former vertices | Avg degree | Max degree |
| --------------- | ----------------------------------- | ---------- | ---------- |
| 50              | 10                                  | 16.0       | 27         |
| 100             | 10                                  | 18.0       | 35         |
| 150             | 10                                  | 18.67      | 39         |
| 200             | 10                                  | 19.0       | 46         |



####Result of Method 02

| Num of Vertices | Max subtree | Max added edges | Avg degree | Max degree |
| --------------- | ----------- | --------------- | ---------- | ---------- |
| 50              | 4           | 8               | 2.28       | 5          |
| 100             | 4           | 8               | 2.14       | 6          |
| 150             | 4           | 8               | 2.093      | 6          |
| 200             | 4           | 8               | 2.07       | 6          |



#### Comparation of the two methods

We can see from the statistics that method 01 initializes a graph with larger connectivity since the graph has larger maximum degree as well as larger average degree. Thus, we need to use more colors if method 01 is used to initialize the graph since our premise is $\bold{q}$ > $\bold{2}$ * $\bold{d}$. Moreover, method 02 is more "stable" because the average degree and maximum degree remains almost unchanged when we increase the number of vertices. Therefore, we employ method 02 for the following experiments.



### Discovery 1: Focusing on one color

In this experiment, we wish to discover the average number of vertices which occupy the same certain color  when running the Markov Chain. We denote $n_{i_j}$ as the average number of vertices which occupy color $i$ from the beginning to the $j$ th iteration. The color index $i$ is randomly picked from $\bold{Q}$ and it is trivial. Theoretically, the sequence $\{n_{i_j}\}$ converges to $\frac{n}{q}$. Since when we change $q$, $\frac{n}{q}$ will also change, it is necessary to adjust the sequences to $\{n_{i_j} - \frac{n}{q}\}$, which theoretically should converge to 0. Moreover, in order to reduce random error, for each setting of number of colors, we repeat the experiment for 50 times and use the average. As we have discussed before, we do the following two sets of experiments:

#### Change total number of colors

Basically, we try different number of colors on the same graph and the index of selected color is trivial. Firstly, I need to show that the Gibbs Sampler really produces a convergent result. I set the number of vertices as 150. The number of colors were 20, 25, 30, 35, 40. I get the following plot in which the x-axis is iterations and the y-axis is $n_{i_j} - \frac{n}{q}$. 

<img src="/Users/pengcheng/Desktop/FYP/MCMC/focus_one_color/plots in report/m2 v150.png" alt="m2 v150" style="zoom:40%;" />

We can see that no matter how many colors we use, ultimately they will converge. However, the difference in speed of convergence is not obvious. We need to enlarge the difference in the number of colors. Meanwhile, the sequences have converged after 15,000 iterations, thus, we are able to reduce the number of iterations in order to shorten the running time. We did the experiments as follows:

<img src="/Users/pengcheng/Desktop/FYP/MCMC/focus_one_color/plots in report/color/m2, v50.png" alt="m2, v50" style="zoom:30%;" /> <img src="/Users/pengcheng/Desktop/FYP/MCMC/focus_one_color/plots in report/color/m2, v100.png" alt="m2, v100" style="zoom:30%;" /> 

<img src="/Users/pengcheng/Desktop/FYP/MCMC/focus_one_color/plots in report/color/m2, v150.png" alt="m2, v150" style="zoom:30%;" /> <img src="/Users/pengcheng/Desktop/FYP/MCMC/focus_one_color/plots in report/color/m2, v200.png" alt="m2, v200" style="zoom:30%;" />

We can see from the plots that there exists a tendency of faster convergence when we increase the number of colors, it seems to converge faster. However, the evidence is not obvious because there exists some cases in which we increase the number of colors while the chain converges slower. Since we only consider the number of vertices occupying one certain color, random error is likely to affect the result. 

####Change connectivity

Basically, we may add more edges to the existing graph so that the connectivity of the graph can be increased. If the conjecture in the previous section is true (i.e. more valid configurations, faster convergence), then when we increase the connectivity of the graph, there will be less valid configurations and the convergence should be slower. We conducted experiments on graphs with vertices 50, 100, 150 and 200. In each experiment, the number of edges that we add is proportional to the number of vertices. Here are the plots: 

<img src="/Users/pengcheng/Desktop/FYP/MCMC/focus_one_color/plots in report/connectivity/m2, v50.png" alt="m2, v50" style="zoom:30%;" /> <img src="/Users/pengcheng/Desktop/FYP/MCMC/focus_one_color/plots in report/connectivity/m2, v100.png" alt="m2, v100" style="zoom:30%;" />

<img src="/Users/pengcheng/Desktop/FYP/MCMC/focus_one_color/plots in report/connectivity/m2, v150.png" alt="m2, v150" style="zoom:30%;" /> <img src="/Users/pengcheng/Desktop/FYP/MCMC/focus_one_color/plots in report/connectivity/m2, v200.png" alt="m2, v200" style="zoom:30%;" />

Roughly speaking, the light blue curve which represents the initial graph converges faster than the others. When we add more edges to the graph, they converge slower in different levels. Therefore, our conjecture is right. The more edges we add to the graph, the less valid configurations and the slower the convergence. Similar to the set of experiments above regarding the number of colors, the results are not stable. There are also some cases in which graphs with larger connectivity converge faster than those with smaller connectivity. Thus, we need to further reduce the random error. Since we have only focused on one color, we turn to focusing on all colors in the following experiments.

### Discovery 2: Focusing on all colors

#### Change total number of colors



####Change connectivity





### Discovery 3: Focusing on edges

