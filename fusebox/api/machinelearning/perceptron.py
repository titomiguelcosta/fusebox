import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score

AWFUL = 0
OK = 1
GREAT = 2
AWESOME = 3


def category(value):
    if 1 <= value < 3:
        return AWFUL
    elif 3 <= value < 5:
        return OK
    elif 5 <= value < 7:
        return GREAT
    elif 7 <= value <= 9:
        return AWESOME
    else:
        return np.nan


data = pd.read_csv("fusebox.csv")
X = data.iloc[:, list(range(4, 14))]

# current rate is a real value from 1 to 9
# mapping to categories: 1-3 -> Awful (1), 3-5 -> OK (2), 5-7 -> Great (3), 7-9 -> Awesome (4)
y = data["rate"].apply(category)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
sc = StandardScaler()
sc.fit(X_train)

X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)

ppn = Perceptron(n_iter=400, eta0=0.001, random_state=0)
ppn.fit(X_train_std, y_train)


y_pred = ppn.predict(X_test_std)
print('Misclassified samples: %d' % (y_test != y_pred).sum())
print('Accuracy: %.2f' % accuracy_score(y_test, y_pred))
