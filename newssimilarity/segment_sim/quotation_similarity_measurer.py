from newssimilarity.segment_sim.segment_similarity_measurement import SegmentSimMeasurement


class QuotationSimilarityMeasurer(SegmentSimMeasurement):
    def calculate_similarity(self):
        """
        Check whether target segment shares any quotations with source segment
        :return: True if they share a quotation, False otherwise
        """

        s1_quotations = []
        for feature in self.source_segment.feature_list:
            if feature.feature_name == 'punctuation':
                for instance in feature.feature_instance_list:
                    if instance.type == 'quotation':
                        s1_quotations.append(instance.content)

        s2_quotations = []
        for feature in self.target_segment.feature_list:
            if feature.feature_name == 'punctuation':
                for instance in feature.feature_instance_list:
                    if instance.type == 'quotation':
                        s2_quotations.append(instance.content)

        for quotation in s1_quotations:
            if quotation in s2_quotations:
                return True

        return False
