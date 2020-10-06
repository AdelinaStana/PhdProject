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
    Export percentage of update between entities A and B.
    * percentage of updates between A and B from all A updates
    * percentage of updates between A and B from all B updates
    '''
    @staticmethod
    def export_connection_percentage(csv_name, structure_manager):
        data = pandas.read_csv(csv_name)
        id_class_name_dict = {}
        entity_class_id_dict = {}

        for class_item in structure_manager.get_class_list():
            id_class_name_dict[class_item.full_name] = class_item.unique_id
            entity_class_id_dict[class_item.unique_id] = class_item

        file_writer = open(csv_name.replace(".csv", "_filtered.csv"), 'wt')
        file_writer.write("a,b,c,d\n")

        for class_item in data.values:
            try:
                entity1_name = class_item[0]
                entity2_name = class_item[1]

                entity1_id = id_class_name_dict[entity1_name]
                entity2_id = id_class_name_dict[entity2_name]

                entity1 = entity_class_id_dict[entity1_id]
                entity2 = entity_class_id_dict[entity2_id]

                nr_of_updates_together1 = entity1.get_nr_of_occ_with(entity2_id)  # update A with B and other entities
                nr_of_total_updates1 = entity1.updates_count
                nr_of_updates_separate = nr_of_total_updates1 - nr_of_updates_together1  # update A without B
                # and other entities

                nr_of_updates_together2 = entity2.get_nr_of_occ_with(entity1_id)  # update B with A and other entities
                nr_of_total_updates2 = entity2.updates_count
                nr_of_updates_separate = nr_of_total_updates2 - nr_of_updates_together2  # update B without A
                # and other entities

                update_percentage1 = (100 * nr_of_updates_together1) / nr_of_total_updates1
                update_percentage2 = (100 * nr_of_updates_together2) / nr_of_total_updates2

                file_writer.write(class_item[0] + "," + class_item[1] + "," + str(update_percentage1) +
                                  "," + str(update_percentage2) + "\n")
            except BaseException as e:
                print("Statistics error:" + class_item[0] + " - " + class_item[1])
                print(e)

        file_writer.close()
