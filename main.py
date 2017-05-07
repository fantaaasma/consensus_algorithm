from consensus_algorithm.consensus import compute_consensus_opt1
from consensus_algorithm.ncb import BernoulliNB

# TODO te dane będą pobierane z bazy danych
complications = [
  [0, 1, 0],
  [0, 1, 1],
  [0, 0, 1],
]

no_complications = [
  [1, 0, 0],
  [1, 1, 0],
  [1, 0, 1],
]

patient_data = [
    [1, 0, 1],
    [0, 1, 1],
    [0, 1, 0],
    [1, 0, 0]
]

class Algorithm:

    def __init__(self, complications_data, no_complications_data, consensus_fun=compute_consensus_opt1):
        self.complications_data = complications_data
        self.no_complications_data = no_complications_data
        self.nb = BernoulliNB(complications_data, no_complications_data)
        self.consensus = consensus_fun(complications_data)
        print('consensus', self.consensus)

    def __get_consensus_probability(self, input_vector):
        if len(input_vector) != len(self.consensus):
            raise Exception('Wektor symptomow nieprawidlowej dlugosci')
        n = len(input_vector)
        probability = 0
        for i in range(n):
            if self.consensus[i] == input_vector[i]:
                probability += 1

        return probability / n

    def __get_bayes_probability(self, input_vector):
        return self.nb.get_probabilities(input_vector)[0]

    def compute(self, input_vector):
        consensus_probability = self.__get_consensus_probability(input_vector)
        bayes_probability = self.__get_bayes_probability(input_vector)
        print('pc={:.2f}  \npb={:.2f}'.format(consensus_probability, bayes_probability))
        return (consensus_probability + bayes_probability) / 2

algorithm = Algorithm(complications, no_complications, compute_consensus_opt1)

for p in patient_data:
    print('symptomy ', p)
    complication_probability = algorithm.compute(p)
    print('prawdopodbienstwo powiklan = {:.2f}%'.format(complication_probability * 100))
