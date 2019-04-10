from newssimilarity.model.features.feature import Feature


class WriterFeature(Feature):
    def get_feature_name(self):
        return self.feature_name
