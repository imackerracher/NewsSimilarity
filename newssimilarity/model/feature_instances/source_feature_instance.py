from newssimilarity.model.feature_instances.feature_instance import FeatureInstance


class SourceFeatureInstance(FeatureInstance):
    def get_feature_instance(self):
        return self.content
