"""from newssimilarity.utils.parsing.jsonparser import JsonParser
from newssimilarity.utils.scoring.annotation_returner import AnnotationReturner
from newssimilarity.segment_sim.segment_similarity_controller import SegmentSimilarityController
from newssimilarity.utils.scoring.scorer import Scorer
from newssimilarity.utils.scoring.evaluator import Evaluator
from newssimilarity.utils.exportation.csv_exporter import CSVExporter"""

import numpy

#from newssimilarity.utils.parsing.csv_test_files_parser import parse

from newssimilarity.utils.predict_test_files import run as test_files_run

from newssimilarity.utils.classify_for_vand import predict as predict_for_vand

from newssimilarity.ml_classifiers.svm_meter import classify as svm_classify

from newssimilarity.utils.featurize_meter import run as get_meter_features

from newssimilarity.ml_classifiers.ffnn_biclass import classify
import random
import itertools
import os
import csv
import time
from newssimilarity.utils.featurize_meter import run
from keras import backend as K


from newssimilarity.ml_classifiers.ffnn_meter import classify as meter_classify

from newssimilarity.utils.parsing.csv_feature_parser import parse
from newssimilarity.utils.parsing.csv_meter_parser import parse as meter_parse
from newssimilarity.definitions import project_root, slash, processed_news_features_path,\
    processed_meter_corpus_path, saved_models_path, processed_test_files_path
from newssimilarity.utils.parsing.jsonparser_ml_features import JsonParserMLFeatures
from newssimilarity.ml_classifiers.old_feauture_preparer import old_get_features
import pickle
from newssimilarity.ml_classifiers.feature_selector import get_features

from keras.utils.np_utils import to_categorical

#from newssimilarity.ml_classifiers.svm import classify as svm_classify


from random import choices, choice
from keras.models import load_model

from newssimilarity.utils.save_model import save
from newssimilarity.utils.load_model import load

import pandas
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
import csv


"""def main():
    #Run everything and export the f-scores to a csv file
    jp = JsonParser()
    car_bomb_1 = jp.parse_topic('CarBomb_1')
    car_bomb_3 = jp.parse_topic('CarBomb_3')
    car_bomb_3 = [car_bomb_3[1], car_bomb_3[0]]
    navy_1 = jp.parse_topic('Navy_1')
    navy_2 = jp.parse_topic('Navy_2')
    navy_2 = [navy_2[1], navy_2[0]]
    navy_3 = jp.parse_topic('Navy_3')
    navy_3 = [navy_3[1], navy_3[0]]
    samsung_3 = jp.parse_topic('Samsung_3')
    samsung_4 = jp.parse_topic('Samsung_4')
    samsung_5 = jp.parse_topic('Samsung_5')
    samsung_6 = jp.parse_topic('Samsung_6')
    #topics = [car_bomb_1, car_bomb_3, navy_1, navy_2, navy_3, samsung_3, samsung_4, samsung_5, samsung_6]
    topics = [car_bomb_1]

    segsimcon = SegmentSimilarityController(topics)
    sim_list = segsimcon.process()
    scorer = Scorer(sim_list)
    score_list = scorer.score()
    annotations_list = AnnotationReturner(topics).pair()
    et = Evaluator(annotations_list, score_list)
    f_measure_list = et.evaluate()
    csv_exporter = CSVExporter().export(f_measure_list, 'f_measure_test.csv')

def svm_test(featureset):
    svm_classify(featureset)

def log_test(featureset):
    log_classify(featureset)


def ffnn_test(featureset):
    ffnn_classify(featureset)"""





def count(x):
    c_out = {'0':0, '1':0}
    for i in x:
        if i==0:
            c_out['0'] += 1
        else:
            c_out['1'] += 1
    print(c_out)



