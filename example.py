# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.metrics import accuracy_score

from twd import TWD

data = pd.read_csv('data/sample.csv', header=None).values

x_train = data[:-10, :-1]
y_train = data[:-10, -1]
x_test = data[-10:, :-1]
y_test = data[-10:, -1]

model = TWD()
y_pred = model.predict(x_train, y_train, x_test)
score = accuracy_score(y_test, y_pred)

print("y true label >>>", y_test)
print("y predicted label >>>", y_pred)
print("accuracy score >> {:.1f}%".format(score*100))


"""Result
y true label >>> ['1' '1' '1' '0' '1' '1' '1' '1' '0' '0']
y predicted label >>> ['1' '1' '1' '0' '1' '1' '1' '0' '0' '0']
accuracy score >> 90.0%
"""
