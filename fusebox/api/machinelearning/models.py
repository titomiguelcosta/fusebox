import numpy as np


class Perceptron(object):
    def __init__(self, eta=0.1, epocs=10):
        """
        :param eta: learning rate
        :param epocs: number of interactions
        """
        self.eta = eta
        self.epocs = epocs
        self._errors = []
        self._w = np.array([])

    def fit(self, x, y):
        self._w = np.zeros(1 + x.shape[1])
        self._errors = []

        for _ in range(self.epocs):
            errors = 0
            for xi, target in zip(x, y):
                update = self.eta * (target - self.predict(xi))
                self._w[1:] += update * xi
                self._w[0] = update
                errors += int(update != 0)

            self._errors.append(errors)

    def predict(self, x):
        return np.where(self._net_input(x) >= 0, 1, -1)

    def _net_input(self, x):
        return np.dot(x, self._w[1:]) + self._w[0]


class Adaline(object):
    def __init__(self, eta=0.1, epocs=10):
        """
        :param eta: learning rate
        :param epocs: number of interactions
        """
        self.eta = eta
        self.epocs = epocs
        self._cost = []
        self._w = np.array([])

    def fit(self, x, y):
        self._w = np.zeros(1 + x.shape[1])
        self._cost = []

        for _ in range(self.epocs):
            output = self._net_input(x)
            errors = y - output
            self._w[1:] += self.eta * x.T.dot(errors)
            self._w[0] += self.eta * errors.sum()
            cost = (errors ** 2).sum() / 2.0
            self._cost.append(cost)

        return self

    def predict(self, x):
        return np.where(self._net_input(x) >= 0, 1, -1)

    def _net_input(self, x):
        return np.dot(x, self._w[1:]) + self._w[0]


if __name__ == "__main__":
    import pandas as pd
    df = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data", header=None)
    y = df.iloc[0:100, 4].values
    y = np.where(y == 'Iris-setosa', -1, 1)
    X = df.iloc[0:100, [0, 2]].values

    ppn = Perceptron()
    ppn.fit(X, y)
    print(ppn.predict(np.array([5.0, 1.4])))
    print(ppn.predict(np.array([7.0, 4.7])))
    print(ppn._errors)

    adl = Adaline(eta=0.01, epocs=15)
    X[:, 0] = (X[:, 0] - X[:, 0].mean()) / X[:, 0].std()
    X[:, 1] = (X[:, 1] - X[:, 1].mean()) / X[:, 1].std()
    adl.fit(X, y)
    print(adl.predict(np.array([5.0, 1.4])))
    print(adl.predict(np.array([7.0, 4.7])))
    print(adl._cost)
