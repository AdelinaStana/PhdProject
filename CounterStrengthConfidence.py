import statistics

from Graph import Graph
from threading import Thread
import time
from CounterStrength import CounterStrength


class CounterStrengthConfidence(CounterStrength):
    def __init__(self, structure_manager, output_dir):
        CounterStrength.__init__(self, structure_manager, output_dir)

    def start_count(self):
        start = time.time()
        number_of_steps = 10

        for i in range(0, number_of_steps + 2):
            self.results_count.append(-1)

        threads = []

        try:
            t_code = Thread(target=self.count_code_links, args=())
            threads.append(t_code)
            t_git = Thread(target=self.count_git_links, args=(2, 1))
            threads.append(t_git)

            for i in range(1, number_of_steps + 1):
                t_strength = Thread(target=self.count_strength, args=(i + 1, i*10))
                threads.append(t_strength)

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

    def count_strength(self, pos, threshold):
        entity_class_id_dict = {}
        max_occ_set = set()

        for classItem in self.structure_manager.get_class_list():
            entity_class_id_dict[classItem.unique_id] = classItem
            values = classItem.git_links_below_commit_size_threshold.values()
            max_occ = 0
            if values:
                max_occ = max(values)
            max_occ_set.add(max_occ)

        mean = statistics.mean(list(max_occ_set))
        print(mean)

        g = Graph(self.working_dir + "\\" + self.name + "_git_strength_"+str(threshold), self.structure_manager)
        try:
            for classItem in self.structure_manager.get_class_list():
                entity1 = classItem
                entity1_id = classItem.unique_id

                related_list = classItem.get_filtered_commit_size_occurrences(1)
                for entity2_id in related_list:
                    entity2 = entity_class_id_dict[entity2_id]

                    nr_of_commits_together1 = entity1.get_nr_of_occ_with(entity2_id)  # commits involving A and B
                    nr_of_total_commits1 = entity1.commits_count  # total nr of commits involving A

                    nr_of_commits_together2 = entity2.get_nr_of_occ_with(entity1_id)  # commits involving A and B
                    nr_of_total_commits2 = entity2.commits_count  # total nr of commits involving B

                    confidence1 = nr_of_total_commits1/mean
                    confidence2 = nr_of_total_commits2/mean

                    update_percentage1 = ((100 * nr_of_commits_together1) / nr_of_total_commits1) * confidence1
                    update_percentage2 = ((100 * nr_of_commits_together2) / nr_of_total_commits2) * confidence2

                    if update_percentage1 >= threshold and update_percentage2 >= threshold:
                        g.add_edge(classItem.unique_id, entity2_id)

        except BaseException as e:
            print("Exception: "+str(e))

        self.results_count[pos] = g.number_of_edges()
        g.export_names_to_csv()
        print("Count git links with strength "+str(threshold)+"% ...")