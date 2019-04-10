from abc import ABCMeta, abstractmethod

"""
A features consists of a list of instances. E.g. List<POS> and the name
of the features. E.g. part of speech tags, start position and end position in the text
"""


class Feature(object, metaclass=ABCMeta):
    def __init__(self, feature_name, feature_instance_list):
        """
        :param feature_name: The name of the feature. For example "part_of_speech"
        :param feature_instance_list: A list containing all the feature instances
        """
        self.feature_name = feature_name
        self.feature_instance_list = feature_instance_list

    @abstractmethod
    def get_feature_name(self):
        raise NotImplementedError('must be impplemented')
