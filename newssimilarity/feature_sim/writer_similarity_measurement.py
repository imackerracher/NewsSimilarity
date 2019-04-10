from newssimilarity.feature_sim.feature_similarity_measurement import FeatureSimMeasurement
from newssimilarity.utils.sim.wikidata_handler import WikidataHandler


class WriterSimilarityMeasurement(FeatureSimMeasurement):


    def calculate_similarity(self):
        """
        Check wether two articles share an author
        Wikidata is checked for different names of the same writer.
        :param source_article: Source article as article object
        :param target_article: Target article as article object
        :return: True if shared author, False otherwise
        """

        # used to disambiguate named entities
        wikidata_handler = WikidataHandler()
        try:
            writer_source = self.source_article.writers[0].lower()
            wsd = set([ne for writer in writer_source for ne in wikidata_handler.get_named_entities(writer)])
            writer_target = self.target_article.writers[0].lower()
            wtd = set([ne for writer in writer_target for ne in wikidata_handler.get_named_entities(writer)])
            return True if wsd.intersection(wtd) else False
        except:
            return False


