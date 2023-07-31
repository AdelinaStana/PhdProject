import csv
from itertools import chain


class DependenciesMapper:
    def __init__(self, file1, file2):
        self.id_dict = {}
        self.file1 = file1
        self.file2 = file2
        self.nodes = {}

        with open(file1, newline='') as file1:
            reader = csv.reader(file1)
            self.data1 = [[row[0].strip(), row[1].strip()] for row in reader]

        with open(file2, newline='') as file2:
            reader = csv.reader(file2)
            self.data2 = [[row[0].strip(), row[1].strip()] for row in reader]

        self.create_map()

    def create_map(self):
        all_data = set(chain(*self.data1)).union(set(chain(*self.data2)))

        self.id_dict = {}
        id_counter = 1

        for name in all_data:
            if name not in self.id_dict:
                self.id_dict[name] = id_counter
                self.nodes[id_counter] = name
                id_counter += 1

        with open('map.txt', 'w') as output_file:
            for name, id_num in self.id_dict.items():
                output_file.write(name + ' - ' + str(id_num) + '\n')

    def convert(self):
        converted_file1_name = self.file1.replace(".csv", "_ids.csv")
        converted_file2_name = self.file2.replace(".csv", "_ids.csv")
        data1_sorted = []
        data2_sorted = []

        for row in self.data1:
            data1_sorted.append([self.id_dict[row[0]], self.id_dict[row[1]]])

        data1_sorted = sorted(data1_sorted, key=lambda row: int(row[0]))

        with open(converted_file1_name, 'w', newline='') as output_file1:
            writer1 = csv.writer(output_file1)
            for row in data1_sorted:
                writer1.writerow([row[0], row[1]])

        for row in self.data2:
            data2_sorted.append([self.id_dict[row[0]], self.id_dict[row[1]]])

        data2_sorted = sorted(data2_sorted, key=lambda row: int(row[0]))

        with open(converted_file2_name, 'w', newline='') as output_file2:
            writer2 = csv.writer(output_file2)
            for row in data2_sorted:
                writer2.writerow([row[0], row[1]])

        return converted_file1_name, converted_file2_name
