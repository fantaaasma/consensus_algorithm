from consensus_algorithm.data import get_symptom_vectors_for_given_complication
from consensus_algorithm.ncb import BernoulliNB
#
# complications = [
#   [0, 1, 0],
#   [0, 1, 1],
#   [0, 0, 1],
# ]
#
# no_complications = [
#   [1, 0, 0],
#   [1, 1, 0],
#   [1, 0, 1],
# ]
#
# patient_data = [
#     [1, 0, 1],
#     [0, 1, 1],
#     [0, 1, 0],
#     [1, 0, 0]
# ]
#
# class Algorithm:
#
#     def __init__(self, complications_data, no_complications_data, consensus_fun=compute_consensus_opt1):
#         self.complications_data = complications_data
#         self.no_complications_data = no_complications_data
#         self.nb = BernoulliNB(complications_data, no_complications_data)
#         self.consensus = consensus_fun(complications_data)
#         print('consensus', self.consensus)
#
#     def __get_consensus_probability(self, input_vector):
#         if len(input_vector) != len(self.consensus):
#             raise Exception('Wektor symptomow nieprawidlowej dlugosci')
#         n = len(input_vector)
#         probability = 0
#         for i in range(n):
#             if self.consensus[i] == input_vector[i]:
#                 probability += 1
#
#         return probability / n
#
#     def __get_bayes_probability(self, input_vector):
#         return self.nb.get_probabilities(input_vector)[0]
#
#     def compute(self, input_vector):
#         consensus_probability = self.__get_consensus_probability(input_vector)
#         bayes_probability = self.__get_bayes_probability(input_vector)
#         print('pc={:.2f}  \npb={:.2f}'.format(consensus_probability, bayes_probability))
#         return (consensus_probability + bayes_probability) / 2
#
# algorithm = Algorithm(complications, no_complications, compute_consensus_opt1)
#
# for p in patient_data:
#     print('symptomy ', p)
#     complication_probability = algorithm.compute(p)
#     print('prawdopodbienstwo powiklan = {:.2f}%'.format(complication_probability * 100))
#
#
#






def test(data, ncbs, number_of_complications):
    real = []
    predicted = []

    for patient in data:
        real.append(patient[-number_of_complications:])
        predicted_complications = [0] * number_of_complications
        symptoms = patient[:-number_of_complications]

        has_complication = 0

        for i in range(len(ncbs)):
            p = ncbs[i].get_probabilities(symptoms)[0]
            if p >= 0.5:
                predicted_complications[i+ 1] = 1
                has_complication = 1

            if not has_complication:
                predicted_complications[0] = 1

        predicted.append(predicted_complications)

    return real, predicted


def method_4(learn_data, test_data, number_of_complications, consensus_fun):

    no_complications_data = get_symptom_vectors_for_given_complication(0, number_of_complications, learn_data)

    ncbs = []

    for i in range(1, number_of_complications):
        complications_data = get_symptom_vectors_for_given_complication(i, number_of_complications, learn_data)
        ncbs.append(BernoulliNB(complications_data, no_complications_data))


    real, predicted = test(test_data, ncbs, number_of_complications)
    return real, predicted


method_4.name = '4. naiwny klasyfikator bayesowski'
