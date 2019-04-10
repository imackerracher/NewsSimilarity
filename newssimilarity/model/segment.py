"""
A segment is part of an article.
"""


class Segment(object):
    def __init__(self, type, start_pos, end_pos, text, feature_list, part=None):
        """
        :param type: Sentence segment or article segment. Paragraph segments get created from multiple sentence segments
        :param start_pos: The starting position of the segment in the article
        :param end_pos: The end position of the segment in the article
        :param text: The text contained in the segment
        :param feature_list: A list containing all the features in this segment, as feature objects
        :param part: Can be head, lead or body. To make sure a paragraph isn't extended beyond head or lead
        """
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.type = type
        self.text = text
        self.feature_list = feature_list
        self.part = part  # for sentence segmentes. part can be head, lead or body

    def get_instances(self, instance_type, part='content'):
        """
        Utility function to return a list of instances
        :param instance_type: e.g 'part_of_speech'
        :param part: part of the instance that should be returned. e.g. 'text'
        :return: Desired instance
        """
        if part == 'content':
            instances = [instance.content
                         for feature in self.feature_list
                         if feature.feature_name == instance_type
                         for instance in feature.feature_instance_list]

        return instances
