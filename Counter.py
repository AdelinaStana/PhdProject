from Graph import Graph
from threading import Thread
import time


class Counter:
    def __init__(self, structure_manager, output_dir):
        self.results_count = []
        self.output_dir = output_dir
        for i in range(0, 6):
            self.results_count.append(-1)
        self.structure_manager = structure_manager
        self.working_dir = self.structure_manager.working_dir.replace("~Temp", "~results")

    def start_count(self):
        start = time.time()
        threads = []

        try:
            t_code = Thread(target=self.count_code_links, args=())
            t_git_1occ = Thread(target=self.count_git_links_1occ, args=(2,))
            t_git_2occ = Thread(target=self.count_git_links_2occ, args=(3,))
            t_git_3occ = Thread(target=self.count_git_links_3occ, args=(4,))
            t_git_4occ = Thread(target=self.count_git_links_4occ, args=(5,))

            t_code.start()
            t_git_1occ.start()
            t_git_2occ.start()
            t_git_3occ.start()
            t_git_4occ.start()

            threads.append(t_code)
            threads.append(t_git_1occ)
            threads.append(t_git_2occ)
            threads.append(t_git_3occ)
            threads.append(t_git_4occ)

            for t in threads:
                t.join()

            print(self.results_count)
        except BaseException as e:
            print(e)
        end = time.time()

        elapsed = end - start
        print("Analysis time: "+str(elapsed))

        with open(self.output_dir+'\\results.txt', 'a') as file:
            line = ",".join([str(x) for x in self.results_count])
            file.write(line + "\n")

    def count_code_links(self):
        g = Graph(self.working_dir+"\\code_links", self.structure_manager)
        try:
            for classItem in self.structure_manager.get_class_list():
                g.add_node(classItem.unique_id)
                related_list = classItem.get_related()
                for related in related_list:
                    g.add_edge(classItem.unique_id, related)
        except BaseException as e:
            print(e)
        nodes = g.number_of_nodes()
        edges = g.number_of_edges()
        print("Number of classes: " + str(nodes))
        print("Number of SD: " + str(edges))
        self.results_count[0] = nodes
        self.results_count[1] = edges

    def count_git_links_1occ(self, pos):
        g = Graph(self.working_dir + "\\git_links_1occ", self.structure_manager)
        try:
            for class_item in self.structure_manager.get_class_list():
                git_list = class_item.get_occurrences_below_threshold(1)
                for related in git_list:
                    g.add_edge(class_item.unique_id, related)
        except BaseException as e:
            print(e)
        self.results_count[pos] = g.number_of_edges()
        print("Count git links with 1 occ ...")

    def count_git_links_2occ(self, pos):
        g = Graph(self.working_dir + "\\git_links_2occ", self.structure_manager)
        try:
            for class_item in self.structure_manager.get_class_list():
                git_list = class_item.get_occurrences_below_threshold(2)
                for related in git_list:
                    g.add_edge(class_item.unique_id, related)
        except BaseException as e:
            print(e)
        self.results_count[pos] = g.number_of_edges()
        print("Count git links with 2 occ ...")

    def count_git_links_3occ(self, pos):
        g = Graph(self.working_dir + "\\git_links_3occ", self.structure_manager)
        try:
            for class_item in self.structure_manager.get_class_list():
                git_list = class_item.get_occurrences_below_threshold(3)
                for related in git_list:
                    g.add_edge(class_item.unique_id, related)
        except BaseException as e:
            print(e)
        self.results_count[pos] = g.number_of_edges()
        print("Count git links with 3 occ ...")

    def count_git_links_4occ(self, pos):
        g = Graph(self.working_dir + "\\git_links_4occ", self.structure_manager)
        try:
            for class_item in self.structure_manager.get_class_list():
                git_list = class_item.get_occurrences_below_threshold(4)
                for related in git_list:
                    g.add_edge(class_item.unique_id, related)
        except BaseException as e:
            print(e)
        self.results_count[pos] = g.number_of_edges()
        print("Count git links with 4 occ ...")

