"""
The principle of greedy string/citation tiling applied to named entities
or part of speech tags
"""

from newssimilarity.segment_sim.segment_similarity_measurement import SegmentSimMeasurement
from newssimilarity.utils.preprocessor import Preprocessor


class GreedyNETiling(SegmentSimMeasurement):
    def __init__(self, source_segment, target_segment, sequence_type='default', min_tile_length=2,
                 ne_disambiguation=False):
        """
        :param source_segment: Segment from source article
        :param target_segment: Segment from target article
        :param sequence_type: Sequence manual of sequence default
        :param ne_disambiguation: Flag, whether to disambiguate named entities
        """
        SegmentSimMeasurement.__init__(self, source_segment, target_segment)
        self.sequence_type = sequence_type
        self.min_tile_length = min_tile_length
        self.ne_disambiguation = ne_disambiguation

    def calculate_similarity(self):
        """
        Greedy citation tiling applied to named entities
        :return: Tiles exceeding a certain threshold (length)
        """

        if self.sequence_type == 'manual':
            s1_nes = [token for token in self.source_segment.get_instances('named_entity_sequence_manual', 'content')]
            s2_nes = [token for token in self.target_segment.get_instances('named_entity_sequence_manual', 'content')]
        else:
            s1_nes = [token for token in self.source_segment.get_instances('named_entity_sequence_default', 'content')]
            s2_nes = [token for token in self.target_segment.get_instances('named_entity_sequence_default', 'content')]

        s1_nes_preprocessed = Preprocessor(s1_nes, ne_disambiguation=self.ne_disambiguation).process()
        s2_nes_preprocessed = Preprocessor(s2_nes, ne_disambiguation=self.ne_disambiguation).process()

        i = 0
        tiles = []
        while i < len(s1_nes_preprocessed):
            tile = []
            for j in range(0, len(s2_nes_preprocessed)):
                if i < len(s1_nes_preprocessed):
                    if s1_nes_preprocessed[i] == s2_nes_preprocessed[j]:
                        tile.append(s1_nes_preprocessed[i])
                        i += 1
            tiles.append(tile)

            i += 1

        long_tiles = [len(tile) for tile in tiles if len(tile) >= self.min_tile_length]
        return long_tiles
