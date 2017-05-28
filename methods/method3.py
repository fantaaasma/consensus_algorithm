from consensus_algorithm.consensus import compute_consensuses_by_complication, compute_consensus_opt1, \
    compute_consensus_opt2
from consensus_algorithm.data import get_complications_dict
from consensus_algorithm.probabilities import probability, compute_aposteriori_for_complications, \
    compute_aposteriori_for_symptoms


def method_3(learn_data, test_data, number_of_complications, consensus_fun):
    probabilities, apost_complications, apost_symptoms = get_probabilities(learn_data, consensus_fun,
                                                                           number_of_complications)
    real, predicted = test(test_data, probabilities, apost_complications, apost_symptoms, number_of_complications)
    return real, predicted


method_3.name = 'metoda 3'


def compute_probabilities(consensuses, views, apost_complications, apost_symptoms):
    probabilities = []
    for i in range(len(consensuses)):
        p = probability(i, consensuses[i], apost_complications, apost_symptoms)
        probabilities.append(p)
    return probabilities


def get_probabilities(learn_views, consensus_fun, number_of_complications):
    apost_complications = compute_aposteriori_for_complications(learn_views, number_of_complications)
    apost_symptoms = compute_aposteriori_for_symptoms(learn_views, apost_complications)
    consensuses = compute_consensuses_by_complication(learn_views, number_of_complications, consensus_fun)
    probabilities = compute_probabilities(consensuses, learn_views, apost_complications, apost_symptoms)

    return probabilities, apost_complications, apost_symptoms


def test(test_views, probabilities, apost_complications, apost_symptoms, number_of_complications):
    predicted = []
    real = []
    for t in test_views:
        real.append(t[-number_of_complications:])
        predicted_complications = [0] * number_of_complications
        for complication_index in range(number_of_complications):
            p = probability(complication_index, t, apost_complications, apost_symptoms)
            if p >= probabilities[complication_index]:
                predicted_complications[complication_index] = 1
        predicted.append(predicted_complications)

    return real, predicted


def show_probabilities_table(data, number_of_complications):
    cd = get_complications_dict()
    apost_complications = compute_aposteriori_for_complications(data, number_of_complications)
    apost_symptoms = compute_aposteriori_for_symptoms(data, apost_complications)

    for i in range(len(apost_symptoms)):
        print('{:35s} {:3.2f} {}'.format(cd[i + 1], 100 * apost_complications[i],
                                         ['%.2f' % (x * 100) for x in apost_symptoms[i]]))

    consensuses_opt1 = compute_consensuses_by_complication(data, number_of_complications, compute_consensus_opt1)
    probabilities1 = compute_probabilities(consensuses_opt1, data, apost_complications, apost_symptoms)

    consensuses_opt2 = compute_consensuses_by_complication(data, number_of_complications, compute_consensus_opt2)
    probabilities2 = compute_probabilities(consensuses_opt2, data, apost_complications, apost_symptoms)

    print('\n\nconsensus opt 1\n')
    for i in range(number_of_complications):
        print('{}\n consensus : {} P(D{}|Sc)={}'.format(cd[i + 1], consensuses_opt1[i], i, 100 * probabilities1[i]))

    print('\n\nconsensus opt 2\n')
    for i in range(number_of_complications):
        print('{}\n consensus : {} P(D{}|Sc)={}'.format(cd[i + 1], consensuses_opt2[i], i, 100 * probabilities2[i]))
