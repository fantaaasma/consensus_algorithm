from consensus_algorithm.consensus import compute_consensuses_by_complication


def test(data, consensuses, number_of_complications):
    real = []
    predicted = []

    for patient in data:
        real.append(patient[-number_of_complications:])
        predicted_complications = [0] * number_of_complications
        symptoms = patient[:-number_of_complications]

        for i in range(len(consensuses)):
            if consensuses[i] == symptoms:
                predicted_complications[i] = 1

        predicted.append(predicted_complications)

    return real, predicted


def method_1(learn_data, test_data, number_of_complications, consensus_fun):
    consensuses = compute_consensuses_by_complication(learn_data, number_of_complications, consensus_fun)
    real, predicted = test(test_data, consensuses, number_of_complications)
    return real, predicted


method_1.name = 'metoda 1'
