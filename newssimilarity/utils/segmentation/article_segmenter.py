"""
Creates a segment out of an article
"""

from newssimilarity.model.segment import Segment
from newssimilarity.utils.segmentation.segmenter import Segmenter
import re


class ArticleSegmenter(Segmenter):
    def __init__(self, article):
        self.article = article

    def segment(self):
        """
        :return: Article as segment in list
        """
        text = self.article.head + ' ' + self.article.lead + self.article.body
        end_pos = len(re.sub('\s', '', text))

        # segment_list = [Segment('article', 0, sum([len(tok) for tok in text.split(' ')]), text, [])]
        segment_list = [Segment('article', 0, end_pos, text, [])]
        article_segment_list = Segmenter.process(self, segment_list, self.article)

        return article_segment_list
