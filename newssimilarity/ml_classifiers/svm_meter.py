from sklearn import svm
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC

def classify(X_train, X_test, y_train, y_test, f_size):
    clf = svm.SVC(kernel='linear', C=1.0)

    #f_size = 30
    new_X_train = np.array([x[:f_size] for x in X_train])
    new_X_test = np.array([x[:f_size] for x in X_test])

    clf.fit(new_X_train, y_train)

    predictions = clf.predict(new_X_test)
    accuracy = 0
    for i in range(len(y_test)):
        if y_test[i] == predictions[i]:
            accuracy += 1
    print(accuracy/len(y_test))
    print(predictions)

    # Set the parameters by cross-validation
    """tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                         'C': [1, 10, 100, 1000]},
                        {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]

    scores = ['precision', 'recall']

    for score in scores:
        print("# Tuning hyper-parameters for %s" % score)
        print()

        clf = GridSearchCV(SVC(), tuned_parameters, cv=5,
                           scoring='%s_macro' % score)
        clf.fit(new_X_train, y_train)

        print("Best parameters set found on development set:")
        print()
        print(clf.best_params_)
        print()
        print("Grid scores on development set:")
        print()
        means = clf.cv_results_['mean_test_score']
        stds = clf.cv_results_['std_test_score']
        for mean, std, params in zip(means, stds, clf.cv_results_['params']):
            print("%0.3f (+/-%0.03f) for %r"
                  % (mean, std * 2, params))
        print()

        print("Detailed classification report:")
        print()
        print("The model is trained on the full development set.")
        print("The scores are computed on the full evaluation set.")
        print()
        y_true, y_pred = y_test, clf.predict(new_X_test)
        print(classification_report(y_true, y_pred))
        print()"""