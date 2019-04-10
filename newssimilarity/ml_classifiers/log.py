from sklearn import linear_model
from newssimilarity.ml_classifiers.feature_selector import get_features
from newssimilarity.utils.ml_utils import extract_labels_single_format, evaluate





def classify(featureset, feature_selection, test_size):
    """

    :param featureset: The entire set of features
    :param feature_selection: A list indicating the features to be used.
    E.g. ['Token Overlap', 'Word Embeddings']
    :param Size of the test set (e.g. 0.2)
    :return:
    """
    X_train, X_test, y_train, y_test =get_features(featureset, feature_selection, test_size)


    logreg = linear_model.LogisticRegression(C=1e5)
    logreg.fit(X_train, y_train)

    evaluate(logreg, X_test, y_test)


