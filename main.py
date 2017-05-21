from consensus_algorithm.consensus import compute_consensus_opt1, compute_consensus_opt2, compute_consensus_opt2_brutal_force
from consensus_algorithm.ncb import BernoulliNB
from consensus_algorithm.data import get_views, get_cases, get_complications_dict

NUMBER_OF_COMPLICATIONS = 13
FOLD_NUMBER = 4

cases = get_cases()

views = get_views(cases,
                  filter_additional_diseases=[0, 3, 4, 7, 9, 11],
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


def get_cases_with_complication(complication_number, views):
    cases_with_complication = []
    for v in views:
        if v[NUMBER_OF_SYMPTOMS + complication_number]:
            cases_with_complication.append(v)

    return cases_with_complication


def get_cases_by_complication(views):
    cases_by_complication =[]
    for i in range(NUMBER_OF_COMPLICATIONS):
        cases_by_complication.append(get_cases_with_complication(i, views))

    return cases_by_complication

def compute_consensuses(views, consensus_fun):
    consensuses = []
    for i in range(NUMBER_OF_COMPLICATIONS):
        consensuses.append(consensus_fun(get_cases_with_complication(i, views))[:NUMBER_OF_SYMPTOMS])

    return consensuses

def compute_probabilities(consensuses, views, apost_complications, apost_symptoms):
    probabilities = []
    for i in range(len(consensuses)):
        p = probability(i, consensuses[i], apost_complications, apost_symptoms)
        probabilities.append(p)
    return probabilities

# cd = get_complications_dict()
# apost_complications = compute_aposteriori(views)[-NUMBER_OF_COMPLICATIONS:]
# apost_symptoms = compute_aposteriori_for_symptoms(views, apost_complications)
#
# for i in range(len(apost_symptoms)):
#     print('{:35s} {:3.2f} {}'.format(cd[i+1], 100*apost_complications[i], ['%.2f' % (x *100) for x in apost_symptoms[i]]))
#
#
# consensuses_opt1 = compute_consensuses(views, compute_consensus_opt1)
# probabilities1 = compute_probabilities(consensuses_opt1, views, apost_complications, apost_symptoms)
#
# consensuses_opt2 = compute_consensuses(views, compute_consensus_opt2)
# probabilities2 = compute_probabilities(consensuses_opt2, views, apost_complications, apost_symptoms)
#
#
#
# print('\n\nconsensus opt 1\n')
# for i in range(NUMBER_OF_COMPLICATIONS):
#     print('{}\n consensus : {} P(D{}|Sc)={}'.format(cd[i+1], consensuses_opt1[i], i, 100 * probabilities1[i]))
#
# print('\n\nconsensus opt 2\n')
# for i in range(NUMBER_OF_COMPLICATIONS):
#     print('{}\n consensus : {} P(D{}|Sc)={}'.format(cd[i+1], consensuses_opt2[i], i, 100 * probabilities2[i]))
# #
# def f():
#     for complication_number in range(NUMBER_OF_COMPLICATIONS):
#         cases = get_cases_with_complication(complication_number, views)
#         probabilities = []
#         threshold = probabilities1[complication_number]
#         accuracy = 0
#         for case in cases:
#             p = probability(complication_number, case, apost_complications, apost_symptoms)
#             if p > threshold:
#                 accuracy += 1
#
#         n = len(cases)
#         accuracy /= n
#
#         print('komplikacja {} dokladnosc {}'.format(complication_number, accuracy))




def get_folds(views, fold_nuber):
    folds = [[]] * fold_nuber
    # TODO change to random
    for i in range(len(views)):
        folds[i%FOLD_NUMBER].append(views[i])
    return folds



def learn(learn_views, consensus_fun=compute_consensus_opt1):
    apost_complications = compute_aposteriori(views)[-NUMBER_OF_COMPLICATIONS:]
    apost_symptoms = compute_aposteriori_for_symptoms(views, apost_complications)
    consensuses = compute_consensuses(views, consensus_fun)
    probabilities = compute_probabilities(consensuses, views, apost_complications, apost_symptoms)

    return probabilities, apost_complications, apost_symptoms

def test(test_views, probabilities, apost_complications, apost_symptoms ):

    predicted = []
    real = []
    for t in test_views:
        real.append(t[-NUMBER_OF_COMPLICATIONS:])
        predicted_complications = [0] * NUMBER_OF_COMPLICATIONS
        for complication_index in range(NUMBER_OF_COMPLICATIONS):
            p = probability(complication_index, t,  apost_complications, apost_symptoms)
            if p >= probabilities[complication_index]:
                predicted_complications[complication_index] = 1
        predicted.append(predicted_complications)

    return real, predicted

def get_stats(real, predicted):
    stats_for_comp = []
    for c_index in range(NUMBER_OF_COMPLICATIONS):
        tp = 0
        tn = 0
        fp = 0
        fn = 0
        for i in range(len(real)):
            if real[i][c_index] == 1:
                if predicted[i][c_index] == 1:
                    tp += 1
                else:
                    fn += 1
            else:
                if predicted[i][c_index] == 1:
                    fp += 1
                else:
                    tn += 1

        stats_for_comp.append((tp, tn, fp, fn))

    return stats_for_comp


def show_stats(stats):
    for i in range(NUMBER_OF_COMPLICATIONS):
        print('\nkomplikacja {}'.format(i))
        tp, tn, fp, fn = stats[i]
        accuracy = (tp + tn) / (tp + tn + fp + fn)
        print('poprawność klasyfikacji:', accuracy)

def learn_and_test(learn_views, test_views):
    probabilities, apost_complications, apost_symptoms = learn(learn_views)
    real, predicted = test(test_views, probabilities, apost_complications, apost_symptoms)
    stats = get_stats(real, predicted)
    show_stats(stats)


folds = get_folds(views, FOLD_NUMBER)

learn_and_test(views, views)