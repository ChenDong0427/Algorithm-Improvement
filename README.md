# Algorithm-Improvement
This is a collection of improvements on general algorithms created by Chen Dong from Boston University

# How to test?
For ShorstestCycle:

Using the follwing commands in command line for testing:

python shortestCycle.py graph_file output_file

There are two arguments, each of which is the name of a file

• graph file describes the graph. This uses the format that is read by simplegraphs.py. The
first two lines of the file list the number of nodes n and the number of directed edges in the
graph. The remaining lines list the edges in the graph, assuming the node IDs are {1, .., n}.
Each line lists two vertices (ints) and a weight (float).

• output file is where your program will write its output. Code for writing the output is
provided. The first line is an float (the shortest cycle length, or “inf” if no cycle was found)
and the third line is a list of the IDs of the nodes in the shortest cycle (an empty list if no
cycle was found). The node IDs should be in order, but they can start anywhere on the cycle.
(The autograder checks that they form a directed cycle of the correct weight.)
