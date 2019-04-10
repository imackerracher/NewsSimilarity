from newssimilarity.definitions import slash, processed_test_files_path
import csv


def parse(file_name):
    """
    At the moment only returns the featuresets and labels, but more information is available
    :return:
    """

    feature_names = ['source_id', 'target_id', 'GST', 'GST syn', 'LCS', 'LCS syn', 'TO', 'TO syn', 'Sparse Vector',
     # 'TFIDF': tfidf_X,
     'Word Embeddings', 'Word Lengths', 'Word Level Levenshtein',
     'WN Path Matrix', 'WN LCH Matrix', 'WN WUP Matrix',
     'NE Coupling', 'NE Coupling syn', 'NE GT',
     'NE GT syn', 'NE LCS', 'NE LCS syn', 'NE Overlap', 'NE Overlap syn', 'LCSubstring',
     'Sentence Lengths', 'String Matching', 'Punctuation Overlap']




    file_path = slash.join(processed_test_files_path + [file_name])

    features = {'source_id':[], 'target_id':[], 'GST':[], 'GST syn':[], 'LCS':[], 'LCS syn':[], 'TO':[],
                'TO syn':[], 'Sparse Vector':[], # 'TFIDF': tfidf_X,
                'Word Embeddings':[], 'Word Lengths':[], 'Word Level Levenshtein':[],
                'WN Path Matrix':[], 'WN LCH Matrix':[], 'WN WUP Matrix':[],
                'NE Coupling':[], 'NE Coupling syn':[], 'NE GT':[], 'NE GT syn':[],
                'NE LCS':[], 'NE LCS syn':[], 'NE Overlap':[], 'NE Overlap syn':[],
                'LCSubstring':[], 'Sentence Lengths':[], 'String Matching':[], 'Punctuation Overlap':[]}
    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            if line[0] != 'source':
                source, target, source_id, target_id = line[:4]
                f = list(zip(feature_names, [int(source_id), int(target_id)] + [float(n) for n in line[4:]]))
                for label, val in f:
                    features[label].append(val)


    return source, target, features


