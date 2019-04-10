from sklearn import svm
from sklearn import metrics
import numpy as np



def evaluate(model, X, y):
    prediction = model.predict(X)

    acc = metrics.accuracy_score(y, prediction)
    print("Accuracy:", acc)
    return prediction

def classify(featureset, trainsize):

    train_size = int(0.9 * len(featureset['Labels']))
    #train_X_to_ = np.array([(feature['feature']) for feature in featureset['Token Overlap'][:train_size]])
    #train_X_to = train_X_to_.reshape(-1, 1)

    train_X_we = np.array([[feature['feature_a'], feature['feature_b']]
                           for feature in featureset['Word Embeddings'][:train_size]], dtype=object)

    #train_X_we = [[feature['feature_a'], feature['feature_b']]
    #                       for feature in featureset['Word Embeddings'][:train_size]]

    for i in train_X_we:
        print(i)


    #print(train_X_we.shape)



    #print(a.shape)



    train_y_ = featureset['Labels'][:train_size]
    train_y = []
    for i in range(len(train_y_)):
        if train_y_[i] == [1,0]:
            if i % 2 == 0:
                train_y.append(0)
            else:
                train_y.append(1)
        else:
            train_y.append(0)


    #test_X_to_ = np.array([(feature['feature']) for feature in featureset['Token Overlap'][train_size:]])
    #test_X_to = test_X_to_.reshape(-1, 1)

    test_X_we = np.array([[feature['feature_a'], feature['feature_b']]
                           for feature in featureset['Word Embeddings'][train_size:]], dtype=object)

    test_y_ = featureset['Labels'][train_size:]
    test_y = []
    for i in test_y_:
        if i == [1, 0]:
            test_y.append(1)
        else:
            test_y.append(0)


    clf = svm.SVC(kernel='linear')
    clf.fit(train_X_we, train_y)

    evaluate(clf, test_X_we, test_y)