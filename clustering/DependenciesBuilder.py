import csv
from itertools import chain
import numpy as np


class DependenciesBuilder:
    def __init__(self, csv_file):
        self.name_index_map = {}
        self.index_name_map = {}
        self.matrix = np.array([])
        self.array = []
        self.n = 0

        self.populate_matrix(csv_file)

    def populate_matrix(self, csv_file):
        # read file
        entities = set()
        data = []
        try:
            with open(csv_file, newline='') as file1:
                reader = csv.reader(file1)
                for row in reader:
                    data.append([row[0].strip(), row[1].strip(), row[2].strip()])
                    entities.add(row[0].strip())
                    entities.add(row[1].strip())

        except:
                return

        data = data[1:] # remove first row
        self.n = len(entities)
        print(f"ENTITIES COUNT: {self.n}")

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

            self.matrix[index_a][index_b] = 1
            self.matrix[index_b][index_a] = 1

            self.array.append([index_a, index_b, 1])

