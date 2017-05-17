from consensus_algorithm.consensus import compute_consensus_opt1, compute_consensus_opt2, compute_consensus_opt2_brutal_force
from consensus_algorithm.ncb import BernoulliNB
from consensus_algorithm.data import get_views, get_cases, get_complications_dict

NUMBER_OF_COMPLICATIONS = 13


cases = get_cases()

views = get_views(cases,
                  filter_additional_diseases=[0, 3, 4, 7, 8],
                  filter_operation_type=[1, 2, 3, 4, 5],
                  filter_complications=[x + 1 for x in range(NUMBER_OF_COMPLICATIONS)]
                  )


NUMBER_OF_SYMPTOMS = len(views[0]) - NUMBER_OF_COMPLICATIONS

def compute_aposteriori(data):
    N = len(data)
    n = len(data[0])
    prob = [0] * n
    for e in data:
        for i in range(n):
            prob[i] += e[i]

    return [p/N for p in prob]



def compute_aposteriori_for_symptom(data, apost_complications, index_of_symptom, index_of_complication):
    N = len(data)
    n = len(data[0])
    prob = 0
    for e in data:
        s = e[index_of_symptom]
        c = e[n - NUMBER_OF_COMPLICATIONS + index_of_complication]
        if c:
            prob += s

    return (prob/N)/apost_complications[index_of_complication]


def compute_aposteriori_for_symptoms(views, apost_complications):
    apost_symptoms = [None] * NUMBER_OF_COMPLICATIONS
    for i in range(NUMBER_OF_COMPLICATIONS):
        apost_symptoms[i] = [None] * NUMBER_OF_SYMPTOMS
        for j in range(NUMBER_OF_SYMPTOMS):
            apost_symptoms[i][j] = compute_aposteriori_for_symptom(views, apost_complications, j, i)

    return apost_symptoms

def probability(complication_number, symptoms_vector, apost_complications, apost_symptoms):
    denominator = 0
    for k in range(len(apost_complications)):
        x = apost_complications[k]
        #print('x',x)
        for j in range(len(apost_symptoms[k])):
            x *= apost_symptoms[k][j] if symptoms_vector[j] else 1 - apost_symptoms[k][j]
            #print('x',x)
        denominator += x
        #print('denominator',denominator)
    #print('denominator', denominator)

    numerator = 0
    x = apost_complications[complication_number]
    #print('x',x)
    for j in range(len(apost_symptoms[complication_number])):
        x *= apost_symptoms[complication_number][j] if symptoms_vector[j] else 1 - apost_symptoms[complication_number][j]
        #print('x',x)
    numerator += x
    #print('numerator', numerator)
    return numerator/denominator



cd = get_complications_dict()
apost_complications = compute_aposteriori(views)[-NUMBER_OF_COMPLICATIONS:]
apost_symptoms = compute_aposteriori_for_symptoms(views, apost_complications)

for i in range(len(apost_symptoms)):
    print('{:35s} {:3.2f} {}'.format(cd[i+1], 100*apost_complications[i], ['%.2f' % (x *100) for x in apost_symptoms[i]]))

p = probability(0,[ x % 2 for x in range(NUMBER_OF_SYMPTOMS)], apost_complications, apost_symptoms)
print(p)