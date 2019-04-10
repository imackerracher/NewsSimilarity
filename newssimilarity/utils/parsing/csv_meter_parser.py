from newssimilarity.definitions import slash, processed_meter_corpus_path
import csv
import os



"""def parse(file_name):

    #file_name = os.listdir(slash.join(processed_meter_corpus_path))[0]
    file_path = slash.join(processed_meter_corpus_path + [file_name])

    feature_names = ['GST', 'GST syn', 'LCS', 'LCS syn', 'TO', 'TO syn', 'Sparse Vector',
                     # 'TFIDF': tfidf_X,
                     'Word Embeddings', 'Word Lengths', 'Word Level Levenshtein',
                     'WN Path Matrix', 'WN LCH Matrix', 'WN WUP Matrix',
                     'NE Coupling', 'NE Coupling syn', 'NE GT',
                     'NE GT syn', 'NE LCS', 'NE LCS syn', 'NE Overlap', 'NE Overlap syn', 'LCSubstring',
                     'Sentence Lengths', 'String Matching', 'Punctuation Overlap']

    features = {'GST': [], 'GST syn': [], 'LCS': [], 'LCS syn': [], 'TO': [],
                'TO syn': [], 'Sparse Vector': [],  # 'TFIDF': tfidf_X,
                'Word Embeddings': [], 'Word Lengths': [], 'Word Level Levenshtein': [],
                'WN Path Matrix': [], 'WN LCH Matrix': [], 'WN WUP Matrix': [],
                'NE Coupling': [], 'NE Coupling syn': [], 'NE GT': [], 'NE GT syn': [],
                'NE LCS': [], 'NE LCS syn': [], 'NE Overlap': [], 'NE Overlap syn': [],
                'LCSubstring': [], 'Sentence Lengths': [], 'String Matching': [], 'Punctuation Overlap': []}

    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            if len(line)>0 and line[0] != 'source':
                f = list(zip(feature_names, [float(n) for n in line[3:]]))
                #print(f)
                for label, val in f:
                    features[label].append(val)


    return features"""


def parse(file_name):

    #file_name = os.listdir(slash.join(processed_meter_corpus_path))[0]
    file_path = slash.join(processed_meter_corpus_path + [file_name])

    feature_names = ['TARGET_ID', 'SOURCE_ID',  'GST', 'GST syn', 'LCS', 'LCS syn', 'TO', 'TO syn', 'Sparse Vector',
                     # 'TFIDF': tfidf_X,
                     'Word Embeddings', 'Word Lengths', 'Word Level Levenshtein',
                     'WN Path Matrix', 'WN LCH Matrix', 'WN WUP Matrix',
                     'NE Coupling', 'NE Coupling syn', 'NE GT',
                     'NE GT syn', 'NE LCS', 'NE LCS syn', 'NE Overlap', 'NE Overlap syn', 'LCSubstring',
                     'Sentence Lengths', 'String Matching', 'Punctuation Overlap']

    features = {'TARGET_ID': [], 'SOURCE_ID': [],  'GST': [], 'GST syn': [], 'LCS': [], 'LCS syn': [], 'TO': [],
                'TO syn': [], 'Sparse Vector': [],  # 'TFIDF': tfidf_X,
                'Word Embeddings': [], 'Word Lengths': [], 'Word Level Levenshtein': [],
                'WN Path Matrix': [], 'WN LCH Matrix': [], 'WN WUP Matrix': [],
                'NE Coupling': [], 'NE Coupling syn': [], 'NE GT': [], 'NE GT syn': [],
                'NE LCS': [], 'NE LCS syn': [], 'NE Overlap': [], 'NE Overlap syn': [],
                'LCSubstring': [], 'Sentence Lengths': [], 'String Matching': [], 'Punctuation Overlap': []}

    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            if len(line)>0 and line[0] != 'source':
                derived = line[2]
                f = list(zip(feature_names, [float(n) for n in line[3:]]))
                #print(line[3], line[4])
                for label, val in f:
                    features[label].append(val)

    return features, derived


