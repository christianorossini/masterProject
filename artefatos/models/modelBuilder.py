# Load libraries
import pandas as pd
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation

from sklearn.tree import export_graphviz
from sklearn.externals.six import StringIO  
from IPython.display import Image  
import pydotplus

import numpy as np
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support
from matplotlib import pyplot as plt

cSmell = "cdsbp"

# load dataset
dfCs = pd.read_csv("../datasets/oracle_dataset/{0}.csv".format(cSmell));

#split dataset in features and target variable
if(cSmell in ["gc","cdsbp"]):
    feature_cols = dfCs.iloc[:,3:46].columns
else:
    feature_cols = dfCs.iloc[:,3:30].columns

#feature_cols = dfCs.iloc[:,3:30].columns
X = dfCs[feature_cols] # Features
y = dfCs["is_{0}".format(cSmell)] # Target variable

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1) # 70% training and 30% test

# Create Decision Tree classifer object
#clf = DecisionTreeClassifier()
#clf = DecisionTreeClassifier(criterion="entropy", max_depth=3)
clf = DecisionTreeClassifier(criterion="entropy")

# Train Decision Tree Classifer
clf = clf.fit(X_train,y_train)

#Predict the response for test dataset
y_pred = clf.predict(X_test)

dot_data = StringIO()
export_graphviz(clf, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True,feature_names = feature_cols,class_names=['0','1'])
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  
graph.write_png('{0}.png'.format(cSmell))
Image(graph.create_png())

""" labels = ['Class 0', 'Class 1']
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(conf_mat, cmap=plt.cm.Blues)
fig.colorbar(cax)
ax.set_xticklabels([''] + labels)
ax.set_yticklabels([''] + labels)
plt.xlabel('Predicted')
plt.ylabel('Expected')
plt.show()

dfCs["is_{0}".format(cSmell)].value_counts().plot(kind='bar', title='Count (target)')
 """
# Model Accuracy, how often is the classifier correct?
accuracy = metrics.accuracy_score(y_test, y_pred)
precision, recall, fmeasure, support = precision_recall_fscore_support(y_test, y_pred)

recall = metrics.recall_score(y_test, y_pred)
precision = metrics.precision_score(y_test, y_pred)
fmeasure = metrics.f1_score(y_test, y_pred)

conf_mat = confusion_matrix(y_true=y_test, y_pred=y_pred)
print('Confusion matrix:\n', conf_mat)

print("Precision: {} \nRecall: {}\nF-Measure: {}\n".format(precision, recall, fmeasure))

