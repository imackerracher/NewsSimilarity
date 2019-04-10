import math
from newssimilarity.feature_sim.feature_similarity_measurement import FeatureSimMeasurement


class SentenceLengthSimilarityMeasurement(FeatureSimMeasurement):
    def calculate_similarity(self):
        """
        Calculate the similarity between the sentence lengths of the two articles
        :param source_article: Source article as article object
        :param target_article: Target article as article object
        :return: Distance between average lengths of sentences
        """

        a1_sentence_lengths = []
        for feature in self.source_article.feature_list:
            if feature.feature_name == 'punctuation':
                for instance in feature.feature_instance_list:
                    if instance.type == 'sentence_length':
                        a1_sentence_lengths.append(instance.content)

        a2_sentence_lengths = []
        for feature in self.target_article.feature_list:
            if feature.feature_name == 'punctuation':
                for instance in feature.feature_instance_list:
                    if instance.type == 'sentence_length':
                        a2_sentence_lengths.append(instance.content)

        a1_avg = sum(a1_sentence_lengths) / len(a1_sentence_lengths)
        a2_avg = sum(a2_sentence_lengths) / len(a2_sentence_lengths)

        return math.sqrt((a1_avg - a2_avg) ** 2)
        # return max(a1_avg, a2_avg) - min(a1_avg, a2_avg)
