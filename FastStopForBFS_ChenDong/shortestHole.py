import sys
import numpy as np
import simplegraphs as sg
import queue


def shortestHole(G,s):
    ########################################
    # Write code that finds the shortest hole containing s if one exists
    # If one exists, set 'found' to True
    # Set hole_length to be the length of the shortest hole
    # Set hole_nodes to be a list of the nodes in the hole in order,
    #    starting from s (and not repeating s)
    ########################################
    # For example, maybe your first step would be to run the usual BFS
    def BFSM(G, s):
        # G is a dictionary with keys "n", "m", "adj" representing an unweighted graph
        # G["adj"][u][v] is True if (u,v) is present. Otherwise, v is not in G["ad"][u].
        distances = {}
        finalized = {} # set of discovered nodes
        parents = {} # lists parent of node in SP tree
        layers = [[] for d in range(G["n"])] # lists of nodes at each distance.
        Q = queue.Queue()
        distances[s] = 0
        parents[s] = None
        tag ={}
        Q.put(s)
        x=G["n"]
        found = False
        hole_length =  -1 # Default value for when no hole is found
        hole_nodes = [] # Default value for when no hole is found
        while not(Q.empty()): #Q not empty
            u = Q.get()
            if u not in finalized: #if u was already finalized, ignore it.
                finalized[u] = True
                layers[distances[u]].append(u)
                if distances[u]>x:
                    return found, hole_length, hole_nodes
                for v in G["adj"][u]:
                    
                    # record v's distance and parent and add v to the queue if  
                    # this is the first path to v,  
                    if (v not in distances): # first path to v
                        distances[v] = distances[u] + 1
                        parents[v] = u
                        Q.put(v)
                        
                        if distances[v] ==1 :
                            tag[v] = v
                        else:
                            tag[v] = tag[u]
                    else:
                        if distances[v]==distances[u] and tag[v] != tag[u]:
                            found=True
                            hole_length = distances[v]+distances[u]+1
                            hole_nodes= [s]+addparents(s,u,parents)+addparents1(s,v,parents)
                            return found, hole_length, hole_nodes
                        elif not found and distances[v]>distances[u] and tag[v] != tag[u]:
                            found=True
                            hole_length = distances[v]+distances[u]+1
                            hole_nodes= [s]+addparents(s,u,parents)+addparents1(s,v,parents)
                            x = distances[u]      
        return found, hole_length, hole_nodes
    found, hole_length, hole_nodes = BFSM(G,s)
    return found, hole_length, hole_nodes
    # Return the output



def addparents(s,u,parents):
    if parents[u] == s:
        return [u]
    else:
        return addparents(s,parents[u],parents)+[u]
def addparents1(s,u,parents):
    if parents[u] ==s:
        return [u]
    else:
        return [u]+addparents1(s,parents[u],parents)


#########################################################
# Don't modify the stuff below this line
#########################################################
 

def readSource(start_file):
    # The source vertex is listed in its own file
    # It is an integer on a line by itself.
    with open(start_file, 'r') as f:
        raw_start = f.readline()
        s = int(raw_start)
    return s



def writeOutput(output_file, hole_found, hole_length, hole_list):
    # This takes the outputs of shortestHole and writes them
    # to a file with the name output_file
    with open(output_file, 'w') as f:
        f.write("{}\n".format(hole_found))
        f.write("{}\n".format(hole_length))
        f.write("{}\n".format(hole_list))
    return



def main(args=[]):
    # Expects three command-line arguments:
    # 1) name of a file describing the graph
    # 2) name of a file with the ID of the start node
    # 3) name of a file where the output should be written
    if len(args) != 3:
        print("Problem! There were {} arguments instead of 3.".format(len(args)))
        return
    graph_file = args[0]
    start_file = args[1]
    out_file = args[2]
    G = sg.readGraph(graph_file) # Read the graph from disk
    s = readSource(start_file) # Read the source from disk
    hole_found, hole_length, hole_list = shortestHole(G,s) # Find the shortest hole!
    writeOutput(out_file, hole_found, hole_length, hole_list) # Write the output
    return 

if __name__ == "__main__":
    main(sys.argv[1:])    

    