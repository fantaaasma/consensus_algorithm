
def compute_single_distance(a, b):
    single_distance = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            single_distance += 1
    return single_distance


def distance1(c, X):

    sum_of_all_distances = 0
    for x in X:
        sum_of_all_distances += compute_single_distance(c, x)

    return sum_of_all_distances


def distance2(c, X):
    sum_of_all_distances = 0
    for x in X:
        sum_of_all_distances += compute_single_distance(c, x) ** 2

    return sum_of_all_distances


def int_to_bit_array(int_number, length):
    return [int(x) for x in list(str('{0:0' + str(length) + 'b}').format(int_number))]


def generate_space(vector_length):
    space = []
    for i in range(2 ** vector_length):
        space.append(int_to_bit_array(i, vector_length))
    return space


def compute_consensus(X, distance_fun):
    vector_length = len(X[0])

    space = generate_space(vector_length)

    all_distances = []

    for i in range(len(space)):
        all_distances.append(distance_fun(space[i], X))

    index_of_min_distance = all_distances.index(min(all_distances))

    return space[index_of_min_distance]


def compare_cons(data):
    print('dane wejściowe:')
    for x in data:
        print(x)

    print('consensus opt-1 =', compute_consensus(data, distance1))
    print('consensus opt-2 =', compute_consensus(data, distance2))


def compute_consensus_opt1(data):
    n = len(data[0])
    consensus = [0] * n
    for e in data:
        for i in range(n):
            consensus[i] += e[i]

    for i in range(n):
        consensus[i] = int(0.5 + consensus[i]/len(data))

    return consensus


def compute_consensus_opt2(data):
    return compute_consensus(data, distance2)
