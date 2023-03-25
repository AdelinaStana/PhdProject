import statistics


from threading import Thread
import time
from counters.CounterStrength import CounterStrength


class CounterStrengthConfidence(CounterStrength):
    def __init__(self, structure_manager, output_dir):
        CounterStrength.__init__(self, structure_manager, output_dir)

    def start_count(self):
        start = time.time()
        number_of_steps = 10

        for i in range(0, number_of_steps + 3):
            self.results_count.append(-1)

        threads = []

        try:
            t_code = Thread(target=self.count_code_links, args=())
            threads.append(t_code)
            t_git = Thread(target=self.count_git_links, args=(2, 1))
            threads.append(t_git)

            for i in range(0, number_of_steps + 1):
                t_strength = Thread(target=self.count_overlapping_with_code, args=(i + 2, i*10))
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
        max_occ_list = []

        for classItem in self.structure_manager.get_class_list():
            entity_class_id_dict[classItem.unique_id] = classItem
            values = classItem.get_all_occurrence_values(self.structure_manager.commit_threshold)
            max_occ = 0
            if values:
                max_occ = max(values)
            max_occ_list.append(max_occ)

        mean = statistics.mean(max_occ_list)
        print(mean)

        count = [i for i in max_occ_list if i > mean]
        print(len(count))
        csv_name = self.working_dir + "\\" + self.project_name + "_git_strength_" + str(threshold) + ".csv"
        file_writer = open(csv_name, 'wt')
        file_writer.write("a,b,c\n")

        entities_count = 0
        try:
            for classItem in self.structure_manager.get_class_list():
                entity1 = classItem

                related_list = classItem.get_filtered_git_links(1)
                for entity2_id in related_list:
                    entity2 = entity_class_id_dict[entity2_id]

                    freqAUB = entity1.get_nr_of_occ_with(entity2_id)  # commits involving A and B
                    freqA = entity1.commits_count  # total nr of commits involving A

                    strength = freqAUB/mean

                    confidence_percent = ((100 * freqAUB) / freqA) * strength

                    if confidence_percent >= threshold:
                        file_writer.write(entity1.full_name + "," + entity2.full_name + "," +
                                          str(round(confidence_percent, 0)) + "\n")
                        entities_count += 1

        except BaseException as e:
            print("Exception: "+str(e))

        file_writer.close()

        self.results_count[pos] = entities_count
        print("Count git links with strength "+str(threshold)+"% ...")

    def count_overlapping_with_code(self, pos, threshold):
            entity_class_id_dict = {}
            max_occ_list = []

            for classItem in self.structure_manager.get_class_list():
                entity_class_id_dict[classItem.unique_id] = classItem
                values = classItem.get_all_occurrence_values()
                max_occ = 0
                if values:
                    max_occ = max(values)
                max_occ_list.append(max_occ)

            mean = statistics.mean(max_occ_list)
            print(mean)

            csv_name = self.working_dir + "\\" + self.project_name + "_git_strength_overlapp_" + str(threshold) + ".csv"
            file_writer = open(csv_name, 'wt')
            file_writer.write("a,b,c\n")

            entities_count = 0
            try:
                for classItem in self.structure_manager.get_class_list():
                    entity1 = classItem

                    commit_related_list = classItem.get_filtered_git_links(1)
                    code_related_list = classItem.get_structural_related_links()
                    related_list = commit_related_list.intersection(code_related_list)

                    for entity2_id in related_list:
                        entity2 = entity_class_id_dict[entity2_id]

                        freqAUB = entity1.get_nr_of_occ_with(entity2_id)  # commits involving A and B
                        freqA = entity1.commits_count  # total nr of commits involving A

                        strength = freqAUB / mean

                        confidence_percent = ((100 * freqAUB) / freqA) * strength

                        if confidence_percent >= threshold:
                            file_writer.write(entity1.full_name + "," + entity2.full_name + "," +
                                              str(round(confidence_percent, 0)) + "\n")
                            entities_count += 1

            except BaseException as e:
                print("Exception: " + str(e))

            file_writer.close()

            self.results_count[pos] = entities_count
            print("Count git links with strength " + str(threshold) + "% ...")