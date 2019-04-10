from abc import ABCMeta, abstractmethod

"""
A features consists of a list of instances. E.g. List<POS> and the name
of the features. E.g. part of speech tags, start position and end position in the text
"""


class FeatureInstance(object, metaclass=ABCMeta):
    def __init__(self, content, type, start_pos=None, end_pos=None):
        self.content = content
        self.type = type
        self.start_pos = start_pos
        self.end_pos = end_pos
