from counters.Graph import Graph
from threading import Thread
import time


class CounterCommit:
    def __init__(self, structure_manager, output_dir):
        self.results_count = []
        self.output_dir = output_dir
        for i in range(0, 34):
            self.results_count.append(-1)
        self.structure_manager = structure_manager
        self.working_dir = self.structure_manager.working_dir.replace("~Temp", "~results")

    def start_count(self):
        start = time.time()
        threads = []

        try:
            t_code = Thread(target=self.count_code_links, args=())
            t_git5 = Thread(target=self.count_git5_links, args=(1,))
            t_git10 = Thread(target=self.count_git10_links, args=(5,))
            t_git20 = Thread(target=self.count_git20_links, args=(9,))
            t_total = Thread(target=self.count_git_total_links, args=(13,))
            t_code_git5 = Thread(target=self.count_code_and_git5_links, args=(17,))
            t_code_git10 = Thread(target=self.count_code_and_git10_links, args=(21,))
            t_code_git20 = Thread(target=self.count_code_and_git20_links, args=(25,))
            t_code_git_total = Thread(target=self.count_code_and_total_git_links, args=(29,))

            t_code.start()
            t_git5.start()
            t_git10.start()
            t_git20.start()
            t_total.start()
            t_code_git5.start()
            t_code_git10.start()
            t_code_git20.start()
            t_code_git_total.start()

            threads.append(t_code)
            threads.append(t_git5)
            threads.append(t_git10)
            threads.append(t_git20)
            threads.append(t_total)
            threads.append(t_code_git5)
            threads.append(t_code_git10)
            threads.append(t_code_git20)
            threads.append(t_code_git_total)

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
                related_list = classItem.get_structural_related_links()
                for related in related_list:
                    g.add_edge(classItem.unique_id, related)
        except BaseException as e:
            print(e)
        print("Number of classes: " + str(g.number_of_nodes()))
        self.results_count[0] = g.number_of_nodes()
        self.results_count[1] = g.number_of_edges()

    def count_git5_links(self, pos):
        for occ in range(1, 5):
            g = Graph(self.working_dir+"\\git5_links", self.structure_manager)
            try:
                for class_item in self.structure_manager.get_class_list():
                    git_list = class_item.get_filtered_git_links(occ, 5)
                    for related in git_list:
                        g.add_edge(class_item.unique_id, related)
            except BaseException as e:
                print(e)
            self.results_count[pos+occ] = g.number_of_edges()
        print("Count git5 links...")

    def count_git10_links(self, pos):
        for occ in range(1, 5):
            g = Graph(self.working_dir+"\\git10_links", self.structure_manager)
            try:
                for classItem in self.structure_manager.get_class_list():
                    git_list = classItem.get_filtered_git_links(occ, 10)
                    for related in git_list:
                        g.add_edge(classItem.unique_id, related)
            except BaseException as e:
                print(e)
            self.results_count[pos + occ] = g.number_of_edges()
        print("Count git10 links...")

    def count_git20_links(self, pos):
        for occ in range(1, 5):
            g = Graph(self.working_dir+"\\git20_links", self.structure_manager)
            try:
                for classItem in self.structure_manager.get_class_list():
                    git_list = classItem.get_filtered_git_links(occ, 20)
                    for related in git_list:
                        g.add_edge(classItem.unique_id, related)
            except BaseException as e:
                print(e)
            self.results_count[pos + occ] = g.number_of_edges()
        print("Count git20 links...")

    def count_git_total_links(self, pos):
        for occ in range(1, 5):
            g = Graph(self.working_dir+"\\git_total_links", self.structure_manager)
            try:
                for classItem in self.structure_manager.get_class_list():
                    git_list = classItem.get_filtered_git_links(occ, 1000000)
                    for related in git_list:
                        g.add_edge(classItem.unique_id, related)
            except BaseException as e:
                print(e)
            self.results_count[pos + occ] = g.number_of_edges()
        print("Count git total links...")

    def count_code_and_total_git_links(self, pos):
        for occ in range(1, 5):
            g = Graph(self.working_dir+"\\code_git_total_links", self.structure_manager)
            try:
                for classItem in self.structure_manager.get_class_list():
                    related_list = classItem.get_git_code_overlapping(occ, 100000)
                    for related in related_list:
                        g.add_edge(classItem.unique_id, related)
            except BaseException as e:
                print(e)
            self.results_count[pos + occ] = g.number_of_edges()
        print("Count code and total links...")

    def count_code_and_git5_links(self, pos):
        for occ in range(1, 5):
            g = Graph(self.working_dir+"\\code_git5_total_links", self.structure_manager)
            try:
                for classItem in self.structure_manager.get_class_list():
                    related_list = classItem.get_git_code_overlapping(occ, 5)
                    for related in related_list:
                        g.add_edge(classItem.unique_id, related)
            except BaseException as e:
                print(e)
            self.results_count[pos + occ] = g.number_of_edges()
        print("Count code and git5...")

    def count_code_and_git10_links(self, pos):
        for occ in range(1, 5):
            g = Graph(self.working_dir+"\\code_git10_total_links", self.structure_manager)
            try:
                for classItem in self.structure_manager.get_class_list():
                    related_list = classItem.get_git_code_overlapping(occ, 10)
                    for related in related_list:
                        g.add_edge(classItem.unique_id, related)
            except BaseException as e:
                print(e)
            self.results_count[pos + occ] = g.number_of_edges()
        print("Count code and git10...")

    def count_code_and_git20_links(self, pos):
        for occ in range(1, 5):
            g = Graph(self.working_dir+"\\code_git20_total_links", self.structure_manager)
            try:
                for classItem in self.structure_manager.get_class_list():
                    related_list = classItem.get_git_code_overlapping(occ, 20)
                    for related in related_list:
                        g.add_edge(classItem.unique_id, related)
            except BaseException as e:
                print(e)
            self.results_count[pos + occ] = g.number_of_edges()
        print("Count code and git20...")