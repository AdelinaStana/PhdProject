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
