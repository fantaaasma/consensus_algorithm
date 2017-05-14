from consensus_algorithm.consensus import compute_consensus_opt1
from consensus_algorithm.ncb import BernoulliNB
from consensus_algorithm.data import get_views, get_cases, get_complications_dict

NUMBER_OF_COMPLICATIONS = 13
# # TODO te dane będą pobierane z bazy danych
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


cases = get_cases()




views = get_views(cases,
                  filter_additional_diseases=[0, 3, 4, 7],
                  filter_operation_type=[1, 2, 3],
                  filter_complications=[x + 1 for x in range(NUMBER_OF_COMPLICATIONS)]
                  )


NUMBER_OF_SYMPTOMS = len(views[0]) - NUMBER_OF_COMPLICATIONS

# complications_cases = []
# for v in views[:50]:
#     if v[-1] == 0:
#         complications_cases.append(v[:-1])

# for v in views:
#     print(v)


def compute_aposteriori(data):
    N = len(data)
    n = len(data[0])
    prob = [0] * n
    for e in data:
        for i in range(n):
            prob[i] += e[i]

    return [p/N for p in prob]

apost_complications = compute_aposteriori(views)[-NUMBER_OF_COMPLICATIONS:]


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

s = [None] * NUMBER_OF_COMPLICATIONS
for i in range(NUMBER_OF_COMPLICATIONS):
    s[i] = [None] * NUMBER_OF_SYMPTOMS
    for j in range(NUMBER_OF_SYMPTOMS):
        s[i][j] = compute_aposteriori_for_symptom(views, apost_complications , j, i)


cd = get_complications_dict()

for i in range(len(s)):
    print('{:35s} {:3.2f} {}'.format(cd[i+1], 100*apost_complications[i], ['%.2f' % (x *100) for x in s[i]]))
#print('consensus\n',compute_consensus_opt1(complications_cases))