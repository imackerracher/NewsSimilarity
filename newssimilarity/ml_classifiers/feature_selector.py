import numpy as np
from scipy import spatial
from sklearn.model_selection import train_test_split



def reshape_single_dimension(X):
    reshaped = np.array(X).reshape(-1, 1)
    return reshaped



"""def transform_labels(labels):
    l = lambda label: 1 if label == [1,0] else 0
    return list(map(l, labels))"""


def get_features(featureset, y, feature_selection, test_size):
    selected_features = []
    for f_name in feature_selection:
        selected_features.append(featureset[f_name])

    #for i in selected_features:
    #    print(len(i))

    #unknown number of lists
    X = list(zip(*selected_features))
    #print(X)
    X = np.array([np.array(i) for i in X])

    #print(np.shape(X))

    #y = np.array(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, shuffle=True)
    return X_train, X_test, y_train, y_test
