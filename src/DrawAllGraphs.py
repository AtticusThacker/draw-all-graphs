# Function that takes in number of edges q and number of vertices p.
# List every permutation with q 1's and p(p-1)/2-q 0's and put them in a master list
# For each permutation x in thge master list, compute all the isomorphic sequences and each time you find another isomorphic sequence, remove it from the master list if it is still there and place it into the list of sequences isomorphic x.
# Return one element from each list of isomorphic sequences

import math
import networkx as nx 
import matplotlib.pyplot as plt 
import itertools
import cProfile
from bitarray import frozenbitarray
import bitarray.util

#from pyavl import AvlTree

class BitGraph:
  def __init__(self, string):
    #self.string = string
    self.string = frozenbitarray(string)

  #this checks equality between two strings
  # def __eq__(self, other):
  #   #iterates through both lists simultaneously
  #   for i,j in zip(self.string, other.string):
  #     if i ^ j:
  #       return False
  #   return True

  # def __eq__(self, other):
  #   x = self.string ^ other.string
  #   return x.any()

  def __eq__(self, other):
    return bitarray.util.count_xor(self.string, other.string) == 0

  #hashes the bitgraph to an integer
  # def __hash__(self):
  #   res = 0
  #   for ele in self.string:
  #     res = (res << 1) | ele
  #   return res

  def __hash__(self):
    return self.string.__hash__()

  #finds all unique, isomorphic bitgraphs to this one
  # def isomorphic_sequences(self, edge_relabellings):
  #   isomorphic_sequences = set()
  #   for permutation in edge_relabellings:
  #     new_array = []
  #     for i in range(len(self.string)):
  #       new_array.append(self.string[permutation[i]])
  #     isomorphic_sequences.add(BitGraph(new_array))
  #   return isomorphic_sequences

  def isomorphic_sequences(self, edge_relabellings):
    isomorphic_sequences = set()
    for permutation in edge_relabellings:
      m = map(lambda p : self.string[p] , permutation)
      isomorphic_sequences.add(BitGraph(m))
    return isomorphic_sequences

  def len(self):
    return len(self.string)
  



# compute_binary_permutations(p,q):
# generate all permutations of q 1's and p(p-1)/2-q 0's and return them as nested lists in a master list
def compute_binary_permutations(p, q):
  def backtrack(curr_permutation, zeros_remaining, ones_remaining):
    if zeros_remaining == 0 and ones_remaining == 0:
      unique_permutations.add(BitGraph(curr_permutation[:]))
      return
    if zeros_remaining > 0:
      curr_permutation.append(False)
      backtrack(curr_permutation, zeros_remaining - 1, ones_remaining)
      curr_permutation.pop()
    if ones_remaining > 0:
      curr_permutation.append(True)
      backtrack(curr_permutation, zeros_remaining, ones_remaining - 1)
      curr_permutation.pop()

  unique_permutations = set()
  backtrack([], (p*(p-1))//2-q, q)
  return unique_permutations
    

# compute_vertex_relabellings(p):
# precompute all the permutations of [0...p-1] and return them nested in a list
#def compute_vertex_relabellings(p):
#  permutations_list = list(itertools.permutations(range(p)))
#  return permutations_list

  
# edge_to_index(v1,v2):
# get the index of the edge between v1 and v2.
def edge_to_index(v1, v2):
  x = min(v1, v2)
  y = max(v1, v2)
  return (y**2 - y + 2*x) // 2


# precompute_edge_relabellings(p):
# for each given permutation of [0...p-1], calculate a list describing which index each edge goes to after permuting the vertices
def precompute_edge_relabellings(p):
  master_list = []
  permuted_edges = [None] * ((p*(p-1))//2)
  for permutation in itertools.permutations(range(p)):
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
  

def to_integer(binary_sequence):
    res = 0
    for ele in binary_sequence:
        res = (res << 1) | ele


# group_isomorphic_sequences(binary_sequences, edge_relabellings):
# start with two lists "grouped_sequences" and "binary_sequences". 
# for each binary sequence in binary_sequences, compute list_isomorphic_sequences(binary_sequence, edge_relabellings) and append the list of all isomorphic sequences to grouped_sequences in a nested list while also removing each of them from binary_sequences, repeat this until binary_sequences is empty.
def group_isomorphic_sequences(binary_sequences, edge_relabellings):
  grouped_sequences = []

  while len(binary_sequences) > 0:
    binary_sequence = binary_sequences.pop()
    x = binary_sequence.isomorphic_sequences(edge_relabellings)
    grouped_sequences.append(x)
    for y in x:
      binary_sequences.discard(y)
  return grouped_sequences


# print one isopmorphic sequence from each list of isomorphic sequences
def print_one_of_each(grouped_sequences):
  seqs=[]
  for string in grouped_sequences:
    seqs.append(string.pop())
  return seqs

# do the final calculation all in one function
def calculate_isomorphic_sequences(p, q):
  b = compute_binary_permutations(p, q)
  e = precompute_edge_relabellings(p)
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


def draw_graph(graph):
  G = GraphVisualization() 
  sequence = graph.string
  for i in range(len(sequence)):
    if sequence[i]:
      c=index_to_edge(i)
      G.addEdge(c[0], c[1])
  G.visualize() 

#cProfile.run('calculate_isomorphic_sequences(6, 9)')
#e = precompute_edge_relabellings(6)
#cProfile.run('for i in range(10000): x = BitGraph([1,1,0,0,0,1,0,0,1,1,1,0,0,1,1]).isomorphic_sequences(e)')
#BitGraph([1,1,0,0,0,1,0,0,1,1,1,0,0,1,1]).isomorphic_sequences(precompute_edge_relabellings(6))
graphs=calculate_isomorphic_sequences(8, 10)

#print(graphs)

for i in range(min(10,len(graphs))):
    draw_graph(graphs[i])

# for i in range(len(graphs)):
#   draw_graph(graphs[i])

