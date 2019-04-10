"""
Segments article into sentences
"""
import re

from nltk.tokenize import sent_tokenize

from newssimilarity.model.segment import Segment
from newssimilarity.utils.segmentation.segmenter import Segmenter

class SentenceSegmenter(Segmenter):
    def __init__(self, article):
        self.article = article

    def segment(self):
        """
        Segment into a list of sentences
        :return: List of sentences as segment objects
        """

        head_segments = sent_tokenize(self.article.head)
        lead_segments = sent_tokenize(self.article.lead)
        body_segments = sent_tokenize(self.article.body)

        segments = [head_segments, lead_segments, body_segments]

        segment_list = []
        start_pos = 0
        for i, part_segments in enumerate(segments):
            for segment in part_segments:
                # usually only 1 sentence in sentences. mainly for case: "example text." \n More example text
                sentences = segment.split('\n')
                for sentence in sentences:
                    if len(sentence) > 3:
                        end_pos = start_pos + len(re.sub(r'\s', '', sentence))
                        # end_pos = start_pos + len(segment)
                        segment_list.append(
                            Segment('sentence', start_pos, end_pos, sentence.replace('&quot;', '\"'), [],
                                    ['head', 'lead', 'body'][i]))
                        start_pos = end_pos

            #sentence_segment_list = Segmenter.process(self, segment_list, self.article)
        sentence_segment_list = Segmenter.process(self, segment_list, self.article)

        return sentence_segment_list
