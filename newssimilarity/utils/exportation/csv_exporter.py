import csv
from pathlib import Path
from newssimilarity.utils.exportation.exporter import Exporter


class CSVExporter(Exporter):

    def __init__(self):
        self.data_path = data_path = str(Path(__file__).parents[2]) + '/data/Similarity/'

    def evaluation_export(self, evaluation_dict_list, file_name):
        """
        :param evaluation_dict_list: list of dictionaries for all the evaluated annotations
        """
        header = ['ann #', 'source', 'target', 'token overlap', 'synonym overlap', 'edit distance',
                  'greedy ne tiling', 'greedy ne syn tiling', 'longest common ne sequence',
                  'longest common ne syn sequence', 'ne coupling', 'ne syn coupling', 'ne overlap', 'ne syn overlap']
        ann_num = 1
        with open(self.data_path + file_name, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(item for item in header)
            for dic in evaluation_dict_list:
                current_row = []
                current_row.append(ann_num)
                current_row.append(dic['source annotation'].body)
                current_row.append(dic['target annotation'].body)
                current_row.append(dic['token overlap'] if dic['token overlap'] is not None else 'Not found')
                current_row.append(dic['synonym overlap'] if dic['synonym overlap'] is not None else 'Not found')
                current_row.append(dic['edit distance'] if dic['edit distance'] is not None else 'Not found')
                current_row.append(dic['greedy ne tiling'] if dic['greedy ne tiling'] is not None else 'Not found')
                current_row.append(dic['greedy ne syn tiling'] if dic['greedy ne syn tiling'] is not None else 'Not found')
                current_row.append(dic['longest common ne sequence'] if dic['longest common ne sequence'] is not None else 'Not found')
                current_row.append(
                    dic['longest common ne syn sequence'] if dic['longest common ne syn sequence'] is not None else 'Not found')
                current_row.append(dic['ne coupling'] if dic['ne coupling'] is not None else 'Not found')
                current_row.append(dic['ne syn coupling'] if dic['ne syn coupling'] is not None else 'Not found')
                current_row.append(dic['ne overlap'] if dic['ne overlap'] is not None else 'Not found')
                current_row.append(dic['ne syn overlap'] if dic['ne syn overlap'] is not None else 'Not found')
                writer.writerow(item for item in current_row)
                ann_num += 1




    def export(self, evaluation_list, file_name):
        """
        export the number of types of information reuse found for each method, false positives, not found
        :param evaluation_list: List containing all the scores
        :param file_name: Name of the csv file
        """
        header = ['Method','Total', 'CPFA', 'CPPar', 'CPSen', 'NearCPFA', 'NearCPPar',
                  'NearCPSen', 'ParaphrasePar', 'ParaphraseSen']

        with open(self.data_path + file_name, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(elem for elem in header)
            for sub_list in evaluation_list:
                writer.writerow(elem for elem in sub_list)
