from newssimilarity.definitions import slash, processed_news_features_path
import csv

"""
Don't use this method
"""


def parse(file_name):
    """
    At the moment only returns the featuresets and labels, but more information is available
    :return:
    """

    feature_names = ['GST', 'GST syn', 'LCS', 'LCS syn', 'TO', 'TO syn', 'Sparse Vector',
     # 'TFIDF': tfidf_X,
     'Word Embeddings', 'Word Lengths', 'Word Level Levenshtein',
     'WN Path Matrix', 'WN LCH Matrix', 'WN WUP Matrix',
     'NE Coupling', 'NE Coupling syn', 'NE GT',
     'NE GT syn', 'NE LCS', 'NE LCS syn', 'NE Overlap', 'NE Overlap syn', 'LCSubstring',
     'Sentence Lengths', 'String Matching', 'Punctuation Overlap']




    file_path = slash.join(processed_news_features_path + [file_name])

    return 's', 't', file_path

    phrase_pairs = []
    labels = []
    origins = []
    features = {'GST':[], 'GST syn':[], 'LCS':[], 'LCS syn':[], 'TO':[],
                'TO syn':[], 'Sparse Vector':[], # 'TFIDF': tfidf_X,
                'Word Embeddings':[], 'Word Lengths':[], 'Word Level Levenshtein':[],
                'WN Path Matrix':[], 'WN LCH Matrix':[], 'WN WUP Matrix':[],
                'NE Coupling':[], 'NE Coupling syn':[], 'NE GT':[], 'NE GT syn':[],
                'NE LCS':[], 'NE LCS syn':[], 'NE Overlap':[], 'NE Overlap syn':[],
                'LCSubstring':[], 'Sentence Lengths':[], 'String Matching':[], 'Punctuation Overlap':[]}
    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        #i = 0
        for line in reader:
            if len(line)>0 and line[0] != 'source':
                #print(line)
                phrase_pairs.append(line[:2])
                #labels.append([1,0] if line[2] == '1' else [0,1])
                labels.append(int(line[2]))
                #labels.append(float(line[2]))
                origins.append(line[3])
                f = list(zip(feature_names, [float(n) for n in line[4:]]))
                #print(f)
                for label, val in f:
                    features[label].append(val)
                #i+=1
            #if i == 800:
            #    break

    return features, labels
