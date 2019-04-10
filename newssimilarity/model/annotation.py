"""
Annotation object, as was annotated in test corpus
"""


class Annotation(object):
    def __init__(self, tag, phrase_id, source, source_id, phrase_type, body, start_pos=None, end_pos=None):
        """
        :param tag: The tag given to the annotation (e.g. CopyPasteSen)
        :param phrase_id: The number of the annotation in the article (between 0 and n - 1, n = # of annotations)
        :param source: If the article is a target article this variable will contain the name of the source outlet.
                       If the article is a source article itself, it will be None
        :param source_id: If the article is a target article this variable will contain the phrase_id of the
                          corresponding annotation in the source article. If the article is a source article itself,
                          it will be None
        :param phrase_type: Target phrase or source phrase
        :param body: Contains the text of the annotation
        :param start_pos: The starting position of the annotation in the article
        :param end_pos: The end position of the annotation in the article
        """
        self.tag = tag
        self.phrase_id = phrase_id
        self.source = source
        self.source_id = source_id
        self.phrase_type = phrase_type
        self.body = body
        self.start_pos = start_pos
        self.end_pos = end_pos