def iterate_all_feature_selections_and_files():

    feature_selection = [#'GST', 'GST syn', 'LCS', 'LCS syn', 'TO', 'TO syn', 'Sparse Vector',
                         # 'TFIDF': tfidf_X,
                         #'Word Embeddings', 'Word Lengths', 'Word Level Levenshtein',
                         #'WN Path Matrix', 'WN LCH Matrix', 'WN WUP Matrix',
                         #'NE Coupling', 'NE Coupling syn',

                         'NE GT',
                         'NE GT syn', 'NE LCS', 'NE LCS syn', 'NE Overlap', 'NE Overlap syn', 'LCSubstring',
                         'Sentence Lengths', 'String Matching', 'Punctuation Overlap']


    best_feautures = ['Sparse Vector', 'Word Level Levenshtein', 'TO', 'GST', 'NE LCS']
    best_features_all_combinations = []
    for i in range(2, 5):
        for c in itertools.combinations(best_feautures, i):
            best_features_all_combinations.append(c)

    feature_files = os.listdir(slash.join(processed_news_features_path))

    #nums = [18, 94, 9, 78, 93, 76, 40, 59, 45, 49, 15, 54, 85, 25]
    nums = [9, 15, 18, 49, 78, 94]
    best_files = [(feature_files[i], i) for i in nums]

    with open(slash.join(saved_models_path + ['multiple_features_scores_file.csv']), 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        # add featureselection
        #header = ['modelnum', 'usedcorpora', 'corpussize', 'loss', 'accuracy',
        #          'loss on meter', 'accuracy on meter', 'featureselection']
        header = ['modelnum', 'mscoco', 'msrp', 'msrp-a', 'opinosis', 'p4p', 'quora',
                  'balanced', 'corpussize', 'loss', 'accuracy', 'loss on meter', 'accuracy on meter',
                  'Sparse Vector', 'Word Level Levenshtein', 'TO', 'GST', 'NE LCS']

        writer.writerow(header)
        modelnum = 0
        for feature_combination in best_features_all_combinations:
            for feature_file_name in best_files:
                start = time.time()
                new_model_row = [0 for _ in list(range(len(header)))]
                #new_model_row[0] = modelnum
                new_model_row[0] = feature_file_name[1]
                #usedcorpora = feature_file_name[0][:-4].split('_')
                usedcorpora = feature_file_name[0][:-4].split('_')
                new_model_row[1] = 1 if 'mscoco' in usedcorpora else 0
                new_model_row[2] = 1 if 'msrp' in usedcorpora else 0
                new_model_row[3] = 1 if 'msrpa' in usedcorpora else 0
                new_model_row[4] = 1 if 'opinosis' in usedcorpora else 0
                new_model_row[5] = 1 if 'p4p' in usedcorpora else 0
                new_model_row[6] = 1 if 'quora' in usedcorpora else 0
                new_model_row[7] = 1 if usedcorpora[0] == 'balance' else 0
                new_model_row[8] = int(usedcorpora[-1]) # corpussize
                model, score = classify(feature_selection, 0.1, feature_file_name[0])
                #model, score = classify(feature_selection, 0.1, feature_file_name)
                loss, accuracy = score

                # meterstuff
                X_train, X_test, y_train, y_test = get_meter_features(model, 0.1, feature_selection)
                loss_on_meter, accuracy_on_meter = meter_classify(X_train, X_test, y_train, y_test)

                new_model_row[9] = loss
                new_model_row[10] = accuracy
                new_model_row[11] = loss_on_meter
                new_model_row[12] = accuracy_on_meter
                new_model_row[13] = 1 if 'Sparse Vector' in feature_combination else 0
                new_model_row[14] = 1 if 'Word Level Levenshtein' in feature_combination else 0
                new_model_row[15] = 1 if 'TO' in feature_combination else 0
                new_model_row[16] = 1 if 'GST' in feature_combination else 0
                new_model_row[17] = 1 if 'NE LCS' in feature_combination else 0

                writer.writerow(new_model_row)

                print(modelnum, 'done in', time.time() - start)
                K.clear_session()
                modelnum += 1

        """for feature_file_name in feature_files:
            start = time.time()
            model, score = classify(feature_selection, 0.1, feature_file_name)
            #save(model, str(modelnum))
            t = feature_file_name[:-4].split('_')
            usedcorpora = '_'.join(t[:-1])
            corpussize = t[-1]
            loss, accuracy = score
            featureselection = '_'.join(feature_selection)

            #meterstuff
            X_train, X_test, y_train, y_test = get_meter_features(model, 0.1, feature_selection)
            loss_on_meter, accuracy_on_meter = meter_classify(X_train, X_test, y_train, y_test)

            #accuracy_on_meter = meter_classify(model, feature_selection, 0.1)
            new_model_row = [modelnum, usedcorpora, corpussize, loss, accuracy,
                             loss_on_meter, accuracy_on_meter] #, featureselection]
            writer.writerow(new_model_row)
            print(modelnum, 'done in', time.time()-start)
            modelnum += 1
            #break"""


"""def svm_stuff():
    f = ['Sparse Vector', 'Word Level Levenshtein', 'TO', 'GST']
    model = load('100')

    X_train, X_test, y_train, y_test = get_meter_features(model, 0.1, f, 2)
    print(numpy.shape(X_train))
    for i in [10, 20, 30, 40, 50, 60, 70]:
        print(i)
        svm_classify(X_train, X_test, y_train, y_test, i)
        print(count(y_train))
        print(count(y_test))"""

def feature_selection():
    f2 = [ 'GST', 'GST syn', 'LCS', 'LCS syn', 'TO', 'TO syn', 'Sparse Vector',
        # 'TFIDF': tfidf_X,
        'Word Embeddings', 'Word Lengths', 'Word Level Levenshtein',
        # 'WN Path Matrix', 'WN LCH Matrix', 'WN WUP Matrix',
        'NE Coupling', 'NE Coupling syn',
        'NE GT',
        'NE GT syn', 'NE LCS', 'NE LCS syn', 'NE Overlap', 'NE Overlap syn', 'LCSubstring',
        'Sentence Lengths', 'String Matching', 'Punctuation Overlap']

    feature_files = os.listdir(slash.join(processed_news_features_path))


    f = ['Sparse Vector', 'Word Level Levenshtein', 'TO', 'GST']
    #must be changed in method to return this
    X, y = classify(f2, 0.1, feature_files[0])
    nan_indeces = numpy.isnan(X)
    X[nan_indeces] = 0
    print(numpy.isnan(numpy.min(X)))
    model = LogisticRegression()
    rfe = RFE(model, 1)
    fit = rfe.fit(X, y)

    features = fit.support_
    ranking = fit.ranking_
    indices = [f2[i] for i, x in enumerate(features) if x]
    print(indices)
    t = []
    #print(ranking)
    features_ranked = []
    for i, num in enumerate(ranking):
        features_ranked.append((num, f2[i]))

    features_ranked_sorted = sorted(features_ranked, key=lambda x: x[0])
    print(features_ranked_sorted[:11])

def select_best_corpora():
    f_selection = ['GST', 'GST syn', 'LCS', 'LCS syn', 'TO', 'TO syn',
         'Sparse Vector', 'Word Lengths', 'Word Level Levenshtein',
         'NE Coupling', 'NE LCS syn']

    feature_files = os.listdir(slash.join(processed_news_features_path))


    with open(slash.join(saved_models_path + ['select_best_corpora_scores_file.csv']), 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        # add featureselection
        #header = ['modelnum', 'usedcorpora', 'corpussize', 'loss', 'accuracy',
        #          'loss on meter', 'accuracy on meter', 'featureselection']
        header = ['filename', 'mscoco', 'msrp', 'msrp-a', 'opinosis', 'p4p', 'quora',
                  'balanced', 'corpussize', 'loss', 'accuracy', 'loss on meter', 'accuracy on meter']

        writer.writerow(header)

        modelnum = 0
        for f_name in feature_files:
            start = time.time()
            model, score, rounded, y = classify(f_selection, 0.1, f_name)
            loss, accuracy = score
            X_train, X_test, y_train, y_test = get_meter_features(model, 0.1, f_selection, None)
            loss_on_meter, accuracy_on_meter = meter_classify(X_train, X_test, y_train, y_test)


            new_model_row = [0 for _ in list(range(len(header)))]
            # new_model_row[0] = modelnum
            new_model_row[0] = f_name
            # usedcorpora = feature_file_name[0][:-4].split('_')
            usedcorpora = f_name[:-4].split('_')
            new_model_row[1] = 1 if 'mscoco' in usedcorpora else 0
            new_model_row[2] = 1 if 'msrp' in usedcorpora else 0
            new_model_row[3] = 1 if 'msrpa' in usedcorpora else 0
            new_model_row[4] = 1 if 'opinosis' in usedcorpora else 0
            new_model_row[5] = 1 if 'p4p' in usedcorpora else 0
            new_model_row[6] = 1 if 'quora' in usedcorpora else 0
            new_model_row[7] = 1 if usedcorpora[0] == 'balance' else 0
            new_model_row[8] = int(usedcorpora[-1])  # corpussize
            new_model_row[9] = loss
            new_model_row[10] = accuracy
            new_model_row[11] = loss_on_meter
            new_model_row[12] = accuracy_on_meter

            writer.writerow(new_model_row)

            print(modelnum, 'done in', time.time() - start)
            K.clear_session()
            modelnum += 1

def test_5_features():
    feature_files = os.listdir(slash.join(processed_news_features_path))
    best_corpus = feature_files[75]

    f_selections = ['GST', 'GST syn', 'LCS', 'LCS syn', 'TO', 'TO syn',
                    'Sparse Vector', 'Word Lengths', 'Word Level Levenshtein',
                    'NE Coupling', 'NE LCS syn']

    a = []
    for c in itertools.combinations(f_selections, 5):
        a.append(c)

    print(len(a))

def test_different_feature_selections():
    """f_selections = ['GST', 'GST syn', 'LCS', 'LCS syn', 'TO', 'TO syn',
                    'Sparse Vector', 'Word Lengths', 'Word Level Levenshtein',
                    'NE Coupling', 'NE LCS syn']"""

    f_selections = ['GST syn', 'LCS syn', 'TO syn', 'GST', 'TO', 'LCS',
                    'LCSubstring', 'Word Lengths', 'Word Level Levenshtein',
                    'String Matching', 'NE Coupling']

    feature_files = os.listdir(slash.join(processed_news_features_path))
    best_c_indeces = [75, 4, 61, 33, 104]
    best_corpora = [(feature_files[i], i) for i in best_c_indeces]


    with open(slash.join(saved_models_path + ['test_different_features_scores_file_new.csv']), 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        # add featureselection

        header = ['corpusnum', 'loss', 'accuracy', 'loss on meter', 'accuracy on meter',
                  'GST syn', 'LCS syn', 'TO syn', 'GST', 'TO', 'LCS',
                    'LCSubstring', 'Word Lengths', 'Word Level Levenshtein',
                    'String Matching', 'NE Coupling']

        writer.writerow(header)
        modelnum = 0
        for c_name in best_corpora:
            f_name = c_name[0]
            num = c_name[1]
            for i in range(5, 12):
                new_model_row = [0 for _ in list(range(len(header)))]
                f = f_selections[:i]
                start = time.time()
                model, score, rounded, y = classify(f, 0.1, f_name)
                loss, accuracy = score
                X_train, X_test, y_train, y_test = get_meter_features(model, 0.1, f, None)
                loss_on_meter, accuracy_on_meter = meter_classify(X_train, X_test, y_train, y_test)

                new_model_row[0] = num
                new_model_row[1] = loss
                new_model_row[2] = accuracy
                new_model_row[3] = loss_on_meter
                new_model_row[4] = accuracy_on_meter
                new_model_row[5] = 1 if 'GST syn' in f else 0
                new_model_row[6] = 1 if 'LCS syn' in f else 0
                new_model_row[7] = 1 if 'TO syn' in f else 0
                new_model_row[8] = 1 if 'GST' in f else 0
                new_model_row[9] = 1 if 'TO' in f else 0
                new_model_row[10] = 1 if 'LCS' in f else 0
                new_model_row[11] = 1 if 'LCSSubstring' in f else 0
                new_model_row[12] = 1 if 'Word Lenghts' in f else 0
                new_model_row[13] = 1 if 'Word Level Levenshtein' in f else 0
                new_model_row[14] = 1 if 'String Matching' in f else 0
                new_model_row[15] = 1 if 'NE Coupling' in f else 0

                writer.writerow(new_model_row)

                print(modelnum, 'done in', time.time() - start)
                K.clear_session()
                modelnum += 1
                if modelnum == 3:
                    break



def handle_test_files():
    f1 = 'bbc_cnn.csv'
    f2 = 'bbc_reuters.csv'
    f3 = 'bbc_wp.csv'
    f4 = 'cnn_wp.csv'
    f5 = 'cnn_reuters.csv'
    f6 = 'reuters_wp.csv'

    file_names = [f1, f2, f3, f4, f5, f6]
    predict_for_vand(file_names)
    #predict_for_vand(f1)"""

    """source, target, features = parse(f1)

    primary_model = load('best_sentence_level_model')
    secondary_model = load('best_article_level_model')
    test_files_run(primary_model, secondary_model, features)"""


if __name__ == '__main__':
    random.seed(7)

    """f = ['GST syn', 'LCS syn', 'TO syn', 'GST', 'TO', 'LCS']
    feature_files = os.listdir(slash.join(processed_news_features_path))
    #test_different_feature_selections()
    model, score, rounded, y = classify(f, 0.1, feature_files[4])
    save(model, 'best_sentence_level_model')
    loss, accuracy = score
    X_train, X_test, y_train, y_test = get_meter_features(model, 0.1, f, None)
    score_meter, model_meter = meter_classify(X_train, X_test, y_train, y_test)
    loss_on_meter, accuracy_on_meter = score_meter
    save(model_meter, 'best_article_level_model')"""

    #model = load('best_article_level_model')

    #feature_files = os.listdir(slash.join(processed_news_features_path))

    #test_file = feature_files[75]


    #feature_selection()

    f = ['GST', 'GST syn', 'LCS', 'LCS syn', 'TO syn']

    """'TO', 'TO syn',
         'Sparse Vector', 'Word Lengths', 'Word Level Levenshtein',
         'NE Coupling', 'NE LCS syn']#, 'NE Overlap', 'NE Overlap syn']"""


    """model, score, rounded, y = classify(f, 0.1, test_file)
    X_train, X_test, y_train, y_test = get_meter_features(model, 0.1, f, None)
    loss_on_meter, accuracy_on_meter = meter_classify(X_train, X_test, y_train, y_test)
    loss, accuracy = score
    print('acc meter', accuracy_on_meter)
    print('loss meter', loss_on_meter)
    print('loss', loss)
    print('accuracy', accuracy)
    print(rounded)
    print(y)"""
    """
    header = ['corpusnum', 'loss', 'accuracy', 'loss on meter', 'accuracy on meter',
              'GST', 'GST syn', 'LCS', 'LCS syn', 'TO', 'TO syn', 'Sparse Vector', 'Word Lengths',
              'Word Level Levenshtein', 'NE Coupling', 'NE LCS syn']


    #test_different_feature_selections()
    #select_best_corpora()
    feature_files = os.listdir(slash.join(processed_news_features_path))
    for f_name in feature_files:
        usedcorpora = f_name[:-4].split('_')
        print(usedcorpora)"""






    #print(test_file)

    #f = ['TO']
    """f = ['Sparse Vector', 'Word Level Levenshtein', 'TO', 'GST']#, 'NE LCS']




    model = load('100')

    #X_train, X_test, y_train, y_test = get_meter_features(model, 0.1, f)

    #print(numpy.shape(X_train))

    def ev(y, r):
        s = {'TP': 0, 'FP': 0, 'TN': 0, 'FN': 0}
        for i in range(len(y)):
            actual = int(y[i])
            predicted = int(r[i])
            if actual == 1 and predicted == 1:
                s['TP'] += 1
            elif actual == 0 and predicted == 1:
                s['FP'] += 1
            elif actual == 0 and predicted == 0:
                s['TN'] += 1
            else:
                s['FN'] += 1
        a = (s['TP'] + s['TN'])/(s['TP'] + s['TN'] + s['FP'] + s['FN'])
        return s, a



    X_train, X_test, y_train, y_test = get_meter_features(model, 0.1, f, None)"""



    """print(numpy.shape(X_train))
    for _ in range(5):
        for cutoff in [0.55]:
            #X_train, X_test, y_train, y_test = get_meter_features(model, 0.1, f)
            score, y_test, predictions, rounded, c1, c2 = meter_classify(X_train, X_test, y_train, y_test, cutoff)
            loss_on_meter, accuracy_on_meter = score

            print('ACCURACY', accuracy_on_meter)
            print('CUTOFF', cutoff)
            print('Loss', loss_on_meter)
            e, a = ev(y_test, rounded)
            print(e)
            print('ACCURACY WITH CUTOFF', a)

            dif_ratio = c1['1']/c1['0'] - c2['1']/c2['0']
            print('dif ratio:', dif_ratio)
            print(c1, 'ratio:', c1['1']/c1['0'])
            print(c2, 'ratio:', c2['1']/c2['0'])
    #print('\n'*10)"""


    handle_test_files()








