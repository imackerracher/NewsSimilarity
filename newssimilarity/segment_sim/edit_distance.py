"""
Word level edit distance
"""
import editdistance
from newssimilarity.utils.preprocessor import Preprocessor
from newssimilarity.segment_sim.segment_similarity_measurement import SegmentSimMeasurement


class EditDistance(SegmentSimMeasurement):
    def __init__(self, source_segment, target_segment, lower_case=True, stopword_removal=True,
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

    def normalise(self, edit):
        """
        Normalise the edit distance, over the entire corpus
        :param edit: Score from similarity computation
        :return: Normalised value
        """

        # values that scorer uses to determine information reuse type
        if edit <= 1:
            return 1.0
        elif edit <= 4:
            return 0.5
        elif edit <= 6:
            return 0.35
        else:
            return 0

    def calculate_similarity(self):
        """
        Normalised over entire test corpus
        Calculate the word level similarity between the token lists from 2 articles
        possible flags: stopwords, lower case
        :return: A value of similarity
        """

        # get a list of tokens withouth the part of speech tags
        ss_tokens = [token for token in self.source_segment.get_instances('part_of_speech', 'content')]
        ts_tokens = [token for token in self.target_segment.get_instances('part_of_speech', 'content')]

        ss_tokens_preprocessed = Preprocessor(ss_tokens, lower_case=self.lower_case,
                                              stopword_removal=self.stopword_removal,
                                              stemming=self.stemming, stemmer=self.stemmer,
                                              lemmatization=self.lemmatization).process()
        ts_tokens_preprocessed = Preprocessor(ts_tokens, lower_case=self.lower_case,
                                              stopword_removal=self.stopword_removal,
                                              stemming=self.stemming, stemmer=self.stemmer,
                                              lemmatization=self.lemmatization).process()

        edit = editdistance.eval(ss_tokens_preprocessed, ts_tokens_preprocessed)

        return self.normalise(edit)
