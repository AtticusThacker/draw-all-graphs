import itertools
import math

# Function to convert an edge (a, b) to its corresponding index in the permutation
def edge_to_index(a, b):
    x = min(a, b)
    y = max(a, b)
    return (y**2 - y + 2*x) // 2

# Function to convert an index in the permutation to the corresponding edge (a, b)
def index_to_edge(i):
    sqrt_val = math.floor((1 + math.sqrt(8*i + 1)) / 2)
    return (2*i + sqrt_val - sqrt_val**2) // 2, sqrt_val

# Function to generate all permutations of numbers from 0 to p-1
def list_permutations(p):
    numbers = list(range(p))
    return list(itertools.permutations(numbers))

# ----- This part is probably doing way more than it has to, maybe try to have it just compute the mappings once at the beginning, if possible
# Function to permute edges based on a given permutation of vertices
def compute_edge_permutations(permutation, edges):
    vertices = len(permutation)
    permuted_edges = [None] * len(edges)
    for i in range(1, vertices):
        for j in range(i):
            permuted_edges[edge_to_index(permutation[i], permutation[j])] = edges[edge_to_index(i, j)]
    return permuted_edges

# Function to count cycles and their lengths in a given array representing a permutation
def count_cycles_with_lengths(arr):
    def find_cycle_length(start):
        current = start
        cycle_length = 0
        while not visited[current]:
            visited[current] = True
            current = arr[current]
            cycle_length += 1
        return cycle_length

    n = len(arr)
    visited = [False] * n
    cycle_lengths = []

    for i in range(n):
        if not visited[i]:
            cycle_length = find_cycle_length(i)
            cycle_lengths.append(cycle_length)

    cycles = len(cycle_lengths)
    return cycles, cycle_lengths

# Function to generate all possible sums using each number from the input list either once or never
def generate_sums(nums):
    def generate_combinations(index, curr_sum):
        if index == len(nums):
            sums.append(curr_sum)
            return

        generate_combinations(index + 1, curr_sum + nums[index])  # Include current number
        generate_combinations(index + 1, curr_sum)  # Exclude current number

    sums = []
    generate_combinations(0, 0)
    return sums

# Function to classify how many graphs of each number of edges there are
def classify_by_edges(cycle_lengths, c):
    totals = []
    counts = {}
    for x in cycle_lengths:
        totals.extend(generate_sums(x))
    for y in range(max(totals) + 1):
        counts[y] = totals.count(y) // c
    return counts

# Function implementing Burnside's Lemma to count the number of distinct graphs with p vertices, which are then sorted by the number of edges
def burnside_count(p):
    total = 0
    cycle_info = []
    permutations = list_permutations(p)
    permuted_edges = [range((p**2 - p) // 2) for _ in range(len(permutations))]
    for i, permutation in enumerate(permutations):
      cycles, cycle_lengths = count_cycles_with_lengths(compute_edge_permutations(permutation, permuted_edges[i]))
      total += 2**cycles
      cycle_info.append(cycle_lengths) 
    c = math.factorial(p)
    return total // c, classify_by_edges(cycle_info, c)


print(burnside_count(6))
