from newssimilarity.utils.load_model import load
from newssimilarity.utils.parsing.csv_meter_parser import parse
from newssimilarity.ml_classifiers.feature_selector import get_features
from newssimilarity.definitions import slash, processed_meter_corpus_path
from sklearn.model_selection import train_test_split
import numpy as np
import os




def featurize_primary(feature_selection, features, model):



    key = list(features.keys())[0]
    f_length = len(features[key])
    dummy_y = [2 for _ in list(range(f_length))]
    X,_,_,_ = get_features(features, dummy_y, feature_selection, 0)
    #print(np.shape(X))


    predictions = model.predict(X)
    #rounded = [int(round(x[0])) for x in predictions]
    target_source_prediction = list(zip(features['target_id'], features['source_id'], predictions.tolist()))

    num_target_sentences = int(target_source_prediction[-1][0])
    num_source_sentences = int(target_source_prediction[-1][1])



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
    #return np.array(scores_padded)[:55]
    return scores_padded



def run(primary_model, secondary_model, features):#, feature_selection):

    feature_selection = ['GST syn', 'LCS syn', 'TO syn', 'GST', 'TO', 'LCS']
    scores = []
    score = featurize_primary(feature_selection, features, primary_model)
    #print(score)
    #return score
    scores.append(score)

    f_size = 55

    X = np.array([np.array(i) for i in scores])
    new_X = np.array([x[:f_size] for x in X])
    p = secondary_model.predict(new_X)

    return p

    #X = np.array([np.array(i) for i in scores])

    #return score

