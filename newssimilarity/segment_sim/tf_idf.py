from newssimilarity.segment_sim.segment_similarity_measurement import SegmentSimMeasurement
from nltk.corpus import stopwords
from scipy import spatial
import math
import nltk


class TfIdf(SegmentSimMeasurement):
    def __init__(self, token_dict, segment_list, source_segment, target_segment):
        """
        :param token_dict: all the tokens in the corpus as a dictionary with the frequencies
        :param segment_list: list of dictionaries containing all segments
        :param source_segment: The 2 segments that are being compared
        :param target_segment:
        """
        self.token_dict = token_dict
        self.token_list = [w for w in token_dict]
        self.segment_list = segment_list
        self.source_segment = source_segment
        self.target_segment = target_segment
        self.stop = set(stopwords.words('english'))

    def segment_token_dict(self, tokens):
        """
        Calculate the frequencies of all tokens apart from stop words
        :param tokens: All the tokens from an segment
        :return: Dictionary with the tokens and their frequencies
        """

        token_dict = {}
        for token in tokens:
            if token not in self.stop:
                if token in token_dict:
                    token_dict[token] += 1
                else:
                    token_dict[token] = 1

        return token_dict

    def tf(self, token, segment_token_dict, length_segment):
        """
        Term frequency
        :param token: Token, that gets counted
        :param segment_dict: dictionary with all the tokens and their frequencies for the segment
        :return:
        """
        return segment_token_dict[token] / length_segment

    def containing(self, token):
        """
        Number of segments that contain the token
        :param token:
        :return:
        """
        return sum([1 for dic in self.segment_list if token in dic])

    def idf(self, token):
        """
        Inverse document frequency
        :param token: Token that gets input, to calculate idf score
        :return: Idf score for token
        """
        # the number of segments in the corpus
        number_segments = len(self.segment_list)

        return math.log(number_segments) / (1 + self.containing(token))

    def tf_idf(self, segment):
        """
        Calculate the tf-idf value for the segment
        :param segment: segment that gets input
        :return: vector score for all the tokens
        """

        segment_tokens = [token.lower() for token in nltk.word_tokenize(segment.text) if token.lower() not in self.stop]

        segment_length = len(segment_tokens)
        segment_token_dict = self.segment_token_dict(segment_tokens)

        vector = []
        for token in self.token_list:
            if token.lower() in segment_tokens:
                tf = self.tf(token.lower(), segment_token_dict, segment_length)
                idf = self.idf(token)
                vector.append(tf*idf)
            else:
                vector.append(0)

        return vector


    def calculate_similarity(self, cosine=True):
        """
        Calculate the tf-idf score between source an target segment
        :return:
        """
        source_vector = self.tf_idf(self.source_segment)
        target_vector = self.tf_idf(self.target_segment)

        result = 1 - spatial.distance.cosine(source_vector, target_vector)
        return result
