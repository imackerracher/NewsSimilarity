from keras.models import Sequential
from keras.layers import Dense
from newssimilarity.utils.parsing.csv_feature_parser import parse
from newssimilarity.ml_classifiers.feature_selector import get_features
from newssimilarity.definitions import project_root
from newssimilarity.utils.ml_utils import extract_labels_single_format, evaluate
import pickle
import numpy as np
import math
from keras import regularizers
from keras import optimizers


"""def classify(featureset, feature_selection, test_size):
    X_train, X_test, y_train, y_test = get_features(featureset, feature_selection, test_size)
    

    print(X_train)

    model = Sequential()
    model.add(Dense(11, input_dim=11, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    model.fit(X_train, y_train, epochs=100, batch_size=int(len(X_train)/100))

    scores = model.evaluate(X_test, y_test)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

    return model"""


"""def classify(featureset, feature_selection, test_size):
    X_train, X_test, y_train, y_test = get_features(featureset, feature_selection, test_size)

    #print(len(X_train))
    model = Sequential()
    model.add(Dense(11, input_dim=11, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    model.fit(X_train, y_train, epochs=100, batch_size=int(len(X_train) / 100))

    scores = model.evaluate(X_test, y_test)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

    return model"""


def test(X,Y):
    model = Sequential()
    model.add(Dense(12, input_dim=12, init='uniform', activation='relu'))
    model.add(Dense(8, init='uniform', activation='relu'))
    model.add(Dense(1, init='uniform', activation='sigmoid'))
    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # Fit the model
    model.fit(X, Y, epochs=150, batch_size=10, verbose=2)
    # calculate predictions
    predictions = model.predict(X)
    # round predictions
    rounded = [round(x[0]) for x in predictions]
    print(rounded)

    return model



"""def classify(feature_selection, test_size, feature_file_name):

    features, labels = parse(feature_file_name)
    X_train, X_test, y_train, y_test = get_features(features, labels, feature_selection, test_size)

    num_features = len(feature_selection)
    num_epochs = math.floor(len(X_train)/20)

    reg_pen = 0.01

    model = Sequential()
    model.add(Dense(num_features, input_dim=num_features, init='uniform', activation='relu', kernel_regularizer=regularizers.l2(reg_pen)))
    model.add(Dense(10, init='uniform', activation='relu', kernel_regularizer=regularizers.l2(reg_pen)))
    model.add(Dense(8, init='uniform', activation='relu', kernel_regularizer=regularizers.l2(reg_pen)))
    model.add(Dense(5, init='uniform', activation='relu', kernel_regularizer=regularizers.l2(reg_pen)))
    model.add(Dense(1, init='uniform', activation='sigmoid'))
    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # Fit the model
    model.fit(X_train, y_train, epochs=num_epochs, batch_size=20, verbose=0)

    #loss and accuracy
    score = model.evaluate(X_test, y_test)
    predictions = model.predict(X_train)
    rounded = [round(x[0]) for x in predictions]
    #print(score)
    return model, score, rounded"""


def count(y):
    c = {'0':0, '1':0}
    for i in y:
        if i == 0:
            c['0'] += 1
        else:
            c['1'] += 1
    return c

def classify(feature_selection, test_size, feature_file_name):

    features, labels = parse(feature_file_name)
    #print(len(features['GST']))
    X_train, X_test, y_train, y_test = get_features(features, labels, feature_selection, test_size)
    #return X_train, y_train

    #print(X_train)
    #print(np.shape(X_train))
    def replace_nan(X):
        nan_indeces = np.isnan(X)
        X[nan_indeces] = 0
        return X

    #print(np.shape(X_train))
    #print(np.shape(X_test))

    X_train = replace_nan(X_train)
    X_test = replace_nan(X_test)

    b_size = 200

    num_features = len(feature_selection)
    num_epochs = math.floor(len(X_train)/b_size)

    reg_pen = 0.01

    model = Sequential()
    model.add(Dense(num_features, input_dim=num_features, init='uniform', activation='relu'))
    #model.add(Dense(10, init='uniform', activation='relu'))
    #model.add(Dense(8, init='uniform', activation='relu'))
    #model.add(Dense(5, init='uniform', activation='relu'))
    model.add(Dense(3, init='uniform', activation='relu'))
    #model.add(Dense(2, init='uniform', activation='relu'))
    model.add(Dense(1, init='uniform', activation='sigmoid'))
    # Compile model
    sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='binary_crossentropy', optimizer=sgd, metrics=['accuracy'])
    # Fit the model
    model.fit(X_train, y_train, epochs=num_epochs, batch_size=b_size, verbose=0)

    #loss and accuracy
    score = model.evaluate(X_test, y_test)
    predictions = model.predict(X_train)
    rounded = [round(x[0]) for x in predictions]
    #print(score)
    return model, score, rounded, count(y_train)

