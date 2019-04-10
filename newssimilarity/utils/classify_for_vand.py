import os
import numpy as np
from newssimilarity.utils.load_model import load
#from newssimilarity.utils.parsing.csv_test_files_parser import parse
from newssimilarity.utils.parsing.csv_feature_parser import parse
from newssimilarity.utils.predict_test_files import run as test_files_run
from newssimilarity.utils.exportation.json_exporter import JsonExporter
from newssimilarity.definitions import project_root
"""
articles must be ordered chronologically
1-article
2-article
"""


def predict(article_file_names):

    #always the same
    feature_selection = ['GST syn', 'LCS syn', 'TO syn', 'GST', 'TO', 'LCS']


    primary_model = load('best_sentence_level_model')
    secondary_model = load('best_article_level_model')

    scores = []

    #print(article_file_names[0])
    #source, target, features = parse(article_file_names[0])
    #test_files_run(primary_model, secondary_model, features)

    sources = []
    targets = []
    outlets = []
    for file_name in article_file_names:
        #parse(file_name)
        source, target, features = parse(file_name)
        sources.append(source)
        targets.append(target)
        outlets.append(source)
        outlets.append(target)
        score = test_files_run(primary_model, secondary_model, features)#, feature_selection)
        scores.append((source, target, score[0][0]))


    outlets = list(set(outlets))

    nums = []
    for i in range(len(outlets)):
        for j in range(i+1, len(outlets)):
            nums.append((i, j))


    """used = []
    for i in sources:
        for j in targets:
            if i != j and (j, i) not in used:
                used.append((i, j))
                print(i, j)"""

    scores_for_json = {}
    for i, score in enumerate(scores):
        source, target, p = score
        scores_for_json['_'.join([source, target])] = \
            {'source': nums[i][0], 'target': nums[i][1], 'value': round(float(p), 2)}
        print(source, target, p)

    JsonExporter(scores_for_json).export()


    """f_size = 55

    X = np.array([np.array(i) for i in scores])
    new_X = np.array([x[:f_size] for x in X])
    p = secondary_model.predict(new_X)

    print(p)"""