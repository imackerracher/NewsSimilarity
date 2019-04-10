from newssimilarity.feature_sim.feature_similarity_measurement import FeatureSimMeasurement


class NESimilarityMeasurement(FeatureSimMeasurement):
    def named_entity_overlap(self, source_article, target_article):
        """
        Ratio of named entities that both articles share
        :param source_article: Source article as article object
        :param target_article: Target article as article object
        :return: Float, ratio of named entities that both articles share
        """

        a1_nes = [instance.content
                  for feature in source_article.feature_list
                  if feature.feature_name == 'named_entity_sequence_default'
                  for instance in feature.feature_instance_list]
        a2_nes = [instance.content
                  for feature in target_article.feature_list
                  if feature.feature_name == 'named_entity_sequence_default'
                  for instance in feature.feature_instance_list]

        a1_set = set(a1_nes)
        a2_set = set(a2_nes)
        intersection_count = len(a1_set.intersection(a2_set))
        union_count = len(a1_set.union(a2_set))

        if union_count == 0:
            return 0

        else:
            return (intersection_count / float(union_count))

    def greedy_named_entity_tiling(self, source_article, target_article):
        """
        Greedy citation tiling applied to named entities.
        :param source_article: Source article as article object
        :param target_article: Target article as article object
        :return: List of the named entity tiles
        """

        a1_nes = [instance.content
                  for feature in source_article.feature_list
                  if feature.feature_name == 'named_entity_sequence_default'
                  for instance in feature.feature_instance_list]
        a2_nes = [instance.content
                  for feature in target_article.feature_list
                  if feature.feature_name == 'named_entity_sequence_default'
                  for instance in feature.feature_instance_list]

        i = 0
        tiles = []
        while i < len(a1_nes):
            tile = []
            for j in range(0, len(a2_nes)):
                if i < len(a1_nes):
                    if a1_nes[i] == a2_nes[j]:
                        tile.append(a1_nes[i])
                        i += 1
            tiles.append(tile)

            i += 1

        return tiles

    def named_entity_coupling(self, source_article, target_article):
        """
        Normalised coupling strength of the two articles
        :param source_article: Source article as article object
        :param target_article: Target article as article object
        :return: Float of coupling strength
        """

        a1_nes = [instance.content
                  for feature in source_article.feature_list
                  if feature.feature_name == 'named_entity_sequence_default'
                  for instance in feature.feature_instance_list]
        a2_nes = [instance.content
                  for feature in target_article.feature_list
                  if feature.feature_name == 'named_entity_sequence_default'
                  for instance in feature.feature_instance_list]

        a1_set = set(a1_nes)
        a2_set = set(a2_nes)

        coupling_strength = len(a1_set.intersection(a2_set))
        # max and min coupling strength over corpus
        max_coupling_strength = 28
        min_coupling_strength = 0
        coupling_strength_normalised = (coupling_strength - min_coupling_strength) / (
        max_coupling_strength - min_coupling_strength)

        return (coupling_strength_normalised)

    def longest_common_ne_sequence(self, source_article, target_article):
        """
        Longest common citation sequence applied to named entites.
        :param source_article: Source article as article object
        :param target_article: Target article as article object
        :return: Int of the lcne sequence
        """

        a1_nes = [instance.content
                  for feature in source_article.feature_list
                  if feature.feature_name == 'named_entity_sequence_default'
                  for instance in feature.feature_instance_list]
        a2_nes = [instance.content
                  for feature in target_article.feature_list
                  if feature.feature_name == 'named_entity_sequence_default'
                  for instance in feature.feature_instance_list]

        # dynamic programming approach
        table = [[0] * (len(a1_nes) + 1) for i in range(0, len(a2_nes) + 1)]
        for i in range(1, len(table)):
            for k in range(1, len(table[0])):
                if a2_nes[i - 1] == a1_nes[k - 1]:
                    table[i][k] = table[i - 1][k - 1] + 1
                else:
                    table[i][k] = max(table[i - 1][k], table[i][k - 1])

        # last elemnt in table, i.e. bottom right corner
        lcnes = table[-1][-1]
        # max and min in entire corpus
        max_lcnes = 64
        min_lcnes = 0
        lcnes_normalised = (lcnes - min_lcnes) / (max_lcnes - min_lcnes)
        return lcnes_normalised

    def calculate_similarity(self):
        """
        Handles the calculations
        :param source_article: Source article as article object
        :param target_article: Target article as article object
        :return: Similarity values
        """
        return self.longest_common_ne_sequence(self.source_article, self.target_article)
        # return self.named_entity_overlap(source_article, target_article)
        # return self.named_entity_coupling(source_article, target_article)
