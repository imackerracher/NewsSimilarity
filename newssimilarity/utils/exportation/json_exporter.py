import json
import os
from newssimilarity.definitions import vand_folder_path, slash

from newssimilarity.utils.exportation.exporter import Exporter


class JsonExporter(Exporter):
    def __init__(self, similarity_dict):
        self.similarity_dict = similarity_dict

    def export(self):
        """
        Export the scores to a json file
        """

        #data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/data/Similarity/'
        data_path = slash.join(vand_folder_path + ['sim_matrix.txt'])
        with open(data_path, 'w') as file:
            json.dump(self.similarity_dict, file)



    #def export_as_txt(self):
