import sys
import os
import heapq
import queue
import numpy as np
import simplegraphs as sg


def bellmanFordSimple(G, s):
    # G is a dictionary with keys "n", "m", "adj" representing an *weighted* graph
    # G["adj"][u][v] is the cost (length / weight) of edge (u,v)
    # This algorithms finds least-costs paths to all vertices
    # Will not detect negative-cost cycles
    # Returns an dict of distances (path costs) and parents in the lightest-paths tree.
    #
    # This is basically the algorithm we covered in class (except it
    # finds paths from a source instead of to a desitnation).
    #
    n = G["n"]
    d = [{} for i in range(n)]
    for u in G["adj"]:
        d[0][u] = np.inf
    d[0][s] = 0
    parent = {s: None}
    for i in range(1,n):
        for v in G["adj"]:
            d[i][v] = d[i-1][v]
        for u in G["adj"]:
            for v in G["adj"][u]:
                newlength = d[i-1][u] + G["adj"][u][v]
                if newlength <  d[i][v]:
                    d[i][v] = newlength
                    parent[v] = u
    distances = d[n-1]
    return distances, parent

def bellmanFordEarlyStop(G, s):
    # G is a dictionary with keys "n", "m", "adj" representing an *weighted* graph
    # G["adj"][u][v] is the cost (length / weight) of edge (u,v)
    # This algorithms finds least-costs paths to all vertices
    # Returns a dict of distances (path costs) and parents in the lightest-paths tree.
    #
    # This version stops early when no further changes observed. 
    #
    n = G["n"]
    d = [{} for i in range(n+1)]
    for u in G["adj"]:
        d[0][u] = np.inf
    d[0][s] = 0
    key = s
    found =False
    parent = {s: None}
    for i in range(1,n+1):
        changed = {}
        for v in G["adj"]:
            d[i][v] = d[i-1][v]
        for u in G["adj"]:
            for v in G["adj"][u]:
                newlength = d[i-1][u] + G["adj"][u][v]
                if newlength <  d[i][v]:
                    d[i][v] = newlength
                    parent[v] = u
                    changed[v] = True
                    newkey = v
                    key = v
                    if i >=2: # if we found a node value is decreased, we 
                              # we trace back to see whether it is a cycle or not
                        for x in range(i):
                            v = parent[v]
                            if key == v:
                                found = True
                                break
                if found:
                    break
            if found:
                break
        if found:
            break
        if not changed:
            break
           
    # if the last iteration had distances still changing,
    # there must exist a negative weight cycle reachable from s.
    if found:
        negCycle = True
    else:
        negCycle = False
    distances = d[i]
    cycle_list = [] 
    # appen a list of nodes that meet the requirement
    if negCycle:
        startnode = newkey
        startnode = parent[startnode]
        while newkey not in cycle_list:
            cycle_list.append(startnode)
            startnode = parent[startnode]
        cycle_list.reverse()
    return distances, parent, i, negCycle, cycle_list

def negCycle(G):
    # This code returns
    # found: a boolean (where true indicates a negative-weight cycle was found)
    # cycle_list: either an empty list (if found is False) or a list of nodes
    # that form a negative-weight cycle.
    ########################################
    # Make a copy of G. Don't touch G again
    newG = sg.copyGraph(G)
    # Add a new source and 0-weight edges to all the original nodes.
    #
    source = 50000
    sg.addNode(G,source)
    for x in G["adj"]:
        sg.addDirEdge(newG,source,x,label = 0)
        
    #
    # Now look for negative cycles. YOU SHOULD MODIFY THE BF ALGORITHM
    distances, parent, i, negCycle, cycle_list = bellmanFordEarlyStop(newG, source)
    if negCycle:
        return True,  cycle_list
    else:
        return False, []

