import pandas


class Graph:
    def __init__(self, name, structure_manager):
        self.csv_name = name
        self.structure_manager = structure_manager
        self.file_writer = None
        self.create_file_writer_dict()
        self.nodes = set()

    def create_file_writer_dict(self):
        self.file_writer = open(self.csv_name+".csv", 'wt')
        self.file_writer.write("a,b\n")# header

    def add_node(self, name):
        if name not in self.nodes:
            self.nodes.add(name)

    def add_edge(self, x, y):
        if x < y:
            self.file_writer.write(str(x)+","+str(y)+"\n")
        else:
            self.file_writer.write(str(y)+","+str(x)+"\n")

    def write_names_of_edges_csv(self, data):
        class_dict_id = {}

        for class_item in self.structure_manager.get_class_list():
            class_dict_id[class_item.unique_id] = class_item.full_name

        self.file_writer = open(self.csv_name + ".csv", 'wt')
        self.file_writer.write("a,b\n")  # header

        for class_item in data.values:
            try:
                entity1 = class_dict_id[class_item[0]]
                entity2 = class_dict_id[class_item[1]]

                self.file_writer.write(entity1 + "," + entity2 + "\n")
            except KeyError:
                print("Key exception for: "+self.csv_name)
            except BaseException as e:
                print("Graph exception: " + str(e))

        self.file_writer.close()

    def number_of_edges(self):
        self.file_writer.close()
        data = pandas.read_csv(self.csv_name + ".csv")
        data = data.drop_duplicates(subset=['a', 'b'], keep='first')
        self.write_names_of_edges_csv(data)
        return len(data.values)

    def number_of_nodes(self):
        return len(self.nodes)

