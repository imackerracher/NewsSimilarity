"""
Principle of Citation Coupling applied to named entities
"""

from newssimilarity.segment_sim.segment_similarity_measurement import SegmentSimMeasurement
from newssimilarity.utils.preprocessor import Preprocessor


class NESynCoupling(SegmentSimMeasurement):
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

    def normalise(self, coupling_strength):
        """
        Normalise coupling strength over entire corpus
        :param coupling_strength: NE coupling strength of source and target segment
        :return: The normalised value
        """
        # max and min coupling strength over corpus
        max_coupling_strength = 28
        min_coupling_strength = 0
        coupling_strength_normalised = (coupling_strength - min_coupling_strength) / (
        max_coupling_strength - min_coupling_strength)

        return (coupling_strength_normalised)

    def calculate_similarity(self):
        """
        Principle of bibliographic coupling applied to named entities.
        Determine ne coupling score between the 2 segments
        :return: Named entity coupling strength
        """

        mode = 'manual' if self.sequence_type == 'manual' else 'default'
        s1_ne_syns = [token for token in self.source_segment.get_instances('ne_syn_' + mode, 'content')]
        s2_ne_syns = [token for token in self.target_segment.get_instances('ne_syn_' + mode, 'content')]


        coupling_strenght = 0
        for syn1 in s1_ne_syns:
            for syn2 in s2_ne_syns:
                if set(syn1).intersection(syn2):
                    coupling_strenght += 1
                    break

        return coupling_strenght

