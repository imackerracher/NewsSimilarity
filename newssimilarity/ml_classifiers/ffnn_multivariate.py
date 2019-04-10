from keras.models import Sequential
from keras.layers import Dense
from newssimilarity.ml_classifiers.feature_selector import get_features
from keras.utils.np_utils import to_categorical
from newssimilarity.utils.ml_utils import extract_labels_single_format, evaluate
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold


def baseline_model():


    model = Sequential()
    model.add(Dense(8, input_dim=4, activation='relu'))
    #model.add(Dense(8, activation='relu'))
    model.add(Dense(3, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model


def classify(featureset, feature_selection, test_size):
    X_train, X_test, y_train, y_test = get_features(featureset, feature_selection, test_size)

    X_raw = X_train + X_test
    y = y_train + y_test

    def r(t):
        return [round(a, 1) for a in t]
    X_raw_2 = [r(n) for n in X_raw]
    X = numpy.array(X_raw_2).astype(float)

    transform = lambda l: 0 if l == [1, 0, 0] else (1 if l == [0, 1, 0] else 2)
    transform_y = list(map(transform, y))
    categorical_y = to_categorical(transform_y)
    seed = 7
    estimator = KerasClassifier(build_fn=baseline_model, epochs=200, batch_size=5, verbose=0)
    kfold = KFold(n_splits=10, shuffle=True, random_state=seed)
    results = cross_val_score(estimator, X, categorical_y, cv=kfold)
    print("Baseline: %.2f%% (%.2f%%)" % (results.mean() * 100, results.std() * 100))