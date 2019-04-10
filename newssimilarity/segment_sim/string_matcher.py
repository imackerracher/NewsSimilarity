from newssimilarity.segment_sim.segment_similarity_measurement import SegmentSimMeasurement


class StringMatcher(SegmentSimMeasurement):
    def calculate_similarity(self):
        """
        Match the strings of source and target segment
        :return: True, if the segments are excatly the same, word for word
        """

        return self.source_segment == self.target_segment
