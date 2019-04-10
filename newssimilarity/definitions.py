import os
from pathlib import Path

project_root = os.path.dirname(os.path.abspath(__file__))
#news_features_data = '/Users/ianmackerracher/PycharmProjects/NewsFeaturesIan/newsfeature/data/extracted_features'
single_value_features = ['Token Overlap']
n_value_features = ['Word Embeddings', 'Sparse Vector']

slash ='\\' if os.name =='nt' else '/'
#exported_features_path = [project_root, 'data', 'ml_features']

processed_test_files_path = [str(Path(project_root).parent.parent), 'NewsFeaturesIan',
                                              'newsfeature', 'data']

processed_news_features_path = [str(Path(project_root).parent.parent), 'NewsFeaturesIan',
                                              'newsfeature', 'data', 'ian', 'saved_files', 'features']

processed_meter_corpus_path = [str(Path(project_root).parent.parent), 'NewsFeaturesIan',
                                              'newsfeature', 'data', 'ian', 'saved_files', 'meter']


saved_models_path = [str(Path(project_root).parent.parent), 'NewsSimilarityIan',
                                              'newssimilarity', 'data', 'saved_models']

vand_folder_path = [project_root, 'data', 'Vand']
