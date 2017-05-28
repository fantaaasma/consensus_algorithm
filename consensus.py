import random

# 1-opt
from consensus_algorithm.data import get_symptom_vectors_for_given_complication


def compute_consensus_opt1(data):
    n = len(data[0])
    consensus = [0] * n
    for i in range(n):
        for e in data:
            consensus[i] += e[i]

    for i in range(n):
        consensus[i] = int(0.5 + consensus[i] / len(data))

    return consensus


compute_consensus_opt1.name = 'opt-1'


# 2-opt

def compute_consensus_opt2(data):
    vector_length = len(data[0])
    consensus = generate_random_vector(vector_length)
    previous_distance = sum_of_distances_power_2(consensus, data)

    for i in range(vector_length):
        consensus[i] = 0 if consensus[i] else 1
        new_distance = sum_of_distances_power_2(consensus, data)
        if new_distance < previous_distance:
            previous_distance = new_distance
        else:
            consensus[i] = 0 if consensus[i] else 1

    return consensus


compute_consensus_opt2.name = 'opt-2'


def distance(a, b):
    single_distance = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            single_distance += 1
    return single_distance


def sum_of_distances_power_2(c, X):
    sum_of_all_distances = 0
    for x in X:
        sum_of_all_distances += distance(c, x) ** 2

    return sum_of_all_distances


def generate_random_vector(n):
    return [random.randint(0, 1) for x in range(n)]


# brutal force
def int_to_bit_array(int_number, length):
    return [int(x) for x in list(str('{0:0' + str(length) + 'b}').format(int_number))]


def generate_space(vector_length):
    space = []
    for i in range(2 ** vector_length):
        space.append(int_to_bit_array(i, vector_length))
    return space


def compute_consensus_opt2_brutal_force(X, distance_fun):
    vector_length = len(X[0])

    space = generate_space(vector_length)

    all_distances = []

    for i in range(len(space)):
        all_distances.append(distance_fun(space[i], X))

    index_of_min_distance = all_distances.index(min(all_distances))

    return space[index_of_min_distance]


def compute_consensuses_by_complication(data, number_of_complications, consensus_fun):
    consensuses = []

    for i in range(number_of_complications):
        consensus = consensus_fun(get_symptom_vectors_for_given_complication(i, number_of_complications, data))
        consensuses.append(consensus)

    return consensuses
