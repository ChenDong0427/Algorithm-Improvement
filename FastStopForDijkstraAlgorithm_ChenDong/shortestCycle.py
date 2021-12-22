import sys
import heapq
import queue
import numpy as np
import simplegraphs as sg
    

def shortestDirCycle(G):
    best_cost = np.Infinity #You should output this if you don't find any cycles
    best_node_list = [] #You should output this if you don't find any cycles
    root = None
    p =[]
    ln = None
    lol =0
    # Your code here.
    print("You are running the placeholder function.")
    for x in G["adj"]:
        lol = lol+1
        print(lol)
        length = best_cost
        distances, parents, lastnode, best_cost= dijkstra(G,x,best_cost)
        if best_cost<length:
            length = best_cost
            p = parents
            ln =lastnode
            root =x
    if best_cost!=np.Infinity:
        best_node_list = [root]+add(root,ln,p)
    return best_cost, best_node_list

def dijkstra(G, s,overallcost):
    # G is a dictionary with keys "n", "m", "adj" representing an *weighted* graph
    # G["adj"][u][v] is the cost (length / weight) of edge (u,v)
    # This algorithms finds least-costs paths to all vertices
    # Returns an array of distances (path costs) and parents in the lightest-paths tree.
    # Assumes nonnegative path costs
    distances = {} # actual distances
    finalized = {} # set of discovered nodes
    parents = {} # lists parent of node in SP tree
    Q = [] # empty priority queue. Use heappush(Q, (priorit, val)) to add. Use heappop(Q) to remove.
    distances[s] = 0
    lastnode = s
    parents[s] = None
    heapq.heappush(Q, (distances[s], s))
    while len(Q) > 0: #Q not empty
        (d, u) = heapq.heappop(Q)
        if distances[u]>overallcost:
            return distances, parents, lastnode,overallcost
        if u not in finalized: #if u was already finalized, ignore it.
            finalized[u] = True
            for v in G["adj"][u]:
                if G["adj"][u][v] <= overallcost:
                    new_length = distances[u] + G["adj"][u][v]
                    # update v's distance (and parent and priority queue) if  
                    # either this is the first path to v 
                    # or we have found a better path to v
                    if ((v not in distances) or (new_length < distances[v] )):
                        distances[v] = new_length
                        parents[v] = u
                        # add a copy of v to the queue with priority distances[v]
                        heapq.heappush(Q, (distances[v], v))
                    if v==s and distances[u]+G["adj"][u][v]<overallcost:
                        overallcost= distances[u]+G["adj"][u][v]
                        lastnode=u
                        
    return distances, parents, lastnode,overallcost

def add(s,u,parents,):
    if parents[u] == s:
        return [u]
    else:
        return add(s,parents[u],parents)+[u]

############################################################
# input/output code. You shouldn't have to modify this. 
############################################################

def writeOutput(output_file, cost, node_list):
    # This takes the outputs of shortestHole and writes them
    # to a file with the name output_file
    with open(output_file, 'w') as f:
        f.write("{}\n{}\n".format(float(cost), node_list))
    return

def main(args=[]):
    # Expects two command-line arguments:
    # 1) name of a file describing the graph
    # 3) name of a file where the output should be written
    if len(args) != 2:
        print("Problem! There were {} arguments instead of 2.".format(len(args)))
        return
    graph_file = args[0]
    out_file = args[1]
    G = sg.readGraph(graph_file) # Read the graph from disk
    best_cost, best_node_list = shortestDirCycle(G) # Find the shortest hole!
    writeOutput(out_file, best_cost, best_node_list) # Write the output
    return     

if __name__ == "__main__":
    main(sys.argv[1:])    


