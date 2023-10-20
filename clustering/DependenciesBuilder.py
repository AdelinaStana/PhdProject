import csv
import re

import networkx as nx
import numpy as np


def extract_number_from_path(file_path):
    match = re.search(r'\d+', file_path)
    if match:
        return int(match.group())
    else:
        return 0


class DependenciesBuilder:
    def __init__(self, csv_file, median=0):
        self.name_index_map = {}
        self.index_name_map = {}
        self.matrix = np.array([])
        self.name_graph = nx.Graph()
        self.n = 0
        self.median = median       # sd median

        self.populate_matrix(csv_file)

    def populate_matrix(self, csv_file):
        # read file
        entities = set()
        data = []

        percent = extract_number_from_path(csv_file)

        try:
            with open(csv_file, newline='') as file1:
                reader = csv.reader(file1)
                for row in reader:
                    entity1 = row[0].strip()
                    entity2 = row[1].strip()
                    value = int(row[2].strip())
                    if len(row) > 3 and row[3]:
                        entity1 = entity1.split('$')[0]     # remove internal classes
                        entity2 = entity2.split('$')[0]
                        data.append([entity1, entity2, value + (self.median * (percent / 100))])
                    else:
                        data.append([entity1, entity2, value])

                    entities.add(entity1)
                    entities.add(entity2)

        except BaseException as e:
            print(f"Error at reading csv file: {csv_file}")
            print(e)
            return
        entities = sorted(entities)
        self.n = len(entities)
        # print(f"ENTITIES COUNT: {self.n}")

        # create dict with mapping between entity and id (index)
        i = 0
        for name in entities:
            if name not in self.name_index_map:
                self.name_index_map[name] = i
                self.index_name_map[i] = name
                i += 1

        #populate matrix
        self.matrix = np.array([[0]*self.n]*self.n)
        for dependency in data:
            index_a = self.name_index_map[dependency[0]]
            index_b = self.name_index_map[dependency[1]]

            self.matrix[index_a][index_b] += dependency[2]
            self.matrix[index_b][index_a] += dependency[2]

            self.name_graph.add_edge(index_a, index_b)

