"""
Takes the json files that were processed and exported by news features and makes an article object out of them
"""

import json
import os
from pathlib import Path

from newssimilarity.model.annotation import Annotation
from newssimilarity.model.article import Article
from newssimilarity.model.feature_instances.keyword_feature_instance import KeywordFeatureInstance
from newssimilarity.model.feature_instances.ne_feature_instance import NEFeatureInstance
from newssimilarity.model.feature_instances.ne_syn_feature_instance import NESynFeatureInstance
from newssimilarity.model.feature_instances.pos_feature_instance import POSFeatureInstance
from newssimilarity.model.feature_instances.punctuation_feature_instance import PunctuationFeatureInstance
from newssimilarity.model.feature_instances.reference_feature_instance import ReferenceFeatureInstance
from newssimilarity.model.feature_instances.source_feature_instance import SourceFeatureInstance
from newssimilarity.model.feature_instances.writer_feature_instance import WriterFeatureInstance
from newssimilarity.model.features.keyword_feature import KeywordFeature
from newssimilarity.model.features.ne_feature import NEFeature
from newssimilarity.model.features.ne_syn_feature import NESynFeature
from newssimilarity.model.features.pos_feature import POSFeature
from newssimilarity.model.features.punctuation_feature import PunctuationFeature
from newssimilarity.model.features.reference_feature import ReferenceFeature
from newssimilarity.model.features.source_feature import SourceFeature
from newssimilarity.model.features.writer_feature import WriterFeature
from newssimilarity.utils.parsing.parser import Parser


class JsonParser(Parser):
    def __init__(self):
        # Data paths to corpus
        self.data_path = str(Path(__file__).parents[2]) + '/data/ExportedFromFeatures/FinalCorpus/'

    def read_file(self, file_name):
        """

        :param file_name: Name of the article to be read
        :return: The article as a json object
        """
        file = open(self.data_path + file_name).read()
        json_article = json.loads(file)
        return json_article

    def get_annotations(self, annotation_list_json):
        """
        This method finds all the annotations in the list of the article (json) and returns them again as a list of annotation
        objects.
        :param annotation_list_json: The list that contains all the annotations (not yet annotation objects)
        :return: List of annotation objects
        """

        annotation_list = []

        for annotation_dict in annotation_list_json:
            tag = annotation_dict['tag']
            phrase_id = annotation_dict['phrase_id']
            source = annotation_dict['source']
            source_id = annotation_dict['source_id']
            phrase_type = annotation_dict['phrase_type']
            body = annotation_dict['body']
            annotation = Annotation(tag, phrase_id, source, source_id, phrase_type, body)
            annotation_list.append(annotation)

        return annotation_list

    def get_features(self, feature_list_json):
        """
        Finds all the features in the json format of the article and creates feature instances from them.
        :param feature_list_json: List with all the features (json)
        :return: List of feature objects
        """

        feature_list = []

        for feature_dict in feature_list_json:

            def feature_list_create(feature_instance_type, feature_type, name):
                """
                helper function
                :param feature_instance_type: The type of feature instance passed
                :param feature_type: The type of feature passed
                :return: A feature with all the instances of one feature type
                """
                feature_type_list = []
                for feature_instance_dict in feature_dict['feature_instance_list']:
                    type = feature_instance_dict['type']
                    content = feature_instance_dict['content']
                    start_pos = feature_instance_dict['start_pos']
                    end_pos = feature_instance_dict['end_pos']
                    feature_instance = feature_instance_type(content, type, start_pos, end_pos)
                    feature_type_list.append(feature_instance)
                current_feature = feature_type(name, feature_type_list)
                return current_feature

            if feature_dict['type'] == 'keyword':
                feature_list.append(feature_list_create(KeywordFeatureInstance, KeywordFeature, 'keyword'))
            elif feature_dict['type'] == 'named_entity_sequence_default':
                feature_list.append(feature_list_create(NEFeatureInstance, NEFeature, 'named_entity_sequence_default'))
            elif feature_dict['type'] == 'named_entity_sequence_manual':
                feature_list.append(feature_list_create(NEFeatureInstance, NEFeature, 'named_entity_sequence_manual'))
            elif feature_dict['type'] == 'ne_synonyms_default':
                feature_list.append(feature_list_create(NESynFeatureInstance, NESynFeature, 'ne_synonyms_default'))
            elif feature_dict['type'] == 'ne_synonyms_manual':
                feature_list.append(feature_list_create(NESynFeatureInstance, NESynFeature, 'ne_synonyms_manual'))
            elif feature_dict['type'] == 'part_of_speech':
                feature_list.append(feature_list_create(POSFeatureInstance, POSFeature, 'part_of_speech'))
            elif feature_dict['type'] == 'part_of_speech_meaningful':
                feature_list.append(feature_list_create(POSFeatureInstance, POSFeature, 'part_of_speech_meaningful'))
            elif feature_dict['type'] == 'punctuation':
                feature_list.append(feature_list_create(PunctuationFeatureInstance, PunctuationFeature, 'punctuation'))
            elif feature_dict['type'] == 'reference':
                feature_list.append(feature_list_create(PunctuationFeatureInstance, PunctuationFeature, 'reference'))
            elif feature_dict['type'] == 'source':
                feature_list.append(feature_list_create(SourceFeatureInstance, SourceFeature, 'source'))
            elif feature_dict['type'] == 'writer':
                feature_list.append(feature_list_create(WriterFeatureInstance, WriterFeature, 'writer'))

        return feature_list

    def classify_tags(self, json_article):
        """
        Finds the different types of information that were tagged in the article (json) and create an Article object
        :param json_article: The file that was read in
        :return: Article object that contains all the relevant information
        """

        head = json_article['head']
        lead = json_article['lead']
        body = json_article['body']
        date = json_article['date']
        time = json_article['time']
        writers = json_article['writers']
        publisher = json_article['publisher'].rstrip()
        source_outlet = json_article['source_outlet']
        additional_information = json_article['additional_information']
        annotation_list = self.get_annotations(json_article['annotation_list'])
        feature_list = self.get_features(json_article['feature_list'])
        raw_article = json_article['raw_article']

        return Article(head, lead, body, date, time, writers, publisher,
                       source_outlet, additional_information, annotation_list,
                       feature_list, raw_article)


    def parse_topic(self, topic_name):
        """
        Reads in the topic that was passed and returns the articles in the topic folder as a list
        :param topic_name: The name of the topic that is being read in
        :return: List of article objects
        """
        topic_path = self.data_path + topic_name
        topic = []
        for file_name in os.listdir(topic_path):
            if file_name.endswith('.json'):
                file_json = self.read_file(topic_name + '/' + file_name)
                topic.append(self.classify_tags(file_json))
        return topic