def BFCountSumPaths(G, s, k = None):
    # G is a dictionary with keys "n", "m", "adj" representing an
    # *weighted* graph where G["adj"][u][v] is the cost (length /
    # weight) of edge (u,v)

    # This algorithm counts the number of paths of length i from s to
    # every other vertex, for every i from 0 to k. If k is not
    # specified, we set k to n-1 (where n is the number of nodes in
    # G).

    # It also computes the sum of the weights of all the paths of
    # length i from s to every other vertex.
    
    # Returns two objects: (a) count is a list of dicts, where
    # count[i][u] is the number of paths with i edges from s to u; (b)
    # weightsum if a list of dicts, where weightsum[i][u] is the sume
    # of path costs over all paths with i edges from s to u.
    n = G["n"]
    if k != None:
        limit = int(k) 
    else:
        limit = n-1
    # Initialize the main data structures.
    count = [{} for i in range(limit + 1)]
    weightsum = [{} for i in range(limit + 1)]
    for i in range(limit+1):
        for u in G["adj"]:
            count[i][u] =0
            weightsum[i][u]=0
    #
    #
    count[0][s] = 1
    reverseG= sg.reverseGraph(G)
    for j in range(1,k+1):
        for v in G["adj"]:
            for u in reverseG["adj"][v]:
                count[j][v]+= count[j-1][u]
                weightsum[j][v]+=reverseG["adj"][v][u]*count[j-1][u]+weightsum[j-1][u]
    return count, weightsum
    

############################################################
#
# The remaining functions are for reading and writing outputs, and processing
# the command line arguments. 
#
############################################################




def writeNegCycleOutput(output_file, found, node_list):
    # This takes the outputs of negCycle and writes them
    # to a file with the name output_file
    with open(output_file, 'w') as f:
        f.write("{}\n{}\n".format(bool(found), node_list))
    return

def writeAverageWeightOutput(output_file, avg_weight):
    # This takes the average path weight and writes it
    # to a file with the name output_file
    with open(output_file, 'w') as f:
        f.write("{}\n".format(avg_weight))
    return


def parseNegCycleOutput(student_out_filename):
    # This will read an output file (either yours or the one provided
    # with the starter and load its content into usable Python
    # variables Its output has the same format as negCycle (a Boolean
    # and a list of nodes).  This may be useful when you are testing
    # your code, but you don't need to use it.
    if not(os.path.isfile(student_out_filename)):
        return False, "Student file not found"
    with open(student_out_filename, "r") as f:
        raw = f.read().splitlines()
        if len(raw) < 2:
            return False, "Too few lines in student file"
        raw_bool = raw[0]
        raw_list = raw[1]
    # Parse first line
    if raw_bool == "True":
        neg_cycle_found = True
    elif raw_bool == "False":
        neg_cycle_found = False
    else:
        return False, "First line of output file could not be parsed as a Boolean."
    # Parse third line
    try: 
        list_of_strings = raw_list.strip('][').split(',')
        if list_of_strings == ['']:
            list_of_nodes = []
        else:
            list_of_nodes = [int(x) for x in list_of_strings]
    except:
        return False, "Second line of output file could not be parsed as a list of integers."          
    return (neg_cycle_found, list_of_nodes)

def main(args = []):
    # Expects three to five command-line arguments:
    # 1) Task, e.g. "negCycle"
    # 2) name of a file describing the graph
    # 3) name of a file where the output should be written
    # 4) For average weight, the source node s.
    # 5) For average weight only, the desitnation node t.
    if len(args) < 3:
        print("Too few arguments! There should be at least 3.")
        return
    task = args[0]
    graph_file = args[1]
    out_file = args[2]
    if task == "negCycle":
        if len(args) != 3:
            print("Problem! There were {} arguments instead of 3 for negCycle.".format(len(args)))
            return
        G = sg.readGraph(graph_file) # Read the graph from disk
        neg_cycle_found, cycle_list = negCycle(G) #This part actually does all the work
        writeNegCycleOutput(out_file, neg_cycle_found, cycle_list) # Write the output
        if neg_cycle_found:
            is_cycle, cost = sg.checkCycle(G, cycle_list) # This is just to show you how to use the checkCycle function.
            if not is_cycle:
                print("Your list of nodes is not a cycle :(")
            elif cost >=0:
                print("Your list of nodes is a cycle but its cost isn't negative :(")
        return
    elif task == "averageWeight":
        if len(args) != 5:
            print("Problem! There were {} arguments instead of 5 for averageWeight.".format(len(args)))
            return
        s = int(args[3])
        t = int(args[4])
        G = sg.readGraph(graph_file) # Read the graph from disk
        count, weightsum = BFCountSumPaths(G, s, k=6) # Compute path counts 
        if count[6][t] == 0:
            average_weight = 0
        else:
            average_weight = weightsum[6][t] / count[6][t]
        writeAverageWeightOutput(out_file, average_weight)
    else: 
        print("Problem! Task {} not recognized".format(task))
    return

if __name__ == "__main__":
    main(sys.argv[1:])    

