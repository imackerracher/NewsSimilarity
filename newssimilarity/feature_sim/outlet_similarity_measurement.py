from newssimilarity.feature_sim.feature_similarity_measurement import FeatureSimMeasurement
from newssimilarity.utils.sim.wikidata_handler import WikidataHandler


class OutletSimilarityMeasurement(FeatureSimMeasurement):
    def calculate_similarity(self):
        """
        Check wether two articles have the same publishing source.
        Wikidata is checked for different names of the same outlet.
        E.g. "New York Times" vs "The New York Times".
        :param source_article: Source article as article object
        :param target_article: Target article as article object
        :return: True if same publishing source, False otherwise
        """

        wikidata_handler = WikidataHandler()
        try:
            source_publisher_disambiguated = set(wikidata_handler.get_named_entities(self.source_article.publisher))
            target_publisher_disambiguated = set(wikidata_handler.get_named_entities(self.source_article.publisher))
            return True if source_publisher_disambiguated.intersection(target_publisher_disambiguated) else False
        except:
            return False

