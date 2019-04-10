from abc import ABCMeta, abstractmethod

"""
Interface for all feature similarity classes.
"""


class FeatureSimMeasurement(object, metaclass=ABCMeta):
    def __init__(self, source_article, target_article):
        """
        :param source_article: article from source article
        :param target_article: article from target article
        """
        self.source_article = source_article
        self.target_article = target_article


    @abstractmethod
    def calculate_similarity(self):
        """
        Every implemented class must have a method that calculates the similarity
        between 2 or more articles
        :return: A measure of similarity, probably a number between 0(completely dissimilar)
        and 1(exact copy)
        """
        raise NotImplementedError('this method must be implemented')
