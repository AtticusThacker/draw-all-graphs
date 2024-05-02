# Function that takes in number of edges q and number of vertices p.
# List every permutation with q 1's and p(p-1)/2-q 0's and put them in a master list
# For each permutation x in thge master list, compute all the isomorphic sequences and each time you find another isomorphic sequence, remove it from the master list if it is still there and place it into the list of sequences isomorphic x.
# Return one element from each list of isomorphic sequences

import math
import networkx as nx 
import matplotlib.pyplot as plt 
import itertools

class Graph:
  def __init__(self, vertices, edges, string):
    self.vertices = vertices
    self.edges = edges
    self.string = string


# compute_binary_permutations(p,q):
# generate all permutations of q 1's and p(p-1)/2-q 0's and return them as nested lists in a master list
def compute_binary_permutations(p, q):
  def backtrack(curr_permutation, zeros_remaining, ones_remaining):
    if zeros_remaining == 0 and ones_remaining == 0:
      unique_permutations.append(curr_permutation[:])
      return
    if zeros_remaining > 0:
      curr_permutation.append(0)
      backtrack(curr_permutation, zeros_remaining - 1, ones_remaining)
      curr_permutation.pop()
    if ones_remaining > 0:
      curr_permutation.append(1)
      backtrack(curr_permutation, zeros_remaining, ones_remaining - 1)
      curr_permutation.pop()

  unique_permutations = []
  backtrack([], (p*(p-1))//2-q, q)
  return unique_permutations
    

# compute_vertex_relabellings(p):
# precompute all the permutations of [0...p-1] and return them nested in a list
def compute_vertex_relabellings(p):
  permutations_list = list(itertools.permutations(range(p)))
  return permutations_list

  
# edge_to_index(v1,v2):
# get the index of the edge between v1 and v2.
def edge_to_index(v1, v2):
  x = min(v1, v2)
  y = max(v1, v2)
  return (y**2 - y + 2*x) // 2


# precompute_edge_relabellings(p,vertex_relabellings):
# for each given permutation of [0...p-1], calculate a list describing which index each edge goes to after permuting the vertices
def precompute_edge_relabellings(p,vertex_relabellings):
  master_list = []
  permuted_edges = [None] * ((p*(p-1))//2)
  for permutation in vertex_relabellings:
    for i in range(1, p):
      for j in range(i):
        permuted_edges[edge_to_index(permutation[i], permutation[j])] = edge_to_index(i, j)
    master_list.append(permuted_edges[:])
  return master_list

# Removes duplicate lists
def eliminate_duplicate_lists(list_of_lists):
  # Use a set to store unique representations of lists
  unique_lists = set()

  # Filter out duplicate lists
  result = [lst for lst in list_of_lists if tuple(lst) not in unique_lists and not unique_lists.add(tuple(lst))]

  return result


# list_isomorphic_sequences(binary_sequence, edge_relabellings):
# apply each edge relabelling to binary_sequence and nest them in a list
def list_isomorphic_sequences(binary_sequence, edge_relabellings):
  isomorphic_sequences = []
  for permutation in edge_relabellings:
    new_array = []
    for i in range(len(binary_sequence)):
      new_array.append(binary_sequence[permutation[i]])
    isomorphic_sequences.append(new_array)
  return eliminate_duplicate_lists(isomorphic_sequences)
  

# group_isomorphic_sequences(binary_sequences, edge_relabellings):
# start with two lists "grouped_sequences" and "binary_sequences". 
# for each binary sequence in binary_sequences, compute list_isomorphic_sequences(binary_sequence, edge_relabellings) and append the list of all isomorphic sequences to grouped_sequences in a nested list while also removing each of them from binary_sequences, repeat this until binary_sequences is empty.
def group_isomorphic_sequences(binary_sequences, edge_relabellings):
  grouped_sequences = []
  while len(binary_sequences) > 0:
    for binary_sequence in binary_sequences:
      x=list_isomorphic_sequences(binary_sequence, edge_relabellings)
      grouped_sequences.append(x.copy())
      for y in x:
        binary_sequences.remove(y)
  return grouped_sequences


# print one isopmorphic sequence from each list of isomorphic sequences
def print_one_of_each(grouped_sequences):
  seqs=[]
  for string in grouped_sequences:
    seqs.append(string[0])
  return seqs

# do the final calculation all in one function
def calculate_isomorphic_sequences(p, q):
  b = compute_binary_permutations(p, q)
  e = precompute_edge_relabellings(p,compute_vertex_relabellings(p))
  return print_one_of_each(group_isomorphic_sequences(b, e))
# -----------------------------------

# Function to convert an index in the permutation to the corresponding edge (a, b)
def index_to_edge(i):
    sqrt_val = math.floor((1 + math.sqrt(8*i + 1)) / 2)
    return (2*i + sqrt_val - sqrt_val**2) // 2, sqrt_val


# Defining a Class 
class GraphVisualization: 

    def __init__(self): 

        # visual is a list which stores all  
        # the set of edges that constitutes a 
        # graph 
        self.visual = [] 

    # addEdge function inputs the vertices of an 
    # edge and appends it to the visual list 
    def addEdge(self, a, b): 
        temp = [a, b] 
        self.visual.append(temp) 

    # In visualize function G is an object of 
    # class Graph given by networkx G.add_edges_from(visual) 
    # creates a graph with a given list 
    # nx.draw_networkx(G) - plots the graph 
    # plt.show() - displays the graph 
    def visualize(self): 
        G = nx.Graph() 
        G.add_edges_from(self.visual) 
        nx.draw_networkx(G) 
        plt.show() 


def draw_graph(sequence):
  G = GraphVisualization() 
  for i in range(len(sequence)):
    if sequence[i] == 1:
      c=index_to_edge(i)
      G.addEdge(c[0], c[1])
  G.visualize() 

graphs=calculate_isomorphic_sequences(6, 9)

print(graphs)

draw_graph(graphs[3])