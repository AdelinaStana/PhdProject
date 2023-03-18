from counters.Graph import Graph
from threading import Thread
import time
import os


class CounterOccurrences:
    def __init__(self, structure_manager, output_dir):
        self.results_count = []
        self.output_dir = output_dir
        self.structure_manager = structure_manager
        self.working_dir = self.structure_manager.working_dir.replace("~Temp", "~results")

        dir_name = self.structure_manager.working_dir
        self.name = os.path.basename(dir_name.replace("/~results", ""))

    def start_count(self):
        start = time.time()
        number_of_steps = 20

        for i in range(0, number_of_steps + 2):
            self.results_count.append(-1)

        threads = []

        try:
            t_code = Thread(target=self.count_code_links, args=())
            threads.append(t_code)
            for i in range(1, number_of_steps + 1):
                t_git = Thread(target=self.count_git_links, args=(i + 1, i))
                threads.append(t_git)

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            print(self.results_count)
        except BaseException as e:
            print(e)
        end = time.time()

        elapsed = end - start
        print("Analysis time: " + str(elapsed))

        with open(self.output_dir + '\\results.txt', 'a') as file:
            line = ",".join([str(x) for x in self.results_count])
            file.write(line + "\n")

    def count_code_links(self):
        g = Graph(self.working_dir+"\\code_links", self.structure_manager)
        try:
            for classItem in self.structure_manager.get_class_list():
                g.add_node(classItem.unique_id)
                related_list = classItem.get_structural_related_links()
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

    def count_git_links(self, pos, occ):
        g = Graph(self.working_dir + "\\" + self.name + "_git_links_"+str(occ)+"occ", self.structure_manager)
        try:
            for class_item in self.structure_manager.get_class_list():
                git_list = class_item.get_filtered_commit_size_occurrences(occ)
                for related in git_list:
                    g.add_edge(class_item.unique_id, related)
        except BaseException as e:
            print(e)
        self.results_count[pos] = g.number_of_edges()
        print("Count git links with "+str(occ)+" occ ...")





