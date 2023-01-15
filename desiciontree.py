#!/usr/bin/python3

import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
from sklearn import tree
import graphviz

TEST_SIZE = 0.3
dataset = pd.read_csv('10_perc.txt')

X = dataset.iloc[:, 0].values
y = dataset.iloc[:, 1].values

# train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = TEST_SIZE, random_state = 0)

X_train = X_train.reshape(-1, 1)
X_test = X_test.reshape(-1, 1)

classifier = DecisionTreeClassifier(criterion = 'entropy', random_state=0)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

cm = confusion_matrix(y_test, y_pred)

total = len(X_test)

confusion = cm[0][1] + cm[1][0] 

ratio = (total - confusion) * 100 / total
dot_data = tree.export_graphviz(classifier, out_file=None)
graph = graphviz.Source(dot_data)
graph.render("iris")

print("{:.2f}".format(ratio))
