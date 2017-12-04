import numpy as np
from numpy.random import seed


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


class AdalineGD(object):
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


class AdalineSGD(object):
    def __init__(self, eta=0.01, epocs=10, shuffle=True, random_state=None):
        self.eta = eta
        self.epocs = epocs
        self.w_initialized = False
        self.shuffle = shuffle
        self._cost = []
        if random_state:
            seed(random_state)

    def fit(self, x, y):
        self._initialize_weights(x.shape[1])
        self._cost = []
        for i in range(self.epocs):
            if self.shuffle:
                x, y = self._shuffle(x, y)
            cost = []
            for xi, target in zip(x, y):
                cost.append(self._update_weights(xi, target))
            avg_cost = sum(cost) / len(y)
            self._cost.append(avg_cost)

        return self

    def partial_fit(self, x, y):
        """Fit training data without reinitializing the weights"""
        if not self.w_initialized:
            self._initialize_weights(x.shape[1])
        if y.ravel().shape[0] > 1:
            for xi, target in zip(x, y):
                self._update_weights(xi, target)
        else:
            self._update_weights(x, y)

        return self

    def net_input(self, x):
        """Calculate net input"""
        return np.dot(x, self.w_[1:]) + self.w_[0]

    def predict(self, x):
        """Return class label after unit step"""
        return np.where(self.net_input(x) >= 0.0, 1, -1)

    def _shuffle(self, x, y):
        """Shuffle training data"""
        r = np.random.permutation(len(y))
        return x[r], y[r]

    def _initialize_weights(self, m):
        """Initialize weights to zeros"""
        self.w_ = np.zeros(1 + m)
        self.w_initialized = True

    def _update_weights(self, xi, target):
        """Apply Adaline learning rule to update the weights"""
        output = self.net_input(xi)
        error = (target - output)
        self.w_[1:] += self.eta * xi.dot(error)
        self.w_[0] += self.eta * error
        cost = 0.5 * error ** 2

        return cost
