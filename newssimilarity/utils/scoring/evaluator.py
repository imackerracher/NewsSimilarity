"""
takes the annotations and the calculated similarity between 2 articles, and determines a score for all the different
reuse types per method.
"""
class Evaluator:
    def __init__(self, annotations_list, score_list):
        """
        :param annotations_list: List of lists per topic
        :param score_list: List of scores per topic
        """
        self.annotations_list = annotations_list
        self.score_list = score_list

    def disambiguate(self, reuse):
        """
        In case there are inconsistencies in the tagged annotations
        :param reuse: The tag in question
        :return: Uniform tag
        """
        if reuse in ['CPSen', 'CPSenSec', 'CPSEN', 'CopyPasteSEN', 'CopyPasteSen']:
            return 'CPSen'
        if reuse in ['CPPar', 'CPParSec', 'CPPAR', 'CopyPastePAR', 'CopyPastePar', 'CopyPastePARF', 'CopyPastePARS',
                     'CopyPastePART']:
            return 'CPPar'
        if reuse in ['CPFA', 'CopyPasteFA']:
            return 'CPFA'
        if reuse in ['NearCPSen', 'NearCPSenSec', 'NearCPSEN', 'NearCPsen']:
            return 'NearCPSen'
        if reuse in ['NearCPPar', 'NearCPPAR', 'NearCPpar']:
            return 'NearCPPar'
        if reuse in ['NearCPFA']:
            return 'NearCPFA'
        if reuse in ['ParaphraseSen', 'ParaphraseSEN']:
            return 'ParaphraseSen'
        if reuse in ['ParaphrasePar', 'ParaphrasePAR']:
            return 'ParaphrasePar'

    def match(self, method, annotations):
        """
        This method matches the annotations with the segments the system found for each reuse type
        :param method: The current method that is being matched (e.g. token overlap)
        :param annotations: All the annotations from all the topics, to see which ones where found by the method
        :return:
        """

        # all the segments that were found
        segments = method[1]
        # the name of the current method
        name = method[0]
        # tuples with start and end position for all the segments that were found
        to_st_end = [[segments.index(dic), dic['segments'][0][0].start_pos, dic['segments'][0][-1].end_pos,
                      dic['segments'][1][0].start_pos, dic['segments'][1][-1].end_pos] for dic in segments]
        # tuples with start and end position for all the annotations
        an_st_end = [[pa[1].start_pos, pa[1].end_pos, pa[2].start_pos, pa[2].end_pos] for pa in annotations]

        an_st_end_tmp = an_st_end
        full_match_ids = []
        j = []
        for t in to_st_end:
            if t[1:] in an_st_end_tmp:
                index = an_st_end.index(t[1:])
                full_match_ids.append((t[0], index))
                index_tmp = an_st_end_tmp.index(t[1:])
                an_st_end_tmp = an_st_end_tmp[:index_tmp] + an_st_end_tmp[index_tmp + 1:]

            else:
                j.append(t)

        # only the segments ids
        full_match_seg_ids = [tup[0] for tup in full_match_ids]
        # only the paired annotation ids
        full_match_ann_ids = [tup[1] for tup in full_match_ids]


        full_match_segments = [dic for dic in segments if segments.index(dic) in full_match_seg_ids]
        full_match_annotations = [pa for pa in annotations if pa[0] in full_match_ann_ids]

        remaining_segments = [dic for dic in segments if dic not in full_match_segments]

        # annotations that weren't matched completely by a segment
        remaining_annotations = [pa for pa in annotations if pa not in full_match_annotations]

        def count(tag_name):
            """
            Determine how many true positives, false negatives and false positives were found for each reuse type by
            the current method and how many relevant elements there where in the annotations for the respective reuse
            type and method.
            :param tag_name: The tag of the reuse type (e.g. copy paste sentence)
            :return: tuple containing all the relevant information
            """
            true_positives = sum(
                [1 for pa in full_match_annotations if self.disambiguate(pa[1].tag) == self.disambiguate(tag_name)])
            relevant_elements = sum(
                [1 for pa in annotations if self.disambiguate(pa[1].tag) == self.disambiguate(tag_name)])
            false_pos = sum(
                [1 for dic in remaining_segments if self.disambiguate(dic['reuse']) == self.disambiguate(tag_name)])
            false_neg = sum([1 for pa in remaining_annotations if
                             self.disambiguate(pa[1].tag) == self.disambiguate(tag_name)])  # Not found

            return (true_positives, relevant_elements, false_pos, false_neg)

        cpfa = count('CPFA')
        cppar = count('CPPar')
        cpsen = count('CPSen')
        ncpfa = count('NearCPFA')
        ncppar = count('NearCPPar')
        ncpsen = count('NearCPSen')
        paraphrase_par = count('ParaphrasePar')
        paraphrase_sen = count('ParaphraseSen')

        # for each topic and method a dictionary containing all the scores is returned
        method_dict = {'method': name,
                       'total': (len(full_match_annotations), len(annotations), len(remaining_segments),
                                 len(remaining_annotations)),
                       # true pos, relevant elements, false pos, false neg (not found)
                       'cpfa': cpfa,
                       'cppar': cppar,
                       'cpsen': cpsen,
                       'ncpfa': ncpfa,
                       'ncppar': ncppar,
                       'ncpsen': ncpsen,
                       'paraphrase_par': paraphrase_par,
                       'paraphrase_sen': paraphrase_sen}

        return method_dict

    def concatenate_results(self, evaluation_list):
        """
        group all the evaluation lists, by the similarity method (e.g. token overlap)
        :param evaluation_list: List of dictionaries with all the evaluation scores for the different methods
        :return: List with a list per method and f-measures for each reuse type for that method
        """

        methods = ['token overlap', 'synonym overlap', 'edit distance', 'tf idf', 'source comparison', 'writer comparison',
                   'ne overlap', 'ne syn overlap', 'ne overlap man', 'ne syn overlap man',
                   'greedy ne tiling', 'greedy ne syn tiling', 'greedy ne tiling man', 'greedy ne syn tiling man',
                   'longest common ne sequence', 'longest common ne syn sequence',
                   'longest common ne sequence man', 'longest common ne syn sequence man',
                   'ne coupling', 'ne syn coupling', 'ne coupling man', 'ne syn coupling man']
        # add empty list if new method is added in methods list
        #grouped = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
        grouped = [[] for _ in methods]

        number_of_topics = len(evaluation_list)


        for topic in evaluation_list:
            for dic in topic:
                grouped[methods.index(dic['method'])].append(dic)
                #print(dic)

        #for m in grouped:
        #    print(m)

        concat_eval_list = []

        for method in grouped:

            def count(type):
                """
                Determine the f-measure for each reuse type per method
                :param type: The reuse type (e.g. copy paste sentence)
                :return: f-measure
                """

                true_positives = sum([dic[type][0] for dic in method])
                relevant_items = sum([dic[type][1] for dic in method])
                false_pos = sum([dic[type][2] for dic in method])
                false_neg = sum([dic[type][3] for dic in method])


                # if relevant_items > 0:
                #    return (true_positives/relevant_items, false_pos, false_neg)
                # else:
                #    return (true_positives, relevant_items, false_pos, false_neg)
                return (true_positives, relevant_items, false_pos, false_neg)

            # for methods that aren't used to find cpfa and ncpfa
            try:
                method_name = method[0]['method']
            except:
                pass

            if method_name in methods[7:]:
                full_article_count = count('cpfa')[1] + count('ncpfa')[1]
                total_true_positive = count('total')[0]
                total_relevant_items = count('total')[1] - full_article_count
                total_false_positive = count('total')[2]
                total_false_negative = count('total')[3] - full_article_count
                concat_eval_list.append([method_name,
                                         (total_true_positive, total_relevant_items,
                                          total_false_positive, total_false_negative),
                                         (0, 0, 0, 0),
                                         count('cppar'),
                                         count('cpsen'),
                                         (0, 0, 0, 0),
                                         count('ncppar'),
                                         count('ncpsen'),
                                         count('paraphrase_par'),
                                         count('paraphrase_sen')
                                         ])

            elif method_name in ['source comparison', 'writer comparison']:
                concat_eval_list.append([method_name,
                                        (count('total')[0], number_of_topics, 0, number_of_topics - count('total')[0]),
                                        (0, 0, 0, 0),
                                        (0, 0, 0, 0),
                                        (0, 0, 0, 0),
                                        (0, 0, 0, 0),
                                        (0, 0, 0, 0),
                                        (0, 0, 0, 0),
                                        (0, 0, 0, 0),
                                        (0, 0, 0, 0)])



            else:
                concat_eval_list.append([method_name,
                                         count('total'),
                                         count('cpfa'),
                                         count('cppar'),
                                         count('cpsen'),
                                         count('ncpfa'),
                                         count('ncppar'),
                                         count('ncpsen'),
                                         count('paraphrase_par'),
                                         count('paraphrase_sen')
                                         ])

        return concat_eval_list


    def f_meausure(self, concat_evaluation_list):
        """
        Determine the f-measure for each type in the evaluation list
        :param evaluation_list: List with tuples containing the relevant information to determine f-measure for each type
        :return: List with f-measure
        """

        f_measure_list = []
        for method in concat_evaluation_list:
            method_list = []
            for type in method[1:]:
                true_positives = type[0]
                relevant_items = type[1]
                false_positives = type[2]

                if (true_positives + false_positives) == 0:
                    method_list.append(type)
                else:
                    precision = true_positives / (true_positives + false_positives)
                    recall = true_positives / relevant_items

                    if precision == 0:
                        method_list.append(type)
                    else:
                        f_measure = 2 * ((precision*recall) /(precision+recall))
                        f_measure_rounded = round(f_measure, 2)
                        method_list.append(f_measure_rounded)
            f_measure_list.append([method[0]] + method_list)

        return f_measure_list



    def evaluate(self):
        """
        Controlls the evaluation
        :return: A list with the evaluation scores for each reuse type per method
        """

        def iterate_sim_types(annotations, segment_scores):
            topic_evalutation_list = []
            for sim_type in segment_scores:

                if len(sim_type[1]) == 1 and sim_type[1][0]['reuse'] in ['CPFA', 'NearCPFA']:  # article level
                    new_source_ann = annotations[0][1]
                    new_source_ann.start_pos = 0
                    new_target_ann = annotations[0][2]
                    new_target_ann.start_pos = 0
                    new_pair = [(0, new_source_ann, new_target_ann)]
                    topic_evalutation_list.append(self.match(sim_type, new_pair))
                else:
                    topic_evalutation_list.append(self.match(sim_type, annotations))

            return topic_evalutation_list

        evaluation_list = []


        for i in zip(self.annotations_list, self.score_list):
            evaluation_list.append(iterate_sim_types(i[0], i[1]))

        concat_list = self.concatenate_results(evaluation_list)
        f_measure_list = self.f_meausure(concat_list)



        return f_measure_list

