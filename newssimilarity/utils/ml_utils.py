from sklearn import metrics






def evaluate(model, X, y):
    prediction = model.predict(X)

    acc = metrics.accuracy_score(y, prediction)
    print("Accuracy:", acc)
    return prediction

def extract_labels_single_format(featureset):
    """
    [0,1,1,1,0,0...] instead of [[1,0], [1,0], [0,1]...]
    :param featureset:
    :return:
    """
    def extract(label): return 1 if label == [1,0] else 0
    y = lambda label: extract(label), featureset['Labels']
    return y