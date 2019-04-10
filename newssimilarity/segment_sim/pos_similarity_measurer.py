from newssimilarity.segment_sim.segment_similarity_measurement import SegmentSimMeasurement


class POSSimilarityMeasurement(SegmentSimMeasurement):
    def count_occurences(self, pos_list):
        """
        Count the occurrences of significant part of speech tags of a segment
        :param pos_list: List of part of speech tags
        :return: Frequency of certain part of speech tags
        """

        ntags = ['NNP', 'NNPS', 'NN', 'NNS']
        vtags = ['VB', 'VBD', 'VBG', 'VBN']
        atags = ['JJ', 'JJR', 'JJS']
        ftags = ['FW']

        pos_dict = {'Noun': 0, 'Verb': 0, 'Adj': 0}
        for pos in pos_list:
            if pos in ntags:
                pos_dict['Noun'] += 1
            elif pos in vtags:
                pos_dict['Verb'] += 1
            elif pos in atags:
                pos_dict['Adj'] += 1

        pos_dict['Noun'] = pos_dict['Noun'] / len(pos_list)
        pos_dict['Verb'] = pos_dict['Verb'] / len(pos_list)
        pos_dict['Adj'] = pos_dict['Adj'] / len(pos_list)

        return pos_dict

    def calculate_similarity(self):
        """
        Calculate the similarity part of speech tags of source and target segment
        :return: Similarity score
        """
        #Todo: implement
        s1_pos = self.source_segment.get_instances('part_of_speech')
        s2_pos = self.target_segment.get_instances('part_of_speech')
