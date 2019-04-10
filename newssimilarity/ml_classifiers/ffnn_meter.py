from keras.models import Sequential
from keras.layers import Dense
from newssimilarity.utils.featurize_meter import run as get_meter_features
import math
import numpy as np

def count(y):
    c = {'0':0, '1':0}
    for i in y:
        if i == 0:
            c['0'] += 1
        else:
            c['1'] += 1
    return c



def classify2(X_train, X_test, y_train, y_test, cutoff):

    #X_train, X_test, y_train, y_test = get_meter_features(primary_model, test_size, feature_selection)

    num_epochs = math.floor(len(X_train) / 10)

    print(np.shape(X_train))

    model = Sequential()
    model.add(Dense(100, input_dim=100, init='uniform', activation='relu'))
    model.add(Dense(80, init='uniform', activation='relu'))
    model.add(Dense(50, init='uniform', activation='relu'))
    model.add(Dense(30, init='uniform', activation='relu'))
    model.add(Dense(50, init='uniform', activation='relu'))
    model.add(Dense(20, init='uniform', activation='relu'))
    model.add(Dense(8, init='uniform', activation='relu'))
    model.add(Dense(1, init='uniform', activation='sigmoid'))
    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # Fit the model
    model.fit(X_train, y_train, epochs=num_epochs, batch_size=10, verbose=0)

    score = model.evaluate(X_test, y_test)
    predictions = model.predict(X_test)
    # round predictions
    #rounded = [int(round(x[0])) for x in predictions]
    def r(i):
        if i >cutoff:
            return 1
        else:
            return 0
    rounded = [r(x[0]) for x in predictions]

    return score, y_test, predictions, rounded, count(y_train), count(y_test)


def classify(X_train, X_test, y_train, y_test):

    #X_train, X_test, y_train, y_test = get_meter_features(primary_model, test_size, feature_selection)

    f_size = 55
    new_X_train = np.array([x[:f_size] for x in X_train])
    new_X_test = np.array([x[:f_size] for x in X_test])

    num_epochs = math.floor(len(new_X_train) / 10)

    print('NUM EPOCHS',
          num_epochs)


    model = Sequential()
    """model.add(Dense(50, input_dim=50, init='uniform', activation='relu'))
    model.add(Dense(35, init='uniform', activation='relu'))
    model.add(Dense(25, init='uniform', activation='relu'))
    model.add(Dense(20, init='uniform', activation='relu'))
    model.add(Dense(8, init='uniform', activation='relu'))
    model.add(Dense(1, init='uniform', activation='sigmoid'))"""
    model.add(Dense(f_size, input_dim=f_size, init='uniform', activation='relu'))
    model.add(Dense(50, init='uniform', activation='relu'))
    #model.add(Dense(40, init='uniform', activation='relu'))
    model.add(Dense(20, init='uniform', activation='relu'))
    #model.add(Dense(15, init='uniform', activation='relu'))
    #model.add(Dense(10, init='uniform', activation='relu'))
    model.add(Dense(8, init='uniform', activation='relu'))
    model.add(Dense(1, init='uniform', activation='sigmoid'))

    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # Fit the model
    model.fit(new_X_train, y_train, epochs=num_epochs, batch_size=10, verbose=0)

    score = model.evaluate(new_X_test, y_test)
    predictions = model.predict(new_X_test)
    # round predictions
    #rounded = [int(round(x[0])) for x in predictions]
    """def r(i):
        if i >cutoff:
            return 1
        else:
            return 0
    rounded = [r(x[0]) for x in predictions]"""

    return score, model #, y_test, predictions, rounded, count(y_train), count(y_test)


