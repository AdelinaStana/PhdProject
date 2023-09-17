import csv

import networkx as nx
import os
import numpy as np

'''
Use it to concatenate two csv;
First must be SD, second LD

concat_files("D:\\Util\\doctorat\\PhdProject\\results\\sd_ant.csv", 
"D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_10.csv")

'''


def concat_files(file1_path, file2_path):
    output_file = file2_path.replace(".csv", "_sd_ld.csv")
    reworked_ld = file2_path.replace(".csv", "_ld.csv")

    with open(output_file, 'w') as out_file:
        with open(file1_path, 'r') as file:
            for line in file:
                out_file.write(line)
        file.close()

        with open(reworked_ld, 'w') as new_ld:
            with open(file2_path, 'r') as file:
                for line in file:
                    if 'a,b' in line:
                        continue
                    out_file.write(line.strip() + ",1\n")
                    new_ld.write(line.strip() + ",1\n")
        file.close()

    out_file.close()
    new_ld.close()
    os.remove(file2_path)


'''
    plot_info(dependencies, louvian.labels)
'''


def plot_info(dependencies, labels):
    import matplotlib.pyplot as plt
    node_colors = []
    for node in dependencies.name_graph.nodes():
        node_colors.append(labels[node])
    pos = nx.spring_layout(dependencies.name_graph)
    nx.draw(dependencies.name_graph, pos, with_labels=True, node_size=500, font_size=5, font_color='black',
            font_weight='bold', node_color=node_colors, cmap=plt.cm.plasma)

    # Display the graph
    plt.show()


def map_package_solution_to_labels(file_path, dependencies_mapper):
    packages = convert_to_cluster_packages(file_path)
    label_index = 0
    labels = np.array([0]*dependencies_mapper.n)
    for package in packages.keys():
        for item in packages[package]:
            index = dependencies_mapper.name_index_map[item]
            labels[index] = label_index
        label_index += 1

    return labels

'''
given a csv, merge all existing entities and split them based on packages
'''


def convert_to_cluster_packages(file_path):
    class_names = set()
    with open(file_path, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if len(row) >= 2:
                class_names.add(row[0])
                class_names.add(row[1])

    packages = {}

    for name in class_names:
        parts = name.split(".")
        package = parts[-2]
        if package in packages.keys():
            packages[package].append(name)
        else:
            packages[package] = [name]

    to_delete = set()
    for package in packages.keys():
        if len(packages[package]) <= 4:
            for item in packages[package]:
                parts = item.split(".")
                new_package = parts[-3]
                if new_package in packages.keys():
                    packages[new_package].append(item)
                    to_delete.add(package)

    for deleted in to_delete:
        del packages[deleted]

    # print(len(packages.keys()))
    # for package in packages.keys():
    #     print(package)
    #     for item in packages[package]:
    #         print(f"\t{item}")

    return packages


def map_labels_to_cluster_array(labels, dependencies_mapper):
    clusters_dict = {}
    for i in range(0, len(labels)):
        if labels[i] in clusters_dict.keys():
            clusters_dict[labels[i]].append(i)
        else:
            clusters_dict[labels[i]] = [i]

    clusters = []
    for key in clusters_dict.keys():
        cluster = []
        for value in clusters_dict[key]:
            cluster.append(dependencies_mapper.index_name_map[value])
        clusters.append(cluster)

    return clusters


def calculate_mojo(sol_labels, reference_lables, dependencies_mapper):
    sol_clusters = map_labels_to_cluster_array(sol_labels, dependencies_mapper)
    reference_clusters = map_labels_to_cluster_array(reference_lables, dependencies_mapper)

    moves = 0
    joins = 0

    for cluster in sol_clusters:
        for reference_cluster in reference_clusters:
            intersect = len(set(cluster) & set(reference_cluster))
            moves += len(cluster) - intersect
            joins += len(reference_cluster) - intersect

    mojo = (1 - ((moves + joins)/dependencies_mapper.n))* 100
    return mojo



