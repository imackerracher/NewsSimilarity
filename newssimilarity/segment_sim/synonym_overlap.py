"""
The token overlap between 2 articles, including synonyms, hypernyms, hyponyms.
Two words are treated as being the same if they are synonyms, one is a hypernym
of the other or one is a hyponym of the other.

Returned value is normalised between 0-1 by default
"""

from newssimilarity.segment_sim.segment_similarity_measurement import SegmentSimMeasurement
from newssimilarity.utils.preprocessor import Preprocessor
from newssimilarity.utils.sim.wordnet_handler import WordnetHandler



class SynonymOverlap(SegmentSimMeasurement):
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

    def get_dict(self, tokens):
        wordnet_handler = WordnetHandler()
        syn_dict = {}
        synonyms = []
        hyper_dict = {}
        hypernyms = []
        hypo_dict = {}
        hyponyms = []
        for tup in tokens:
            if tup[0] not in syn_dict:
                s = wordnet_handler.get_synonyms(tup[0])
                syn_dict[tup[0]] = s
                synonyms += s
            if tup[0] not in hyper_dict:
                hyper = wordnet_handler.get_hypernyms(tup[0])
                hyper_dict[tup[0]] = hyper
                hypernyms += hyper
            if tup[0] not in hypo_dict:
                hypo = wordnet_handler.get_hyponyms(tup[0])
                hypo_dict[tup[0]] = hypo
                hyponyms += hypo
        return syn_dict, synonyms, hyper_dict, hypernyms, hypo_dict, hyponyms

    def get_intersection_count(self, *args):
        intersection_count = 0
        # check if word matches, if yes: increment counter
        # if not, check if word matches one of the synonyms
        # if not check if one of the synonyms match the word
        for token1 in args[0]:
            if token1 in args[1]:
                # print('1: token1: {} '.format(token1))
                intersection_count += 1
            elif token1 in args[2]:
                intersection_count += 1
            elif token1 in args[3]:
                intersection_count += 1

            elif token1 in args[4]:
                intersection_count += 1
            elif token1 in args[5]:
                intersection_count += 1
            elif token1 in args[6]:
                intersection_count += 1

            elif len(set(args[0][token1]).intersection(args[9])) > 0:
                intersection_count += 1
            elif len(set(args[7][token1]).intersection(args[9])) > 0:
                intersection_count += 1
            elif len(set(args[8][token1]).intersection(args[9])) > 0:
                intersection_count += 1

        return intersection_count

    def calculate_similarity(self):

        s1_tups = [token for token in self.source_segment.get_instances('part_of_speech', 'content')]
        s2_tups = [token for token in self.target_segment.get_instances('part_of_speech', 'content')]

        s1_pre_toks = Preprocessor(s1_tups, lower_case=self.lower_case,
                                    stopword_removal=self.stopword_removal,
                                    stemming=self.stemming, stemmer=self.stemmer,
                                    lemmatization=self.lemmatization).process()
        s2_pre_toks = Preprocessor(s2_tups, lower_case=self.lower_case,
                                    stopword_removal=self.stopword_removal,
                                    stemming=self.stemming, stemmer=self.stemmer,
                                    lemmatization=self.lemmatization).process()

        s1_syn_dict, s1_synonyms, \
        s1_hyper_dict, s1_hypernyms, \
        s1_hypo_dict, s1_hyponyms = self.get_dict(s1_pre_toks)
        # s1_synonyms = [syn for word in s1_syn_dict for syn in s1_syn_dict[word]]
        s1_tokens = set([token for token in s1_syn_dict])

        s2_syn_dict, s2_synonyms, \
        s2_hyper_dict, s2_hypernyms, \
        s2_hypo_dict, s2_hyponyms = self.get_dict(s2_pre_toks)
        s2_synonyms = [syn for word in s2_syn_dict for syn in s2_syn_dict[word]]
        s2_tokens = set([token for token in s2_syn_dict])

        intersection_count = self.get_intersection_count(s1_syn_dict, s2_syn_dict, s2_hyper_dict, s2_hypo_dict,
                                                         s2_synonyms, s2_hypernyms, s2_hyponyms,
                                                         s1_hyper_dict, s1_hypo_dict, s2_tokens)

        """intersection_count2 = self.get_intersection_count(s2_syn_dict, s1_syn_dict, s1_hyper_dict, s1_hypo_dict,
                                                         s1_synonyms, s1_hypernyms, s1_hyponyms,
                                                         s2_hyper_dict, s2_hypo_dict, s1_tokens)"""

        union_count = len(s1_tokens.union(s2_tokens))

        if intersection_count == 0 or union_count == 0:
            return 0
        else:
            return intersection_count / union_count

