import 



# Function that takes in number of edges q and number of vertices p.
# List every permutation with q 1's and p(p-1)/2-q 0's and put them in a master list
# For each permutation x in the master list, compute all the isomorphic sequences and each time you find another isomorphic sequence, remove it from the master list if it is still there and place it into the list of sequences isomorphic x.
# Return one element from each list of isomorphic sequences

# compute_binary_permutations(p,q):
# generate all permutations of q 1's and p(p-1)/2-q 0's and return them as nested lists in a master list


# compute_vertex_relabellings(p):
# precompute all the permutations of [0...p-1] and return them nested in a list


# convert_edge_to_index(v1,v2):
# get the index of the edge between v1 and v2.



# precompute_edge_relabellings(p,vertex_relabellings):
# for each given permutation of [0...p-1], calculate a list describing which index each edege goes to after permuting the vertices


# list_isomorphic_sequences(binary_sequence, edge_relabellings):
# apply each edge relabelling to binary_sequence and nest them in a list


# group_isomorphic_sequences(binary_sequences, edge_relabellings):
# start with two lists "grouped_sequences" and "binary_sequences".
# for each binary sequence in binary_sequences, compute list_isomorphic_sequences(binary_sequence, edge_relabellings)
# and append the list of all isomorphic sequences to grouped_sequences in a nested list while also removing each of 
#them from binary_sequences, repeat this until binary_sequences is empty.


#todo: make a class that holds one string
#implement each of these functions
#implement a function to take one of these string classes and draw it