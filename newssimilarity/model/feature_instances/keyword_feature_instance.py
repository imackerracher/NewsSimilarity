from newssimilarity.model.feature_instances.feature_instance import FeatureInstance


class KeywordFeatureInstance(FeatureInstance):
    def get_feature_instance(self):
        return self.content
