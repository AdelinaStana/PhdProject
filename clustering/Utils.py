import csv
import os

import networkx as nx
import numpy as np
import subprocess
import pandas as pd

from clustering.DependenciesBuilder import DependenciesBuilder
from clustering.LouvainClustering import LouvainClustering
from clustering.MSTClustering import MSTClusteringWrapper
from clustering.ModularizationQuality import *

'''
Use it to concatenate two csv;
First must be SD, second LD

for i in range(10, 101, 10):
    input_file1 = f"D:\\Util\\doctorat\\PhdProject\\results\\sd_catalina.csv"
    input_file2 = f"D:\\Util\\doctorat\\PhdProject\\results\\LD\\catalina_git_strength_{i}_ld.csv"

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
    for node in dependencies.graph.nodes():
        node_colors.append(labels[node])
    pos = nx.spring_layout(dependencies.graph)
    nx.draw(dependencies.graph, pos, with_labels=True, node_size=500, font_size=5, font_color='black',
            font_weight='bold', node_color=node_colors, cmap=plt.cm.plasma)

    # Display the graph
    plt.show()


"""
#diff(f"D:\\Util\\doctorat\\PhdProject\\results\\LD\\ant_git_strength_90_sd_ld.csv",
f"D:\\Util\\doctorat\\PhdProject\\results\\LD\\ant_git_strength_100_sd_ld.csv", 125)


"""


def diff(file_path1, file_path2):
    # calculate clustering for path1
    print(os.path.basename(file_path1), end=',')
    dependencies1 = DependenciesBuilder(file_path1,)
    result1 = MSTClusteringWrapper(dependencies1)

    print(len(result1.clusters), end=",")
    print(dependencies1.n, end=",")

    print(os.path.basename(file_path2), end=',')
    dependencies2 = DependenciesBuilder(file_path2)
    results2 = MSTClusteringWrapper(dependencies2)
    print(len(results2.clusters), end=",")
    print(dependencies2.n, end=",")

    sol1 = map_labels_to_cluster_array(result1.labels, dependencies1)
    sol2 = map_labels_to_cluster_array(results2.labels, dependencies2)

    for cluster1 in sol1:
        for cluster2 in sol2:
            difference = set(cluster1) - set(cluster2)
            common = set(cluster1) & set(cluster2)
            if difference != set() and len(difference) != len(cluster1):
                print(f"cluster 1: {cluster1}")
                print(f"cluster 2: {cluster2}")
                print(f"diff ({len(difference)}){difference}")
                print(f"common ({len(common)}) {common}")



'''
given a csv, merge all existing entities and split them based on packages
'''


def create_clustering_based_on_packages(file_path, dependencies_mapper):
    packages = convert_to_cluster_packages(file_path)
    label_index = 0
    labels = np.array([0] * dependencies_mapper.n)
    for package in packages.keys():
        for item in packages[package]:
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
                entity1 = row[0].strip()
                entity2 = row[1].strip()
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

    # threshold = 15
    # if 'hibernate' in file_path:
    #     threshold = 30
    #
    # to_delete = set()
    # keys = list(packages.keys())
    # keys = sorted(keys)
    # for package in keys:
    #     if len(packages[package]) <= threshold:
    #         for item in packages[package]:
    #             parts = item.split(".")
    #             new_package = parts[-3]
    #             if new_package in packages.keys() and new_package != package:
    #                 packages[new_package].append(item)
    #                 to_delete.add(package)
    #
    # for deleted in to_delete:
    #     del packages[deleted]

    # print(f"packages: {len(packages.keys())}")
    # for package in packages.keys():
    #     print(package)
    #     for item in packages[package]:
    #         print(f"\t{item}")

    return packages


def calculate_key_classes_percent(dependencies, key_class_file_path):
    with open(key_class_file_path, 'r') as file:
        key_classes = [line.strip() for line in file.readlines()]

    classes = set(dependencies.name_index_map.keys())
    nr_of_key_classes = len(classes)
    key_classes = set(key_classes)

    nr_of_found_key_classes = len(classes & key_classes)
    return round((nr_of_found_key_classes * 100) / nr_of_key_classes, 2)


def map_labels_to_cluster_array(labels, dependencies_mapper):
    clusters_dict = {}
    unique_labels = set(labels)
    for i in unique_labels:
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


def save_clusters(labels, dep_mapper, file_name):
    with open(file_name, 'w') as file:
        for i in range(0, len(labels)):
            file.write(f"contain {labels[i]} {dep_mapper.index_name_map[i]}\n")


def read_links_from_csv(file_path):
    links = set()
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 2:
                link = tuple(sorted(row[:2]))
                links.add(link)
    return links


def calculate_overlapp(file_ld, file_sd):
    percentage = 0

    if file_sd:
        links_ld = read_links_from_csv(file_ld)
        links_sd = read_links_from_csv(file_sd)

        common_links = links_ld.intersection(links_sd)
        percentage = round(((len(common_links) / len(links_ld)) * 100), 2)

    print(percentage)


'''
To export reference solution
'''


def export_reference_solution(name, file_path):
    dependencies_mapper = DependenciesBuilder(file_path)
    entities_set, data = dependencies_mapper.read_csv_dependencies(file_path)
    packages = convert_to_cluster_packages(file_path)

    for entity in entities_set:
        for package in packages.keys():
            if entity in packages[package]:
                for connection in packages[package]:
                    data.append([entity, connection, 1])
                    data.append([connection, entity, 1])

    dependencies_mapper.populate_matrix(entities_set, data)
    louvian = LouvainClustering(dependencies_mapper)
    save_clusters(louvian.labels, dependencies_mapper, f"D:\\Util\\doctorat\\PhdProject\\results\\baseline\\{name}_reference.rsf")


def import_clustering_solution_labels(file_path, dependencies_mapper):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    reference_sol_dict = {}

    for line in lines:
        name = line.split(" ")[2].strip()
        cluster = line.split(" ")[1].strip()

        reference_sol_dict[name] = cluster

    reference_sol = np.array([0]*dependencies_mapper.n)
    for name in dependencies_mapper.name_index_map.keys():
        index = dependencies_mapper.name_index_map[name]
        reference_sol[index] = reference_sol_dict[name]

    return reference_sol


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


def calculate_mojo(sol_labels, reference_sol_path, dependencies_mapper):
    save_clusters(sol_labels, dependencies_mapper, "D:\\Util\\doctorat\\PhdProject\\results\\solution.rsf")

    mojo = subprocess.run(["java", "-jar", "D:\\Util\\doctorat\\mojo\\mojorun.jar", "D:\\Util\\doctorat\\PhdProject\\results\\solution.rsf", reference_sol_path],
                          capture_output=True, text=True)
    mojofm = subprocess.run(
        ["java", "-jar", "D:\\Util\\doctorat\\mojo\\mojorun.jar", "solution.rsf", "reference.rsf", "-fm"],
        capture_output=True, text=True)

    print(mojo.stdout.strip(), end=",")


def draw_graph(G, cluster_nodes, cut_prefix):
    import plotly.graph_objects as go
    import networkx as nx

    pos = nx.spring_layout(G, k=0.75, iterations=10)

    # Create edge traces for the graph
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='Black'),
        hoverinfo='none',
        mode='lines')

    # Create node trace with smaller, fixed-size nodes
    node_x = []
    node_y = []
    node_text = []
    node_color = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        if node in cluster_nodes:
            node_color.append('green')
        else:
            node_color.append('LightSkyBlue')
        node = node.split(".")[-1]
        node_text.append(node.replace(cut_prefix, ""))

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="bottom center",
        hoverinfo='text',
        marker=dict(
            size=30,  # Smaller node size
            color=node_color,
            line=dict(color='Black', width=1)),
        textfont=dict(
            size=20,
            color='Black'),
    )

    # Create figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        paper_bgcolor='white',
                        plot_bgcolor='white',
                        showlegend=False,
                        hovermode='closest',
                        # annotations=edge_annotations,
                        margin=dict(b=0, l=0, r=0, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    fig.update_layout(
        dragmode='lasso'  # 'lasso' allows dragging nodes
    )

    # Show plot
    fig.show()


    import plotly.io as pio
    fig.update_layout(
        autosize=True,
        width=800,
        height=600
    )

    # Save the figure to a file
    pio.write_image(fig, 'D:\\network_graph.png')


def check_mapping(labels1, labels2, index):
    count = 0
    match = {}

    for i in range(len(labels1)):
        if labels1[i] == index:
            if labels2[i] not in match:
                match[labels2[i]] = []
            match[labels2[i]].append(i)
            count += 1

    best_match = max(match, key=lambda x: len(match[x])) if match else None

    return best_match


def diff_results(file_path1, file_path2):
    # calculate clustering for path1
    print(os.path.basename(file_path1), end=',')
    dependencies1 = DependenciesBuilder(file_path1)
    result1 = MSTClusteringWrapper(dependencies1)
    print(len(result1.clusters), end=",")
    print(dependencies1.n, end=",")
    print(f"Clusters: {set(result1.labels)}")
    print(f"MQ: {calculate_modularity(dependencies1.matrix, result1.labels)}")

    print(os.path.basename(file_path2), end=',')
    dependencies2 = DependenciesBuilder(file_path2)
    result2 = MSTClusteringWrapper(dependencies2)
    print(len(result2.clusters), end=",")
    print(dependencies2.n, end=",")
    print(f"Clusters: {set(result2.labels)}")
    print(f"MQ: {calculate_modularity(dependencies2.matrix, result2.labels)}")

    match_dict = {}
    for i in set(result1.labels):
        match_dict[i] = check_mapping(result1.labels, result2.labels, i)

    print(match_dict)

    for i in range(0, len(result1.labels)):
        if result1.labels[i] != result2.labels[i]:
            if match_dict[result1.labels[i]] and result2.labels[i] != match_dict[result1.labels[i]]:
                print(result2.index_name_map[i])

    result1.print_clusters()
    result2.print_clusters()


def filter_csv_by_names(csv1_path, csv2_path):
    df1 = pd.read_csv(csv1_path, header=None, usecols=[0, 1])
    df2 = pd.read_csv(csv2_path, header=None, usecols=[0, 1])

    names_set1 = set(df1[0]).union(set(df1[1]))
    names_set2 = set(df2[0]).union(set(df2[1]))
    missing = names_set2 - names_set1
    print("Missing entities:", end="")
    print(missing)

    with open(csv2_path, 'r') as file:
        all_lines = [line.strip() for line in file.readlines()]

    filtered_lines = []
    for line in all_lines:
        entities = line.split(",")
        if entities[0] in missing or entities[1] in missing:
            filtered_lines.append(line)

    with open(csv2_path, 'w') as file:
        for line in all_lines:
            if line not in filtered_lines:
                file.write(line + '\n')


def create_graphs():
    import networkx as nx

    dependencies_sd = DependenciesBuilder(f"D:\\Util\\doctorat\\PhdProject\\results\\SD\\structural_dep_ant.csv")
    dependencies_ld = DependenciesBuilder(
        f"D:\\Util\\doctorat\\PhdProject\\results\\LD\\ant_git_strength_20_sd_ld.csv", dependencies_sd)

    louvian_ld = LouvainClustering(dependencies_ld)

    G = nx.Graph()
    dependencies = dependencies_ld
    names = ['org.apache.tools.ant.taskdefs.Replace', 'org.apache.tools.ant.taskdefs.Replace$NestedString','org.apache.tools.ant.taskdefs.Replace$Replacefilter']

    # for name in names:
    #     G.add_node(name)
    #     index = dependencies.name_index_map[name]
    #     for j in range(0, dependencies.n):
    #         if dependencies.matrix[index][j] != 0:
    #             other = dependencies.index_name_map[j]
    #             G.add_node(other)
    #             G.add_edge(name, other, weight=dependencies.matrix[index][j])
    #
    #         if dependencies.matrix[j][index] != 0:
    #             other = dependencies.index_name_map[j]
    #             G.add_node(other)
    #             G.add_edge(name, other,weight=dependencies.matrix[j][index])

    draw_graph(dependencies.graph, names, "org.apache.tools.ant.")