from newssimilarity.model.feature_instances.feature_instance import FeatureInstance


class WriterFeatureInstance(FeatureInstance):
    def get_feature_instance(self):
        return self.content
