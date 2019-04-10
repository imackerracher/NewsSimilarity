"""
Named entity overlap between 2 segments
"""

from newssimilarity.segment_sim.segment_similarity_measurement import SegmentSimMeasurement
from newssimilarity.utils.preprocessor import Preprocessor


class NESynOverlap(SegmentSimMeasurement):
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

    def calculate_similarity(self):
        """
        Determine ne overlap of 2 segments
        :return: Ratio of overlapping named entities between source and target segment
        """

        mode = 'manual' if self.sequence_type == 'manual' else 'default'
        s1_ne_syns = [token for token in self.source_segment.get_instances('ne_syn_' + mode, 'content')]
        s2_ne_syns = [token for token in self.target_segment.get_instances('ne_syn_' + mode, 'content')]

        intersection_count = 0
        for syn1 in s1_ne_syns:
            for syn2 in s2_ne_syns:
                if set(syn1).intersection(syn2):
                    intersection_count += 1
                    break

        intersection_count
        union_count = len(set(s1_ne_syns).union(set(s2_ne_syns)))

        if union_count == 0:
            return 0

        else:
            return (intersection_count / float(union_count))
