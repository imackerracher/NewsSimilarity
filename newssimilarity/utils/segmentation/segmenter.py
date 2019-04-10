"""
Metaclass to segment an article into various segment sizes (article or sentences)
"""

from abc import ABCMeta, abstractmethod
from newssimilarity.model.features.ne_feature import NEFeature
from newssimilarity.model.features.pos_feature import POSFeature


class Segmenter(object, metaclass=ABCMeta):
    def print(self, processed_segment_list, feature_name):
        """
        Function for testing purposes.
        :param segment_list:
        :return:
        """

        for segment in processed_segment_list:
            instance_list = [(instance.content, (instance.start_pos, instance.end_pos))
                             for feature in segment.feature_list
                             if feature.feature_name == feature_name
                             for instance in feature.feature_instance_list]

            print(segment.type, segment.start_pos, segment.end_pos, segment.text, instance_list)

    def fill_segment(self, instance_list, segment):
        """
        Fill the segment with all the features that belong into it
        :param instance_list: List of instances that fill the segment
        :param segment: The segment that receives the feature instances
        :return: List of instances in that segment
        """
        return [instance
                for instance in instance_list
                if instance.start_pos >= segment.start_pos
                and instance.end_pos <= segment.end_pos]

    def process(self, segment_list, article):
        """
        Assign all the relevant feature instances to the segment
        :param segment_list: The segment list without the feature instances
        :param article: The input article object
        :return: The segment list with the feature instances
        """

        nes_default = article.get_instances('named_entity_sequence_default')
        nes_manual = article.get_instances('named_entity_sequence_manual')
        pos_default = article.get_instances('part_of_speech')
        pos_meaningful = article.get_instances('part_of_speech_meaningful')
        keyword = article.get_instances('keyword')

        # not optimal yet, doesn't have to run through entire named_entity list
        processed_segment_list = []
        for segment in segment_list:
            segment.feature_list.append(
                NEFeature('named_entity_sequence_default', self.fill_segment(nes_default, segment)))
            segment.feature_list.append(
                NEFeature('named_entity_sequence_manual', self.fill_segment(nes_manual, segment)))
            segment.feature_list.append(POSFeature('part_of_speech', self.fill_segment(pos_default, segment)))
            segment.feature_list.append(
                POSFeature('part_of_speech_meaningful', self.fill_segment(pos_meaningful, segment)))
            segment.feature_list.append(POSFeature('keyword', self.fill_segment(keyword, segment)))

            processed_segment_list.append(segment)

        return processed_segment_list

    @abstractmethod
    def segment(self):
        """
        Segment article
        :return: Segments (article or list of sentences)
        """

        raise NotImplementedError('this method must be implemented')
