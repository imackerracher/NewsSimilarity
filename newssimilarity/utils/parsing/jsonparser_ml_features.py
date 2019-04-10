import json
import numpy as np
from newssimilarity.utils.parsing.parser import Parser
import json


class JsonParserMLFeatures:

    def __init__(self, path):
        self.path = path

    def parse(self):

        with open(self.path, 'r') as f:
            featureset = json.loads(f.read())

        #if word embeddings have to be converted again to numpy array:
        # np.array(list)

        return featureset