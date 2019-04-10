"""
This class finds all the annotations in the articles and adds the start and end position to them.
"""

from newssimilarity.model.annotation import Annotation
import re


class AnnotationReturner:
    def __init__(self, topics):
        """
        :param topics: Several topics in list
        """
        self.topics = topics

    def get_annotations(self, article):
        """
        Find all the annotations in the article and return them as a list. Includes start and end position.
        :param article: The article object
        :return: List containing all the annotations in the article
        """

        tag = 'Information'
        tmp = re.findall('<' + tag + '.*?</' + tag + '>', article.raw_article, re.DOTALL)

        text = ''
        for phrase in tmp:
            tag_line = re.search('<.*?>', phrase).group().split(' ')
            tag_name = tag_line[2].split('=')[0]
            # if tag_name == 'head' or tag_name == 'lead' or tag_name == 'body':
            if tag_name == 'head' or tag_name == 'lead' or tag_name == 'body':
                tag_body = re.sub('</?Information.*?>', '', phrase)
                tag_body = re.sub('&quot;', '\"', tag_body)
                tag_body = re.sub('&apos;', '', tag_body)
                text = text + ' ' + tag_body  # .replace('&quot;', '\"')

        tags = set(re.findall('(?<=<)[a-zA-Z]*?(?= )', text))

        annotations = []
        for tag in tags:
            tmp = re.findall('<' + tag + '.*?</' + tag + '>', text, re.DOTALL)
            for annotation in tmp:
                annotations.append(annotation)

        annotation_list = []
        text_no_space = re.sub(r'\s', '', text)
        for annotation in annotations:
            # tag_line = ''.join(re.search(r'<.*?>', annotation).group().split(' '))


            index_raw = text_no_space.index(re.sub(r'\s', '', annotation))  # start index of the raw annotation
            preceding_txt = text_no_space[:index_raw]
            # tags = re.findall('<.*?>', preceding_txt)        #other annotation tags that occur before in the text
            preceding_txt_no_anns = re.sub(r'<.*?>', '', preceding_txt)  # preceding annotation tags removed
            start_pos = len(preceding_txt_no_anns)
            annotation_no_tag = re.sub(r'<.*?>', '', annotation)  # tag removed
            annotation_no_tag_no_space = re.sub(r'\s', '', annotation_no_tag)  # spaces removed
            # end_pos = start_pos + len(annotation_no_tag_no_space)
            end_pos = start_pos + sum(
                [len(tok) for tok in annotation_no_tag_no_space.split(' ')])  # other line didn't work in CarBomb_3

            tag_line = re.search(r'<.*?>', annotation).group().split(' ')
            if len(tag_line) == 4:
                tag = tag_line[0][1:]
                phrase_type = tag_line[2][6:-1]
                phrase_id = tag_line[3][11:-2]
                annotation_list.append(
                    Annotation(tag, phrase_id, None, None, phrase_type, annotation_no_tag, start_pos, end_pos))
            else:
                tag = tag_line[0][1:]
                phrase_id = tag_line[2][11:-1]
                source = tag_line[3][8:-1]
                source_id = tag_line[4][11:-1]
                phrase_type = tag_line[5][6:-2]

                annotation_list.append(
                    Annotation(tag, phrase_id, source, source_id, phrase_type, annotation_no_tag, start_pos, end_pos))

        return annotation_list

    def pair(self):
        """
        Pair the annotations (i.e. create tuple out of source and target annotation)
        :return: List with the paired annotations
        """

        annotations = []

        for topic in self.topics:
            source_annotations = self.get_annotations(topic[0])
            target_annotations = self.get_annotations(topic[1])

            source_annotations = sorted(source_annotations, key=lambda annotation: int(annotation.phrase_id))
            target_annotations = sorted(target_annotations, key=lambda annotation: int(annotation.source_id))

            pairs = zip(range(0, len(source_annotations)), source_annotations, target_annotations)

            annotations.append(list(pairs))

        return annotations
