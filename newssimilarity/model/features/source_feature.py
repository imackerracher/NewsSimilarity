from newssimilarity.model.features.feature import Feature

"""
Feature for source outlet of the article
"""


class SourceFeature(Feature):
    def get_feature_name(self):
        return self.feature_name
