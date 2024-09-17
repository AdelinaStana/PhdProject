import csv
import re

import networkx as nx
import numpy as np
import pickle


def extract_number_from_path(file_path):
    match = re.search(r'\d+', file_path)
    if match:
        return int(match.group())
    else:
        return 10


def compute_overall_average(data):
    total_sum = 0
    total_count = 0

    for _, _, value in data:
        total_sum += value
        total_count += 1

    overall_average = total_sum / total_count if total_count > 0 else 0

    return overall_average


class DependenciesBuilder:
    def __init__(self, name, csv_file_sd, csv_file_ld, original_dependencies=None):
        self.name_index_map = {}
        self.index_name_map = {}
        self.matrix = np.array([], dtype=float)
        self.graph = nx.Graph()
        self.n = 0
        self.ld_only = True if csv_file_sd is None else False

        entities_set, data = self.read_csv_dependencies(csv_file_sd, csv_file_ld)
        with open(f'../results/indexing/{name}_index_map.dump', 'rb') as file:
            self.name_index_map = pickle.load(file)

        for key in self.name_index_map.keys():
            value = self.name_index_map[key]
            self.index_name_map[value] = key

        if original_dependencies:
            self.repopulate_matrix(data, original_dependencies)
        else:
            self.populate_matrix(entities_set, data)

    def read_csv_dependencies(self, csv_file_sd, csv_file_ld):
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
                        data.append([entity1, entity2, value*10])

                        entities_set.add(entity1)
                        entities_set.add(entity2)
            except BaseException as e:
                print(f"Error at reading csv file: {csv_file_ld}")
                print(e)
                return

        entities_set = set(sorted(entities_set))

        return entities_set, data

    def populate_name_index_map(self, entities_set):
        i = 0
        self.name_index_map = {}
        self.index_name_map = {}
        for name in entities_set:
            if name not in self.name_index_map:
                self.name_index_map[name] = i
                self.index_name_map[i] = name
                i += 1

    def populate_matrix(self, entities_set, data):
        self.n = len(entities_set)
        if self.ld_only:
            self.populate_name_index_map(entities_set)

        # with open('../results/indexing/gson_index_map.dump', 'wb') as file:
        #     pickle.dump(self.name_index_map, file)

        self.matrix = np.array([[0]*self.n]*self.n)
        self.graph.clear()

        for dependency in data:
            index_a = self.name_index_map[dependency[0]]
            index_b = self.name_index_map[dependency[1]]

            self.matrix[index_a][index_b] += int(dependency[2])

            if self.graph.has_edge(dependency[0], dependency[1]):
                old_weight = self.graph.get_edge_data(dependency[0], dependency[1])['weight']
                new_weight = old_weight+dependency[2]
                self.graph.add_edge(dependency[0], dependency[1], weight=new_weight)
            else:
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

                self.matrix[index_a][index_b] += int(dependency[2])
                self.graph.add_edge(dependency[0], dependency[1], weight=dependency[2])


