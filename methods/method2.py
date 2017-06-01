from consensus_algorithm.probabilities import probability, compute_aposteriori_for_complications, \
    compute_aposteriori_for_symptoms

PROBABILITY_THRESHOLD = 0.5


def method_2(learn_data, test_data, number_of_complications, consensus_fun):
    apost_complications, apost_symptoms = get_probabilities(learn_data, number_of_complications)
    real, predicted = test(test_data, apost_complications, apost_symptoms, number_of_complications)
    return real, predicted


method_2.name = '2. Bayes'


def get_probabilities(learn_views, number_of_complications):
    apost_complications = compute_aposteriori_for_complications(learn_views, number_of_complications)
    apost_symptoms = compute_aposteriori_for_symptoms(learn_views, apost_complications)

    return apost_complications, apost_symptoms


def test(test_views, apost_complications, apost_symptoms, number_of_complications):
    predicted = []
    real = []
    for t in test_views:
        real.append(t[-number_of_complications:])
        predicted_complications = [0] * number_of_complications
        for complication_index in range(number_of_complications):
            p = probability(complication_index, t, apost_complications, apost_symptoms)
            if p >= PROBABILITY_THRESHOLD:
                predicted_complications[complication_index] = 1
        predicted.append(predicted_complications)

    return real, predicted
