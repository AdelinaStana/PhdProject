import csv
import re

import networkx as nx
import numpy as np


def extract_number_from_path(file_path):
    match = re.search(r'\d+', file_path)
    if match:
        return int(match.group())
    else:
        return 10


class DependenciesBuilder:
    def __init__(self, csv_file_sd, csv_file_ld, original_dependencies=None):
        self.name_index_map = {}
        self.index_name_map = {}
        self.matrix = np.array([], dtype=float)
        self.graph = nx.Graph()
        self.n = 0

        entities_set, data = self.read_csv_dependencies(csv_file_sd, csv_file_ld)

        if original_dependencies:
            self.repopulate_matrix(data, original_dependencies)
        else:
            self.populate_matrix(entities_set, data)

    def read_csv_dependencies(self, csv_file_sd, csv_file_ld):
        # read file
        entities_set = set()
        data = []

        if csv_file_sd:
            try:
                with open(csv_file_sd, newline='') as file1:
                    reader = csv.reader(file1)
                    for row in reader:
                        entity1 = row[0].strip()
                        entity2 = row[1].strip()
                        value = int(row[2].strip())
                        data.append([entity1, entity2, value])

                        entities_set.add(entity1)
                        entities_set.add(entity2)

            except BaseException as e:
                print(f"Error at reading csv file: {csv_file_sd}")
                print(e)
                return

        if csv_file_ld:
            try:
                with open(csv_file_ld, newline='') as file1:
                    reader = csv.reader(file1)
                    for row in reader:
                        entity1 = row[0].strip()
                        entity2 = row[1].strip()
                        value = int(row[2].strip())
                        data.append([entity1, entity2, value])

                        entities_set.add(entity1)
                        entities_set.add(entity2)

            except BaseException as e:
                print(f"Error at reading csv file: {csv_file_ld}")
                print(e)
                return

        entities_set = sorted(entities_set)

        return entities_set, data

    def populate_matrix(self, entities_set, data):
        self.n = len(entities_set)

        i = 0
        for name in entities_set:
            if name not in self.name_index_map:
                self.name_index_map[name] = i
                self.index_name_map[i] = name
                i += 1

        self.matrix = np.array([[0]*self.n]*self.n)
        self.graph.clear()

        for dependency in data:
            index_a = self.name_index_map[dependency[0]]
            index_b = self.name_index_map[dependency[1]]

            self.matrix[index_a][index_b] += dependency[2]
            self.graph.add_edge(dependency[0], dependency[1],  weight=dependency[2])

    def repopulate_matrix(self, data, original_dependencies):
        self.index_name_map = original_dependencies.index_name_map
        self.name_index_map = original_dependencies.name_index_map
        self.n = original_dependencies.n

        self.matrix = np.array([[0] * self.n] * self.n)
        self.graph.clear()

        for dependency in data:
            if dependency[0] in self.name_index_map.keys() and dependency[1] in self.name_index_map.keys():
                index_a = self.name_index_map[dependency[0]]
                index_b = self.name_index_map[dependency[1]]

                self.matrix[index_a][index_b] += dependency[2]
                self.graph.add_edge(dependency[0], dependency[1], weight=dependency[2])


