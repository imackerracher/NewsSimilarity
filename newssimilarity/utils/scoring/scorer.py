"""
Use scorer to give a score to 2 articles.
Given a similarity dictionary with all the feature similarity measures and all the segments compared,
calculate a score that can be used to determine the type of information reuse
"""


class Scorer:
    def __init__(self, sim_list):
        """
        :param sim_list: List containing dictionary with values assigned to the segments for each method
        """
        self.sim_list = sim_list

    def choose_highest_score(self, reuse_occurence):
        """
        Make sure that each sentence is only part of one segment. choose the segment with the highest score
        A lot less found with this
        Don't use this anymore !!!
        :param reuse_occurences:
        :return:
        """

        min_score = [elem for elem in reuse_occurence if elem[0] >= 0.3]  # [:3]
        segments = []
        for elem in min_score:
            segments.append(elem[1])
            segments.append(elem[2])

        unique_segments = set(segments)
        max_elems = []
        for seg in unique_segments:
            max_elem = None
            for elem in min_score:
                if seg == elem[1]:
                    # print(seg.text, elem[1].text)
                    if max_elem is None:
                        max_elem = elem
                    elif elem[0] > max_elem[0]:
                        max_elem = elem
            if max_elem is not None:
                max_elems.append(max_elem)

        return max_elems

    def determine_type(self, sim_type, parameters, article_level=False):
        """
        in reuse_occurences['segments'] : contains 2 lists of segments. first list contains all the segments from one article,
        second list contains all the segments from other article.
        Every segment should only be allowed to be part of one reuse
        :param sim_type:
        :param parameters:
        :param article_level: Wether it runs on article level or sentence level. Sentence level by default
        :return: List of dictionaries containing the assigned type of information reuse for each method
        """

        reuse_occurences = []
        contains_sp_ep = []
        for index, match_1 in enumerate(sim_type):
            # make sure a paragrpah can't go beyond head, lead, body
            a1_seg1_part = match_1[1].part
            a2_seg1_part = match_1[2].part

            def match(type):
                article_1_segs = [match_1[1]]
                article_2_segs = [match_1[2]]
                for match_2 in sim_type[index + 1:]:

                    a1_seg2_part = match_2[1].part  # make sure a paragraph can't go beyond head, lead, body
                    a2_seg2_part = match_2[2].part

                    if (match_2[0] >= parameters[type + 'Minval'] and
                                match_2[1].start_pos == article_1_segs[-1].end_pos and
                                match_2[2].start_pos == article_2_segs[-1].end_pos and
                                a1_seg1_part == a1_seg2_part and
                                a2_seg1_part == a2_seg2_part):
                        article_1_segs.append(match_2[1])
                        article_2_segs.append(match_2[2])

                if len(article_1_segs) == 1:
                    # might have to change segments from tuple to list
                    if article_level:
                        new_sen_reuse = {'reuse': type + 'FA', 'segments': (article_1_segs, article_2_segs)}
                    else:
                        new_sen_reuse = {'reuse': type + 'Sen', 'segments': (article_1_segs, article_2_segs)}
                    if new_sen_reuse not in reuse_occurences:
                        reuse_occurences.append(new_sen_reuse)

                else:
                    new_par_reuse = {'reuse': type + 'Par', 'segments': (article_1_segs, article_2_segs)}
                    if new_par_reuse not in reuse_occurences:
                        reuse_occurences.append(new_par_reuse)
                    for seg_tup in zip(article_1_segs, article_2_segs):
                        new_sen_reuse = {'reuse': type + 'Sen', 'segments': ([seg_tup[0]], [seg_tup[1]])}
                        if new_sen_reuse not in reuse_occurences:
                            reuse_occurences.append(new_sen_reuse)

            if match_1[0] >= parameters['CPMinval']:
                match('CP')

            elif match_1[0] >= parameters['NearCPMinval']:
                match('NearCP')

            elif match_1[0] >= parameters['ParaphraseMinval']:
                match('Paraphrase')

        return reuse_occurences

    def article_segment_score(self, article_similarity_dict):
        """
        Determine reuse type on article level
        :param article_similarity_dict: Dictionary for each method with the assigned score on article level
        :return: Assigned reuse type
        """

        token_overlap = article_similarity_dict['tokenoverlap']
        synonym_overlap = article_similarity_dict['synonymoverlap']
        edit_distance = article_similarity_dict['editdistance']
        tf_idf = article_similarity_dict['tfidf']
        ne_overlap = article_similarity_dict['neoverlap']
        ne_overlap_man = article_similarity_dict['neoverlapman']

        def check_feature(feature_name):
            if article_similarity_dict[feature_name][0][0]:
                segments = article_similarity_dict[feature_name][0]
                feature_score = [{'reuse': True, 'segments': ([segments[1]], [segments[2]])}]
            else:
                feature_score = []

            return feature_score






        parameters = {'CPMinval': 0.9, 'NearCPMinval': 0.8, 'ParaphraseMinval': 1.1}
        score_list = [('token overlap', self.determine_type(token_overlap, parameters, article_level=True)),
                      ('synonym overlap', self.determine_type(synonym_overlap, parameters, article_level=True)),
                      ('edit distance', self.determine_type(edit_distance, parameters, article_level=True)),
                      ('tf idf', self.determine_type(tf_idf, parameters, article_level=True)),
                      ('source comparison', check_feature('sourcecomp')),
                      ('writer comparison', check_feature('writercomp')),
                      ('ne overlap', self.determine_type(ne_overlap, parameters, article_level=True)),
                      ('ne overlap man', self.determine_type(ne_overlap_man, parameters, article_level=True)),
                      ('greedy ne tiling', []),
                      ('greedy ne tiling man', []),
                      ('longest common ne sequence', []),
                      ('longest common ne sequence man', []),
                      ('ne coupling', []),
                      ('ne coupling man', [])]



        return score_list

    def sentence_segment_score(self, sentence_similarity_dict):
        """
        Determine reuse type on sentence/paragraph level
        :param sentence_similarity_dict: Dictionary for each method with the assigned score on sentence level
        :return: Assigned reuse types
        """

        edit_distance = sentence_similarity_dict['editdistance']
        edit_distance = [elem for elem in edit_distance if elem[0] >= 0.3]

        token_overlap = sentence_similarity_dict['tokenoverlap']
        token_overlap = [elem for elem in token_overlap if elem[0] >= 0.3]

        synonym_overlap = sentence_similarity_dict['synonymoverlap']
        synonym_overlap = [elem for elem in token_overlap if elem[0] >= 0.3]

        tf_idf = sentence_similarity_dict['tfidf']
        tf_idf = [elem for elem in tf_idf if elem[0] >= 0.3]

        greedy_ne_tiling = sentence_similarity_dict['greedynetiling']
        greedy_ne_tiling = [[0.35, elem[1], elem[2]] for elem in greedy_ne_tiling if len(elem[0]) > 0]

        greedy_ne_syn_tiling = sentence_similarity_dict['greedynesyntiling']
        greedy_ne_syn_tiling = [[0.35, elem[1], elem[2]] for elem in greedy_ne_syn_tiling if len(elem[0]) > 0]

        greedy_ne_tiling_man = sentence_similarity_dict['greedynetilingman']
        greedy_ne_tiling_man = [[0.35, elem[1], elem[2]] for elem in greedy_ne_tiling_man if len(elem[0]) > 0]

        greedy_ne_syn_tiling_man = sentence_similarity_dict['greedynesyntilingman']
        greedy_ne_syn_tiling_man = [[0.35, elem[1], elem[2]] for elem in greedy_ne_syn_tiling_man if len(elem[0]) > 0]

        longest_common_ne_sequence = sentence_similarity_dict['lcnes']
        longest_common_ne_sequence = [[0.35, elem[1], elem[2]] for elem in longest_common_ne_sequence if elem[0] >= 2]

        longest_common_ne_syn_sequence = sentence_similarity_dict['lcnesyn']
        longest_common_ne_syn_sequence = [[0.35, elem[1], elem[2]] for elem in longest_common_ne_syn_sequence if elem[0] >= 2]

        longest_common_ne_sequence_man = sentence_similarity_dict['lcnesman']
        longest_common_ne_sequence_man = [[0.35, elem[1], elem[2]] for elem in longest_common_ne_sequence_man if elem[0] >= 2]

        longest_common_ne_syn_sequence_man = sentence_similarity_dict['lcnesynman']
        longest_common_ne_syn_sequence_man = [[0.35, elem[1], elem[2]] for elem in longest_common_ne_syn_sequence_man if
                                          elem[0] >= 2]

        ne_coupling = sentence_similarity_dict['necoupling']
        ne_coupling = [[0.35, elem[1], elem[2]] for elem in ne_coupling if elem[0] >= 2]

        ne_syn_coupling = sentence_similarity_dict['nesyncoupling']
        ne_syn_coupling = [[0.35, elem[1], elem[2]] for elem in ne_syn_coupling if elem[0] >= 2]

        ne_coupling_man = sentence_similarity_dict['necouplingman']
        ne_coupling_man = [[0.35, elem[1], elem[2]] for elem in ne_coupling_man if elem[0] >= 2]

        ne_syn_coupling_man = sentence_similarity_dict['nesyncouplingman']
        ne_syn_coupling_man = [[0.35, elem[1], elem[2]] for elem in ne_syn_coupling_man if elem[0] >= 2]

        ne_overlap = sentence_similarity_dict['neoverlap']
        ne_overlap = [[0.35, elem[1], elem[2]] for elem in ne_overlap if elem[0] == 1.0]

        ne_syn_overlap = sentence_similarity_dict['nesynoverlap']
        ne_syn_overlap = [[0.35, elem[1], elem[2]] for elem in ne_syn_overlap if elem[0] == 1.0]

        ne_overlap_man = sentence_similarity_dict['neoverlapman']
        ne_overlap_man = [[0.35, elem[1], elem[2]] for elem in ne_overlap_man if elem[0] == 1.0]

        ne_syn_overlap_man = sentence_similarity_dict['neoverlapman']
        ne_syn_overlap_man = [[0.35, elem[1], elem[2]] for elem in ne_syn_overlap_man if elem[0] == 1.0]

        parameters = {'CPMinval': 0.8, 'NearCPMinval': 0.4, 'ParaphraseMinval': 0.35}

        score_list = [('token overlap', self.determine_type(token_overlap, parameters)),
                      ('synonym overlap', self.determine_type(synonym_overlap, parameters)),
                      ('edit distance', self.determine_type(edit_distance, parameters)),
                      ('tf idf', self.determine_type(tf_idf, parameters)),
                      ('greedy ne tiling', self.determine_type(greedy_ne_tiling, parameters)),
                      ('greedy ne syn tiling', self.determine_type(greedy_ne_syn_tiling, parameters)),
                      ('greedy ne tiling man', self.determine_type(greedy_ne_tiling_man, parameters)),
                      ('greedy ne syn tiling man', self.determine_type(greedy_ne_syn_tiling_man, parameters)),
                      ('longest common ne sequence', self.determine_type(longest_common_ne_sequence, parameters)),
                      ('longest common ne syn sequence', self.determine_type(longest_common_ne_syn_sequence, parameters)),
                      ('longest common ne sequence man', self.determine_type(longest_common_ne_sequence_man, parameters)),
                      ('longest common ne syn sequence man',
                       self.determine_type(longest_common_ne_syn_sequence_man, parameters)),
                      ('ne coupling', self.determine_type(ne_coupling, parameters)),
                      ('ne syn coupling', self.determine_type(ne_syn_coupling, parameters)),
                      ('ne coupling man', self.determine_type(ne_coupling_man, parameters)),
                      ('ne syn coupling man', self.determine_type(ne_syn_coupling_man, parameters)),
                      ('ne overlap', self.determine_type(ne_overlap, parameters)),
                      ('ne syn overlap', self.determine_type(ne_syn_overlap, parameters)),
                      ('ne overlap man', self.determine_type(ne_overlap_man, parameters)),
                      ('ne syn overlap man', self.determine_type(ne_syn_overlap_man, parameters))]

        return score_list

    def score(self):
        """
        Determine which score list to return
        :return: Score list on article level if CPFA, else score list on sentence level
        """

        score_list = []
        for topic in self.sim_list:

            sentence_segment_score = self.sentence_segment_score(topic[0])
            article_segment_score = self.article_segment_score(topic[1])

            # print(article_segment_score)

            # if article_segment_score[0][1][0]['reuse'] in ['CPFA', 'NearCPFA']:
            if len(article_segment_score[0][1]) > 0:
                score_list.append(article_segment_score)
            else:
                score_list.append(sentence_segment_score)
                # score_list.append(article_segment_score)

        return score_list
