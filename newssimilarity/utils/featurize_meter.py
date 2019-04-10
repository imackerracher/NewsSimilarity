from newssimilarity.utils.load_model import load
from newssimilarity.utils.parsing.csv_meter_parser import parse
from newssimilarity.ml_classifiers.feature_selector import get_features
from newssimilarity.definitions import slash, processed_meter_corpus_path
from sklearn.model_selection import train_test_split
import numpy as np
import os




def featurize(feature_selection, file_name, model):

    #get meter file
    features, derived = parse(file_name)

    key = list(features.keys())[0]
    f_length = len(features[key])
    dummy_y = [2 for _ in list(range(f_length))]
    X,_,_,_ = get_features(features, dummy_y, feature_selection, 0)
    #print(np.shape(X))


    predictions = model.predict(X)
    #rounded = [int(round(x[0])) for x in predictions]
    target_source_prediction = list(zip(features['TARGET_ID'], features['SOURCE_ID'], predictions.tolist()))

    num_target_sentences = int(target_source_prediction[-1][0])
    num_source_sentences = int(target_source_prediction[-1][1])

    if num_source_sentences == 0 or num_target_sentences == 0:
        return None


    #find maximum score for each target sentence
    max_dict = {}
    used_source_ids = []
    for prediction in target_source_prediction:
        target_id, source_id, val = prediction
        source_id = int(source_id)
        target_id = int(target_id)
        val = val[0]
        used_source_ids.append(source_id)
        if target_id in max_dict:
            if val > max_dict[target_id][1]:
                max_dict[target_id] = [source_id, val]
        else:
            max_dict[target_id] = [source_id, val]

    scores = [max_dict[k][1] for k in max_dict]
    #include fraction of number of target and source sentences
    scores_padded = [num_target_sentences/num_source_sentences] + scores + [0 for _ in list(range(len(scores)+1, 100))]

    #x = np.array(scores_padded)
    return (scores_padded, derived)


def balance_up(X, y):
    balanced_X = []
    balanced_y = []
    num = 0
    for i in range(len(y)):
        if y[i] == 0:
            balanced_y.append(y[i])
            balanced_X.append(X[i])
        elif num < 400:
            balanced_y.append(y[i])
            balanced_X.append(X[i])
            num += 1
    return balanced_X, balanced_y

def balance_down(X, y):
    balanced_X = []
    balanced_y = []
    num = 0
    for i in range(len(y)):
        if y[i] == 0:
            balanced_y.append(y[i])
            balanced_X.append(X[i])

            balanced_y.append(y[i])
            balanced_X.append(X[i])

        else:
            balanced_y.append(y[i])
            balanced_X.append(X[i])
            num += 1
    return balanced_X, balanced_y

def balance_both(X, y):
    X_u, y_u = balance_up(X, y)
    X_b, y_b = balance_down(X_u, y_u)

    return X_b, y_b


def run(primary_model, test_size, feature_selection, b_mode):
    #model = load(model_name)

    file_names = os.listdir(slash.join(processed_meter_corpus_path))

    scores = []
    y = []
    for file_name in file_names:
        f = featurize(feature_selection, file_name, primary_model)
        if f is not None:
            score, label = f
            #print(score)
            scores.append(score)
            new_y = 0 if label == '0' else 1
            y.append(new_y)
            #y.append(int(label))
            #break


    #print(scores)


    X = np.array([np.array(i) for i in scores])

    if b_mode == 0:
        b_X, b_y = balance_both(X, y)
    elif b_mode == 1:
        b_X, b_y = balance_down(X, y)
    elif b_mode == 2:
        b_X, b_y = balance_up(X, y)
    else:
        b_X = X
        b_y = y


    X_train, X_test, y_train, y_test = train_test_split(b_X, b_y, test_size=test_size, shuffle=True)
    return X_train, X_test, y_train, y_test

