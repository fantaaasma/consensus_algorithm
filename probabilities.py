def compute_aposteriori(data):
    N = len(data)
    n = len(data[0])
    prob = [0] * n
    for e in data:
        for i in range(n):
            prob[i] += e[i]

    return [p / N for p in prob]


def compute_aposteriori_for_complications(data, number_of_complications):
    return compute_aposteriori(data)[-number_of_complications:]


def compute_aposteriori_for_symptom(data, apost_complications, index_of_symptom, index_of_complication):
    number_of_complications = len(apost_complications)
    N = len(data)
    n = len(data[0])
    prob = 0
    for e in data:
        s = e[index_of_symptom]
        c = e[n - number_of_complications + index_of_complication]
        if c:
            prob += s

    return (prob / N) / apost_complications[index_of_complication]


def compute_aposteriori_for_symptoms(views, apost_complications):
    number_of_complications = len(apost_complications)
    vector_len = len(views[0])
    number_of_symptoms = vector_len - number_of_complications
    apost_symptoms = [None] * number_of_complications
    for i in range(number_of_complications):
        apost_symptoms[i] = [None] * number_of_symptoms
        for j in range(number_of_symptoms):
            apost_symptoms[i][j] = compute_aposteriori_for_symptom(views, apost_complications, j, i)

    return apost_symptoms


def probability(complication_number, symptoms_vector, apost_complications, apost_symptoms):
    denominator = 0
    for i in range(len(apost_complications)):
        x = apost_complications[i]
        for j in range(len(apost_symptoms[i])):
            x *= apost_symptoms[i][j] if symptoms_vector[j] else 1 - apost_symptoms[i][j]
        denominator += x

    numerator = 0
    x = apost_complications[complication_number]
    for j in range(len(apost_symptoms[complication_number])):
        x *= apost_symptoms[complication_number][j] if symptoms_vector[j] else 1 - apost_symptoms[complication_number][
            j]
    numerator += x
    return numerator / denominator
