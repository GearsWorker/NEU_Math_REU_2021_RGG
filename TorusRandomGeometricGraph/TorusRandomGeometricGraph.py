#Written by Nicholas Thevenin for NEU Math REU 2021
#TODO:
#add progress tracker to see how many trials are left during operation

import networkx as nx
import matplotlib.pyplot as plt
import scipy
from bisect import bisect_left
from itertools import accumulate, combinations, product
from math import sqrt
import numpy as np
import math
import random
from math import radians, cos, sin, asin, sqrt


#WORKING IN RADIANS

def haversine(a, b):
    lon1, lat1 = a
    lon2, lat2 = b
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 1 # Radius of unit sphere
    return c * r

def _3D_sphere_edges(G, radius, p):
    edges = []
    for (u, pu), (v, pv) in combinations(G.nodes(data="pos"), 2):
        if sum(haversine(a,b)  p for a, b in zip(pu, pv)) <= radius  p: 
            edges.append((u, v))
    return edges


#Number of dimensions and number of vertices
d=2
n=10000 
radius = 3

random.seed()

G = nx.Graph()
G.add_nodes_from(range(n))

#STUFF TO GENERATE POINTS ON A SPHERE (gives pairs of spherical coordinates).
#latitude is in range of -pi/2 to pi/2, because this is what haversine formula expects
pos = {v: [2* math.pi * random.random(), ((math.acos(1-(2*random.random())))-(math.pi/2))] for v in range(n)}


nx.set_node_attributes(G, pos, "pos")



edges = _3D_sphere_edges(G, radius)
G.add_edges_from(edges)


#Initialize variables which will change often during loops to 0
radius = 0
counter = 0


#Initialize values for statistical paremeters, number of trials, and number of radii tested
trials = 1
categories = 1
radius_stop_value=0.05


#Arrays for keeping track of results.  
counts_list=[]
connectivity_list=[]
radius_list=[]


#Loop variables
j=0

increment = ((radius_stop_value - radius)/categories)

#First loop handles resetting variables for a given radius
while radius < radius_stop_value:
    counter = 0
    radius = radius + increment
    j = 0

    #Second loop handles individual trials
    while j < trials: 
        G = nx.random_geometric_graph(n, radius, d, None, math.inf)
        if nx.is_k_edge_connected(G,1) == True:
            counter = counter + 1
        j = j + 1
        #End inner loop
    counts_list.append(counter)
    radius_list.append(radius)
    #End outer loop


#Divide each count of connected graphs by number of trials to give probability
for counts in counts_list:
    connectivity_list.append(counts/trials)

title = "Plot of probability vs. radius by radius increments of " + str(increment) + ", with " + str(trials) + " trials on RGG of " + str(n) + " vertices."

threshold = pow((1/(2*d))*(np.log(n)/n),1./d)

#Plot results
plt.plot(radius_list, connectivity_list)
if d > 1:
    plt.plot([threshold,threshold], [0,1], linestyle = 'dashed')
else:
    plt.plot([(np.log(n)/n),(np.log(n)/n)], [0,1], linestyle = 'dashed')
plt.xlabel('Radius')
plt.ylabel('Probability')
plt.title(title)
plt.show()





#Extra stuff for other functions I worked on below
#
#
#

#Provided by networkx package, used for changing radius size for a given set of nodes
def _fast_edges(G, radius, p):
    """Returns edge list of node pairs within `radius` of each other
       using scipy KDTree and Minkowski distance metric `p`

    Requires scipy to be installed.
    """
    pos = nx.get_node_attributes(G, "pos")
    nodes, coords = list(zip(*pos.items()))
    kdtree = scipy.spatial.KDTree(coords)  # Cannot provide generator.
    edge_indexes = kdtree.query_pairs(radius, p)
    edges = ((nodes[u], nodes[v]) for u, v in edge_indexes)
    return edges

#plt.hist(connectivity_list, categories, (0,1), color = 'green',
        #histtype = 'bar', rwidth = 0.8)




#G = nx.random_geometric_graph(n, 0, d)

#granularity = 0.01

#while nx.is_k_edge_connected(G,1) == False:
 #   radius = radius + granularity
 #   temp_edges = _fast_edges(G, radius, 2)
 #   G.add_edges_from(temp_edges)
    

#print("The connectivity radius in ", d, " dimensions with ", granularity, " granularity for ", n, " vertices is ", radius)
#print("The value of the connectivity distance to the power of d times n / log (n) is ", ((pow(radius,d)*n)/np.log(n)), ".  The limit as n -> infinity is ", (1/(2*d)))

#print("Out of 100 graphs with ", n, "vertices, ", counter, " with a radius of ", radius, "were connected.")
#print("The connectivity value predicted in the paper is ")

#methodology is to check if surface distance between points when using a mapping which
#sends the x value to range of 0 to 2pi radians, used to determine which circle to "put"
# the point on
#sends the y value to range of 0 to 2pi radians, used to determine how "far around" the 
#given circle to "put" the point on
#
#while i < 100: 
#   G = nx.random_geometric_graph(n, radius)
#   if (nx.is_k_edge_connected(G,1) == True):
#       counter = counter + 1
#   i = i + 1

#while nx.is_k_edge_connected(G,1) == False:
#    radius = radius + granularity
#    temp_edges = _fast_edges(G, radius, 2)
#    G.add_edges_from(temp_edges)

#plt.subplot(121)

#nx.draw(G, with_labels=0)

# nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')

#plt.show()
#nx.write_graphml(G,"E:/NEU_Math_REU_2021/Graphs_for_Cytoscape/test.graphml")

