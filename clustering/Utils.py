import csv

import networkx as nx
import numpy as np
import subprocess

'''
Use it to concatenate two csv;
First must be SD, second LD

for i in range(10, 101, 10):
    input_file1 = f"D:\\Util\\doctorat\\PhdProject\\results\\sd_catalina.csv"
    input_file2 = f"D:\\Util\\doctorat\\PhdProject\\results\\computed\\catalina_git_strength_{i}_ld.csv"

    Utils.concat_csv_files(input_file1, input_file2)

'''


def concat_csv_files(file1_path, file2_path):
    output_file = file2_path.replace("_ld.csv", "_sd_ld.csv")

    with open(output_file, 'w') as out_file:
        with open(file1_path, 'r') as file:
            for line in file:
                out_file.write(line)
        file.close()

        with open(file2_path, 'r') as file:
            for line in file:
                out_file.write(line)
        file.close()

    out_file.close()

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

'''
given a csv, merge all existing entities and split them based on packages
'''


def create_clustering_based_on_packages(file_path, dependencies_mapper):
    packages = convert_to_cluster_packages(file_path)
    label_index = 0
    labels = np.array([0]*dependencies_mapper.n)
    for package in packages.keys():
        for item in packages[package]:
            if '$' in item:
                item = item.split('$')[0]
            try:
                index = dependencies_mapper.name_index_map[item]
                labels[index] = label_index
            except BaseException as e:
                pass
        label_index += 1

    return labels


def convert_to_cluster_packages(file_path):
    class_names = set()
    with open(file_path, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if len(row) >= 2:
                entity1 = row[0].strip().split('$')[0]
                entity2 = row[1].strip().split('$')[0]
                class_names.add(entity1)
                class_names.add(entity2)

    packages = {}

    for name in class_names:
        parts = name.split(".")
        package = parts[-2]
        if package in packages.keys():
            packages[package].append(name)
        else:
            packages[package] = [name]

    threshold = 15
    if 'hibernate' in file_path:
        threshold = 30

    to_delete = set()
    keys = list(packages.keys())
    keys = sorted(keys)
    for package in keys:
        if len(packages[package]) <= threshold:
            for item in packages[package]:
                parts = item.split(".")
                new_package = parts[-3]
                if new_package in packages.keys() and new_package != package:
                    packages[new_package].append(item)
                    to_delete.add(package)

    for deleted in to_delete:
        del packages[deleted]

    # print(f"packages: {len(packages.keys())}")
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


def save_clusters(clusters, file_name):
    index = 0
    with open(file_name, 'w') as file:
        for cluster in clusters:
            for item in cluster:
                file.write(f"contain {index} {item}\n")
            index += 1

'''
Please use one of the following:

java mojo.MoJo a.rsf b.rsf
  calculates the one-way MoJo distance from a.rsf to b.rsf
java mojo.MoJo a.rsf b.rsf -fm
  calculates the MoJoFM distance from a.rsf to b.rsf
java mojo.MoJo a.rsf b.rsf -b
  calculates the two-way MoJo distance between a.rsf and b.rsf
java mojo.MoJo a.rsf b.rsf -e r.rsf
  calculates the EdgeMoJo distance between a.rsf and b.rsf
java mojo.MoJo a.rsf b.rsf -m+
  calculates the one-way MoJoPlus distance from a.rsf to b.rsf
java mojo.MoJo a.rsf b.rsf -b+
  calculates the two-way MoJoPlus distance between a.rsf and b.rsf
'''


def calculate_mojo(sol_labels, reference_lables, dependencies_mapper):
    sol_clusters = map_labels_to_cluster_array(sol_labels, dependencies_mapper)
    reference_clusters = map_labels_to_cluster_array(reference_lables, dependencies_mapper)

    save_clusters(sol_clusters, "solution.rsf")
    save_clusters(reference_clusters, "reference.rsf")

    mojo = subprocess.run(["java", "-jar", "D:\\Util\\doctorat\\mojo\\mojorun.jar", "solution.rsf", "reference.rsf"], capture_output=True, text=True)
    mojofm = subprocess.run(["java", "-jar", "D:\\Util\\doctorat\\mojo\\mojorun.jar", "solution.rsf", "reference.rsf", "-fm"], capture_output=True, text=True)

    print(mojo.stdout.strip(), end=",")
    print(mojofm.stdout.strip())



