import pandas


class Statistics:
    """for each link A - B export two columns that contain number of total connections of A and
    number of total connections of B"""

    @staticmethod
    def export_connection_strength(csv_name, structure_manager, occ):
        data = pandas.read_csv(csv_name)
        class_dict_conn = {}

        for class_item in structure_manager.get_class_list():
            connections = class_item.get_occurrences_below_threshold(occ)
            full_name = class_item.full_name
            class_dict_conn[full_name] = len(connections)

        file_writer = open(csv_name.replace(".csv", "_conn.csv"), 'wt')
        file_writer.write("a,b,c,d\n")

        for class_item in data.values:
            try:
                file_writer.write(class_item[0] + "," + class_item[1] + "," + str(class_dict_conn[class_item[0]]) + ","
                                  + str(class_dict_conn[class_item[1]]) + "\n")
            except BaseException as e:
                print(class_item[0] + " - " + class_item[1])
                print(e)

        file_writer.close()

    '''
    Export percentage of commit update between entities A and B.
    * percentage of commits involving A and B from all A commits
    * percentage of commits involving A and B from all B commits
    * note: number of occurrences between A and B = number of commits in which A and B are involved
            
            commits count total  = 8
            commits count A + B  = 6 
            
            occ count total = 140
            occ count A + B = 6
    '''
    @staticmethod
    def filter_commit_percentage(csv_name, structure_manager, threshold):
        data = pandas.read_csv(csv_name)
        id_class_name_dict = {}
        entity_class_id_dict = {}

        for class_item in structure_manager.get_class_list():
            id_class_name_dict[class_item.full_name] = class_item.unique_id
            entity_class_id_dict[class_item.unique_id] = class_item

        file_name = csv_name.replace(".csv", "_filtered_commit" + str(threshold) + ".csv")
        file_writer = open(file_name, 'wt')
        file_writer.write("a,b\n")

        for class_item in data.values:
            try:
                entity1_name = class_item[0]
                entity2_name = class_item[1]

                entity1_id = id_class_name_dict[entity1_name]
                entity2_id = id_class_name_dict[entity2_name]

                entity1 = entity_class_id_dict[entity1_id]
                entity2 = entity_class_id_dict[entity2_id]

                nr_of_commits_together1 = entity1.get_nr_of_occ_with(entity2_id)  # commits involving A and B
                nr_of_total_commits1 = entity1.commits_count  # total nr of commits involving A

                nr_of_commits_together2 = entity2.get_nr_of_occ_with(entity1_id)  # commits involving A and B
                nr_of_total_commits2 = entity2.commits_count  # total nr of commits involving B

                update_percentage1 = (100 * nr_of_commits_together1) / nr_of_total_commits1
                update_percentage2 = (100 * nr_of_commits_together2) / nr_of_total_commits2

                if update_percentage1 >= threshold and update_percentage2 >= threshold:
                    max = update_percentage1
                    if update_percentage2 > max:
                        max = update_percentage2
                    file_writer.write(entity1_name + "," + entity2_name + "\n")

            except BaseException as e:
                print("Statistics exception: " + entity1_name + " - " + entity2_name)

        file_writer.close()

        return file_name

    @staticmethod
    def get_entities_conn(structure_manager):
        data = pandas.read_csv("D:\\Util\\doctorat\\KeyClassesProject\\hibernate-core-5.2.12.Final.jar_StructOnly.csv")
        data["logical_count occ > 0"] = "-1"
        data["logical_count occ > 5"] = "-1"
        data["logical_count occ > 10"] = "-1"
        data["logical_count occ > 20"] = "-1"
        id_class_name_dict = {}
        entity_class_id_dict = {}

        for class_item in structure_manager.get_class_list():
            id_class_name_dict[class_item.full_name] = class_item.unique_id
            entity_class_id_dict[class_item.unique_id] = class_item

        row_index = 0
        for row in data.values:
            name = row[0]
            if name in id_class_name_dict.keys():
                id = id_class_name_dict[name]
                class_item = entity_class_id_dict[id]
                data.iloc[row_index, 14] = len(class_item.get_occurrences_below_threshold(0))
                data.iloc[row_index, 15] = len(class_item.get_occurrences_below_threshold(5))
                data.iloc[row_index, 16] = len(class_item.get_occurrences_below_threshold(10))
                data.iloc[row_index, 17] = len(class_item.get_occurrences_below_threshold(20))
            row_index += 1

        data.to_csv("D:\\Util\\doctorat\\KeyClassesProject\\hibernate-core-5.2.12.Final.jar_StructOnly_new.csv", index=False)


