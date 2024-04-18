import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import ast
warnings.filterwarnings('ignore')
from gen_dataset import d, d2

from sklearn.model_selection import train_test_split

X = pd.concat([d, d2])['data'].apply(ast.literal_eval)
X2 = np.array([np.array(x) for x in X])
X2 = np.vstack(X2)
y = pd.concat([d, d2])['State']


X_train, X_test, y_train, y_test = train_test_split(X2, y, train_size=0.7, random_state=0)

from sklearn import tree
clf = tree.DecisionTreeClassifier()
clf.fit(X_train, y_train)


from sklearn.metrics import accuracy_score

# Visualize the tree after training
plt.figure(figsize=(10,8)) 
tree.plot_tree(clf, class_names=['1', '0'], filled=True)
plt.show()

# Predict Accuracy Score on test dataset
y_pred = clf.predict(X_test)

print("Train data accuracy:",round(100*accuracy_score(y_true = y_train, y_pred=clf.predict(X_train)),3),"%")
print("Test data accuracy:","%.3f" %(100*accuracy_score(y_true = y_test, y_pred=y_pred)),"%")