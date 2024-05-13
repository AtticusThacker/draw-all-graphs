import math
from itertools import permutations
import json
import os

# Function to load data from file
def load_dict_from_file(filename):
    try:
        # Check if file is empty
        if os.path.getsize(filename) == 0:
            return {}

        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to convert string keys to tuple keys in a dictionary
def convert_keys_to_tuples(input_dict):
    new_dict = {}
    for key, value in input_dict.items():
        # Assuming key is a string in the format '(m,n)'
        # Strip parentheses and split by comma to get the tuple
        new_key = tuple(map(int, key.strip('()').split(',')))
        new_dict[new_key] = value
    return new_dict

# Load permutations dictionary from file
permsDict = load_dict_from_file('permsDict.json')
# Load graphs dictionary from file with converted keys to tuples
graphsDict = convert_keys_to_tuples(load_dict_from_file('graphsDict.json'))

if not graphsDict:
    # Default graphs if graphsDict is empty
    graphsDict = {(2, 0): [[0]], (2, 1): [[1]]}

# Function to convert index to edge tuple
def index_to_edge(i):
    sqrt_val = math.floor((1 + math.sqrt(8 * i + 1)) / 2)
    return (2 * i + sqrt_val - sqrt_val ** 2) // 2, sqrt_val

# Function to convert edge tuple to index
def edge_to_index(v1, v2):
    x = min(v1, v2)
    y = max(v1, v2)
    return (y ** 2 - y + 2 * x) // 2

# Computes (ordered) degree sequence of a graph
def computeDegreeSequence(graph, vertices=None):
    if vertices is None:
        vertices = round((1 + math.sqrt(8 * len(graph) + 1)) / 2)
    degrees = [0] * vertices
    for i in range(len(graph)):
        c = index_to_edge(i)
        degrees[c[0]] += graph[i]
        degrees[c[1]] += graph[i]
    return degrees

# Computes all permutations that can get from one list to another of identical characters
def compute_degree_matchings(input_list, output_list):
    # Create a list containing all the indices for elements in range(len(A))
    indices = list(range(len(output_list)))

    # Generate all permutations of indices
    perms = permutations(indices)

    # Initialize a list to store valid lists C
    valid_lists = []

    # Iterate through each permutation
    for perm in perms:
        # Create a temporary list to represent the image of A under the permutation
        temp_output_list = [output_list[perm[i]] for i in range(len(output_list))]

        # Check if temp_A matches B
        if temp_output_list == input_list:
            valid_lists.append(list(perm))  # Add the permutation (list C) to valid_C_lists

    return valid_lists

# Compute a single edge relabelling function
def precompute_edge_relabelling(vertex_relabelling, p=None):
    if p is None:
        p = len(vertex_relabelling)
    permuted_edges = [None] * ((p * (p - 1)) // 2)
    for i in range(1, p):
        for j in range(i):
            permuted_edges[edge_to_index(i, j)] = edge_to_index(vertex_relabelling[i], vertex_relabelling[j])
    return permuted_edges

# Apply edge relabelling to a given graph
def apply_edge_relabelling(graph, edge_permutation):
    c = len(graph)
    output = c * [None]
    for i in range(c):
        output[edge_permutation[i]] = graph[i]
    return output

# Function to save dictionary to file
def save_dict_to_file(filename, perms_dict):
    # Convert tuple keys to strings
    perms_dict_str_keys = {str(key): value for key, value in perms_dict.items()}
    with open(filename, 'w') as file:
        json.dump(perms_dict_str_keys, file)

# Check if two graphs are isomorphic
def smart_isomorphic(graph1, graph2):
    if len(graph1) != len(graph2):
      return False
    if graph1 == graph2:
      return True
    if graph1.count(0) != graph2.count(0):
      return False
    a = computeDegreeSequence(graph1)
    b = computeDegreeSequence(graph2)
    if sorted(a) != sorted(b):
        return False
    else:
        c = compute_degree_matchings(a, b)
        for permutation in c:
            # Convert list to tuple for hashability
            perm_tuple = tuple(permutation)
            if perm_tuple not in permsDict:
                permsDict[perm_tuple] = precompute_edge_relabelling(permutation)
        if apply_edge_relabelling(graph1, permsDict[perm_tuple]) == graph2:
            return True
    return False

# Function to compute previous subgraph properties
def compute_previous_subgraph_properties(descriptor):
    vertices, edges = descriptor
    lower_bound = max(0, edges - vertices + 1)
    upper_bound = min((vertices - 1) * (vertices - 2) // 2, edges)
    previous_required_computations = [(vertices - 1, i) for i in range(lower_bound, upper_bound + 1)]
    return previous_required_computations

# Remove isomorphic graphs from a list
def remove_isomorphic_graphs(list_of_graphs):
    unique_graphs = []
    for graph in list_of_graphs:
        if not any(smart_isomorphic(graph, existing_graph) for existing_graph in unique_graphs):
            unique_graphs.append(graph)
    return unique_graphs

# Function to compute binary permutations
def compute_binary_permutations(zeros, ones):
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
    backtrack([], zeros, ones)
    return unique_permutations

# Function to fuse previous subgraphs and permutations
def fuse_previous_subgraphs_and_permutations(previous_subgraphs, permutations):
    fused_graphs = []
    for elem_a in previous_subgraphs:
        for elem_b in permutations:
            fused_graphs.append(elem_a + elem_b)
    return fused_graphs

# Function to compute non-isomorphic graphs
def compute_non_isomorphic_graphs(p, q):
    if (p, q) in graphsDict:
        return graphsDict[(p, q)]
    master_list = []
    keys = compute_previous_subgraph_properties((p, q))
    for k in keys:
        if k not in graphsDict:
            compute_non_isomorphic_graphs(k[0], k[1])
    for h in keys:
        temp = compute_binary_permutations(p - 1 + h[1] - q, q - h[1])
        master_list.extend(fuse_previous_subgraphs_and_permutations(graphsDict[h], temp))
    graphsDict[(p, q)] = remove_isomorphic_graphs(master_list)
    return graphsDict[(p, q)]

# Function to compute next available graphs
def compute_next_available_graphs():
    p = 2
    q = 0
    while (p, q) in graphsDict:
        q += 1
        if q > p * (p - 1) // 2:
            p += 1
            q = 0
    return compute_non_isomorphic_graphs(p, q)

# Main computation
graphs =  compute_non_isomorphic_graphs(7, 16)
# compute_non_isomorphic_graphs(8, 16)
# compute_next_available_graphs()

# Convert dictionaries to strings and save to files
graphsDict_str_keys = {str(key): value for key, value in graphsDict.items()}
save_dict_to_file('graphsDict.json', graphsDict_str_keys)
permsDict_str_keys = {str(key): value for key, value in permsDict.items()}
save_dict_to_file('permsDict.json', permsDict_str_keys)

# Print the computed graphs
print(graphs)
