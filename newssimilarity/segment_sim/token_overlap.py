"""
The token overlap between 2 articles

Returned value is normalised between 0-1 by default
"""

from newssimilarity.segment_sim.segment_similarity_measurement import SegmentSimMeasurement
from newssimilarity.utils.preprocessor import Preprocessor


class TokenOverlap(SegmentSimMeasurement):
    def __init__(self, source_segment, target_segment, lower_case=True, stopword_removal=False,
                 stemming=False, stemmer='porter', lemmatization=False):
        """

        :param source_segment: Segment from source article
        :param target_segment: Segment from target article
        :param lower_case: Flag, whether all tokens should be lower case
        :param stopword_removal: Flag, whether stop words should be removed before the computation
        :param stemming: Flag, whether word stems should be used instead
        :param stemmer: Flag, to decide which stemmer to use
        :param lemmatization: Flag to decide, if words lemmas should be used instead
        """
        SegmentSimMeasurement.__init__(self, source_segment, target_segment)
        self.lower_case = lower_case
        self.stopword_removal = stopword_removal
        self.stemming = stemming
        self.stemmer = stemmer
        self.lemmatization = lemmatization

    def calculate_similarity(self):

        """
        Calculates the ratio of overlapping tokens between two articles.
        This method doesn't consider multiple occurrences of the same token.
        :return: Jaccard Coefficient
        """

        s1_tokens = [token for token in self.source_segment.get_instances('part_of_speech', 'content')]
        s2_tokens = [token for token in self.target_segment.get_instances('part_of_speech', 'content')]



        s1_tokens_preprocessed = Preprocessor(s1_tokens, lower_case=self.lower_case,
                                              stopword_removal=self.stopword_removal,
                                              stemming=self.stemming, stemmer=self.stemmer,
                                              lemmatization=self.lemmatization).process()
        s2_tokens_preprocessed = Preprocessor(s2_tokens, lower_case=self.lower_case,
                                              stopword_removal=self.stopword_removal,
                                              stemming=self.stemming, stemmer=self.stemmer,
                                              lemmatization=self.lemmatization).process()

        s1_set = set([token[0] for token in s1_tokens_preprocessed])
        s2_set = set([token[0] for token in s2_tokens_preprocessed])
        intersection_count = len(s1_set.intersection(s2_set))
        union_count = len(s1_set.union(s2_set))


        if intersection_count == 0 or union_count == 0:
            return 0
        else:
            return (intersection_count / float(union_count))
