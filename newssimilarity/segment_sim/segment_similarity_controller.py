"""
Controlls all the similarity methods
"""

from newssimilarity.segment_sim.edit_distance import EditDistance
from newssimilarity.segment_sim.token_overlap import TokenOverlap
from newssimilarity.segment_sim.tf_idf import TfIdf
from newssimilarity.segment_sim.greedy_ne_tiling import GreedyNETiling
from newssimilarity.segment_sim.greedy_ne_syn_tiling import GreedyNESynTiling
from newssimilarity.segment_sim.longest_common_ne_sequence import LongestCommonNESequence
from newssimilarity.segment_sim.longest_common_ne_syn_sequence import LongestCommonNESynSequence
from newssimilarity.segment_sim.ne_coupling import NECoupling
from newssimilarity.segment_sim.ne_syn_coupling import NESynCoupling
from newssimilarity.segment_sim.ne_overlap import NEOverlap
from newssimilarity.segment_sim.ne_syn_overlap import NESynOverlap
from newssimilarity.segment_sim.synonym_overlap import SynonymOverlap
from newssimilarity.feature_sim.outlet_similarity_measurement import OutletSimilarityMeasurement
from newssimilarity.feature_sim.writer_similarity_measurement import WriterSimilarityMeasurement
from newssimilarity.utils.segmentation.sentence_segmenter import SentenceSegmenter
from newssimilarity.utils.segmentation.article_segmenter import ArticleSegmenter
from newssimilarity.utils.corpus_extraction.extractor import Extractor


class SegmentSimilarityController:
    def __init__(self, topics):
        self.topics = topics
        self.corpus_tokens, self.article_tokens, self.sentence_tokens = \
            Extractor(topics).run()[0], Extractor(topics).run()[1], Extractor(topics).run()[2]


    def segment_similarity(self, source_segment_list, target_segment_list, level='sentence'):
        """
        Calculate all the different similarity measures for 2 segments
        :param source_segment_list: Segments from source article
        :param target_segment_list: Segments from target article
        :return: A similarity dictionary for each method between the 2 segments
        """

        similarity_dict = {'editdistance': [], 'tokenoverlap': [], 'synonymoverlap': [], 'tfidf': [],
                           'greedynetiling': [], 'greedynesyntiling': [],
                           'greedynetilingman': [], 'greedynesyntilingman': [],
                           'lcnes': [], 'lcnesyn': [],
                           'lcnesman': [], 'lcnesynman': [],
                           'necoupling': [],  'nesyncoupling': [],
                           'necouplingman': [], 'nesyncouplingman': [],
                           'neoverlap': [], 'nesynoverlap': [],
                           'neoverlapman': [], 'nesynoverlapman': []}
        for source_segment in source_segment_list:
            for target_segment in target_segment_list:
                def sim_value(method, source_segment, target_segment, flag=None):
                    """
                    Move this method out of loop?
                    """

                    if flag == 'manual':
                        return (
                            method(source_segment, target_segment, sequence_type='manual').calculate_similarity(),
                            source_segment, target_segment)
                    elif flag == 'tfidf':
                        if level=='sentence':
                            return (
                                method(self.corpus_tokens, self.sentence_tokens, source_segment, target_segment)
                                    .calculate_similarity(), source_segment, target_segment)
                        else:
                            return (
                                method(self.corpus_tokens, self.article_tokens, source_segment, target_segment)
                                    .calculate_similarity(), source_segment, target_segment)
                    else:
                        return (
                            method(source_segment, target_segment).calculate_similarity(), source_segment, target_segment)

                similarity_dict['editdistance'].append(sim_value(EditDistance, source_segment, target_segment))
                similarity_dict['tokenoverlap'].append(sim_value(TokenOverlap, source_segment, target_segment))
                similarity_dict['synonymoverlap'].append(sim_value(SynonymOverlap, source_segment, target_segment))
                similarity_dict['tfidf'].append(sim_value(TfIdf, source_segment, target_segment, flag='tfidf'))
                similarity_dict['greedynetiling'].append(sim_value(GreedyNETiling, source_segment, target_segment))
                similarity_dict['greedynesyntiling'].append(sim_value(GreedyNESynTiling, source_segment, target_segment))
                similarity_dict['greedynetilingman'].append(sim_value(GreedyNETiling, source_segment, target_segment, flag='manual'))
                similarity_dict['greedynesyntilingman'].append(sim_value(GreedyNESynTiling, source_segment, target_segment, flag='manual'))
                similarity_dict['lcnes'].append(sim_value(LongestCommonNESequence, source_segment, target_segment))
                similarity_dict['lcnesyn'].append(sim_value(LongestCommonNESynSequence, source_segment, target_segment))
                similarity_dict['lcnesman'].append(sim_value(LongestCommonNESequence, source_segment, target_segment, flag='manual'))
                similarity_dict['lcnesynman'].append(sim_value(LongestCommonNESynSequence, source_segment, target_segment, flag='manual'))
                similarity_dict['necoupling'].append(sim_value(NECoupling, source_segment, target_segment))
                similarity_dict['nesyncoupling'].append(sim_value(NESynCoupling, source_segment, target_segment))
                similarity_dict['necouplingman'].append(sim_value(NECoupling, source_segment, target_segment, flag='manual'))
                similarity_dict['nesyncouplingman'].append(sim_value(NESynCoupling, source_segment, target_segment, flag='manual'))
                similarity_dict['neoverlap'].append(sim_value(NEOverlap, source_segment, target_segment))
                similarity_dict['nesynoverlap'].append(sim_value(NESynOverlap, source_segment, target_segment))
                similarity_dict['neoverlapman'].append(sim_value(NEOverlap, source_segment, target_segment, flag='manual'))
                similarity_dict['nesynoverlapman'].append(sim_value(NESynOverlap, source_segment, target_segment, flag='manual'))

        return similarity_dict

    def feature_similarity(self, source_article, target_article, similarity_dict):
        """
        Apply feature similarity methods, add them to similartiy dictionary and return it again. Only on article level.
        :param source_article:
        :param target_article:
        :return:
        """

        source_segment = ArticleSegmenter(source_article).segment()[0]
        target_segment = ArticleSegmenter(target_article).segment()[0]


        similarity_dict['sourcecomp'] = \
            [(OutletSimilarityMeasurement(source_article, target_article).calculate_similarity(),
              source_segment, target_segment)]

        similarity_dict['writercomp'] = \
            [(WriterSimilarityMeasurement(source_article, target_article).calculate_similarity(),
              source_segment, target_segment)]


        return similarity_dict





    def process(self):
        """
        For each topic a similarity dictionary on sentence level and on article level is calculated
        :return: List of tuples with sentence and article similarity
        """

        article_similarity_list = []



        for topic in self.topics:
            source_sentences = SentenceSegmenter(topic[0]).segment()

            target_sentences = SentenceSegmenter(topic[1]).segment()
            sentence_sim_dict = self.segment_similarity(source_sentences, target_sentences, level='sentence')

            source_article = ArticleSegmenter(topic[0]).segment()
            target_article = ArticleSegmenter(topic[1]).segment()
            article_sim_dict = self.segment_similarity(source_article, target_article, level='article')
            article_sim_dict = self.feature_similarity(topic[0], topic[1], article_sim_dict)

            article_similarity_list.append((sentence_sim_dict, article_sim_dict))

        return article_similarity_list
