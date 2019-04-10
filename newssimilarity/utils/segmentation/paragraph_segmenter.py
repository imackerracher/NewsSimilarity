import re
from newssimilarity.model.segment import Segment
from newssimilarity.utils.segmentation.segmenter import Segmenter


class ParagraphSegmenter(Segmenter):
    def __init__(self):
        pass

    def segment(self, article):
        """
        Head is treated as a paragraph as well. Not used, since a paragraph is created by expanding sentences.
        :return: List of paragraphs as segments
        """
        text = article.head + '\n\n' + article.lead + '\n\n' + article.body
        segments = re.split(r'\n{2,}', text)

        segment_list = []
        start_pos = 0
        for segment in segments:
            end_pos = start_pos + len(re.sub(r'\s', '', segment))
            segment_list.append(Segment('paragraph', start_pos, end_pos, segment, []))
            start_pos = end_pos

        paragraph_segment_list = Segmenter.process(self, segment_list, article)
        return paragraph_segment_list
