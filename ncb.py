import numpy as np

data = np.array([
    [0, 1, 0],
    [0, 1, 1],
    [0, 0, 1],
    [1, 0, 0],
    [1, 1, 0],
    [1, 0, 1]
])

complications = np.array([
    0,
    0,
    0,
    1,
    1,
    1
])

data_set = []

for i in range(len(data)):
    data_set.append(data[i] + [complications[i]])


def print_list(s, msg=''):
    print(msg)
    for e in s:
        print(e)


class BernoulliNB(object):
    def __init__(self, data1, data2):
        self.alpha = 1.0
        X = []
        y = []
        for e in data1:
            X.append(e)
            y.append(0)

        for e in data2:
            X.append(e)
            y.append(1)

        self.fit(np.array(X), np.array(y))

    def fit(self, X, y):
        count_sample = X.shape[0]
        separated = [[x for x, t in zip(X, y) if t == c] for c in np.unique(y)]
        self.class_log_prior_ = [np.log(len(i) / count_sample) for i in separated]
        count = np.array([np.array(i).sum(axis=0) for i in separated]) + self.alpha
        smoothing = 2 * self.alpha
        n_doc = np.array([len(i) + smoothing for i in separated])
        self.feature_prob_ = count / n_doc[np.newaxis].T
        return self

    def predict_log_proba(self, X):
        return [(np.log(self.feature_prob_) * x + \
                 np.log(1 - self.feature_prob_) * np.abs(x - 1)
                 ).sum(axis=1) + self.class_log_prior_ for x in X]

    def get_probabilities(self, input_vector):
        X = np.array([input_vector])
        probabilities = np.exp(self.predict_log_proba(X))[0]
        p1 = probabilities[0]
        p2 = probabilities[1]
        a = 1 / (p1 + p2)
        return a * probabilities

    def predict(self, X):
        return np.argmax(self.predict_log_proba(X), axis=1)
