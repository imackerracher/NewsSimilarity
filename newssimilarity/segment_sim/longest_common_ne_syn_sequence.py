"""
Longest common named entity sequence
"""

from newssimilarity.segment_sim.segment_similarity_measurement import SegmentSimMeasurement
from newssimilarity.utils.preprocessor import Preprocessor


class LongestCommonNESynSequence(SegmentSimMeasurement):
    def __init__(self, source_segment, target_segment, sequence_type='default', ne_disambiguation=False):
        """
        :param source_segment: Segment from source article
        :param target_segment: Segment from target article
        :param sequence_type: Sequence manual of sequence default
        :param ne_disambiguation: Flag, whether to disambiguate named entities
        """
        SegmentSimMeasurement.__init__(self, source_segment, target_segment)
        self.sequence_type = sequence_type
        self.ne_disambiguation = ne_disambiguation

    def normalise(self, lcnes):
        """
        Normalise the value over the entire corpus
        :param lcnes: Longest common ne sequence between source and target segment
        :return: Normalised value
        """
        # max and min in entire corpus
        max_lcnes = 64
        min_lcnes = 0
        lcnesyn_normalised = (lcnes - min_lcnes) / (max_lcnes - min_lcnes)
        return lcnesyn_normalised

    def calculate_similarity(self):
        """
        Principle of longest common co-citation sequence applied to named entities.
        Determine the longest common named entity sequence between two segments and return the value
        :return: Length of lcne sequence
        """

        mode = 'manual' if self.sequence_type == 'manual' else 'default'
        s1_ne_syns = [token for token in self.source_segment.get_instances('ne_syn_' + mode, 'content')]
        s2_ne_syns = [token for token in self.target_segment.get_instances('ne_syn_' + mode, 'content')]

        #s1_nes_preprocessed = Preprocessor(s1_nes, ne_disambiguation=self.ne_disambiguation).process()
        #s2_nes_preprocessed = Preprocessor(s2_nes, ne_disambiguation=self.ne_disambiguation).process()

        # dynamic programming approach
        table = [[0] * (len(s1_ne_syns) + 1) for i in range(0, len(s2_ne_syns) + 1)]
        for i in range(1, len(table)):
            for k in range(1, len(table[0])):
                if set(s2_ne_syns[i - 1]).intersection(s1_ne_syns[k - 1]):
                    table[i][k] = table[i - 1][k - 1] + 1
                else:
                    table[i][k] = max(table[i - 1][k], table[i][k - 1])

        # last elemnt in table, i.e. bottom right corner
        lcnesyn = table[-1][-1]

        return lcnesyn
