"""
Test purposes
"""

import numpy as np
from scipy import spatial
from sklearn.model_selection import train_test_split
import math


def reshape_single_dimension(X):
    reshaped = np.array(X).reshape(-1, 1)
    return reshaped

def we_simple_sum(word_embeddings):
    """

    :param word_embeddings:
    :return:
    """
    #sums = lambda vecs: abs(sum(vecs[0]) - sum(vecs[1]))
    sums = lambda vecs: abs(sum([sum(wv) for wv in vecs[0]]) - sum([sum(wv) for wv in vecs[1]]))
    return list(map(sums, word_embeddings))
    """for i in word_embeddings:
        print(sum([sum(a) for a in i[0]]))
        print([sum(a) for a in i[1]])
        print()"""

def cosine_distance(vector_list):
    """"#make sure both vectors have a dimension (i.e. are not only zeros)
    def good_vecs_format(vecs):
        if len(set(vecs[0])) > 1  and len(set(vecs[0])) > 1:
            return True
        else:
            return False
    cos = lambda vecs: 1-spatial.distance.cosine(vecs[0], vecs[1]) if good_vecs_format(vecs) else 1.0
    x = list(map(cos, vector_list))"""
    features = []
    for i in vector_list:
        if len(set(i[0])) > 1 and len(set(i[1])) > 1:
            s = 1-spatial.distance.cosine(i[0], i[1])
            """print(s)
            if math.isnan(s):
                print(set(i[0]))
                print(set(i[1]))
                print()"""
        else:
            s = 1.0
        features.append(s)
    return features

def transform_labels(labels):
    l = lambda label: 1 if label == [1,0] else 0
    return list(map(l, labels))





def old_get_features(featureset, feature_selection, test_size):

    selected_features = []
    for f_name in feature_selection:
        if f_name == 'Token Overlap':
            selected_features.append([f['feature'] for f in featureset[f_name]])
        elif f_name == 'Word Embeddings':
            word_embeddings = [(f['feature_a'], f['feature_b']) for f in featureset[f_name]]
            processed = we_simple_sum(word_embeddings)
            selected_features.append(processed)
        elif f_name == 'Sparse Vector':
            sparse_vectors = [(f['feature_a'], f['feature_b']) for f in featureset[f_name]]
            selected_features.append(cosine_distance(sparse_vectors))
        elif f_name in ['GST', 'GST syn', 'LCS', 'LCS syn', 'TO', 'TO syn', 'Word Level Levenshtein', 'NE Coupling',
         'NE Overlap syn', 'Punctuation Overlap', 'Word Lengths']:
            selected_features.append([f['feature'] for f in featureset[f_name]])


    #unknown number of lists
    X = list(zip(*selected_features))
    y = transform_labels(featureset['Labels'])

    #for i in X:
    #    print(i)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, shuffle=True)
    return X_train, X_test, y_train, y_test