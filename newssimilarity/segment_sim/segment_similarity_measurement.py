from abc import ABCMeta, abstractmethod

"""
Abstract base class for all segment similarity classes
"""


class SegmentSimMeasurement(object, metaclass=ABCMeta):
    def __init__(self, source_segment, target_segment):
        """
        :param source_segment: Segment from source article
        :param target_segment: Segment from target article
        """
        self.source_segment = source_segment
        self.target_segment = target_segment

    @abstractmethod
    def calculate_similarity(self):
        """
        Every implemented class must have a method that calculates the similarity
        between 2 or more articles
        :return: A measure of similarity, probably a number between 0(completely dissimilar)
        and 1(exact copy)
        """

        raise NotImplementedError('this method must be implemented')
