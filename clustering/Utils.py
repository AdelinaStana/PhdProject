import csv
import os

import networkx as nx
import numpy as np
import subprocess

from clustering.DependenciesBuilder import DependenciesBuilder
from clustering.LouvainClustering import LouvainClustering

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
    for node in dependencies.graph.nodes():
        node_colors.append(labels[node])
    pos = nx.spring_layout(dependencies.graph)
    nx.draw(dependencies.graph, pos, with_labels=True, node_size=500, font_size=5, font_color='black',
            font_weight='bold', node_color=node_colors, cmap=plt.cm.plasma)

    # Display the graph
    plt.show()


"""
#diff(f"D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_90_sd_ld.csv",
f"D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_100_sd_ld.csv", 125)


"""


def diff(file_path1, file_path2):
    # calculate clustering for path1
    print(os.path.basename(file_path1), end=',')
    dependencies1 = DependenciesBuilder(file_path1,)
    louvian1 = LouvainClustering(dependencies1)
    reference_labels1 = create_clustering_based_on_packages(file_path1, dependencies1)

    print(len(louvian1.clusters), end=",")
    print(dependencies1.n, end=",")

    calculate_mojo(louvian1.labels, reference_labels1, dependencies1)

    # calculate clustering for path2
    print(os.path.basename(file_path2), end=',')
    dependencies2 = DependenciesBuilder(file_path2)
    louvian2 = LouvainClustering(dependencies2)
    print(len(louvian2.clusters), end=",")
    print(dependencies2.n, end=",")

    reference_labels2 = create_clustering_based_on_packages(file_path2, dependencies2)

    calculate_mojo(louvian2.labels, reference_labels2, dependencies2)

    sol1 = map_labels_to_cluster_array(louvian1.labels, dependencies1)
    sol2 = map_labels_to_cluster_array(louvian2.labels, dependencies2)

    for cluster1 in sol1:
        for cluster2 in sol2:
            difference = set(cluster1) - set(cluster2)
            common = set(cluster1) & set(cluster2)
            if difference != set() and len(difference) != len(cluster1):
                print(f"cluster 1: {cluster1}")
                print(f"cluster 2: {cluster2}")
                print(f"diff ({len(difference)}){difference}")
                print(f"common ({len(common)}) {common}")

    id1 = dependencies1.name_index_map["org.apache.tools.ant.util.regexp.RegexpMatcher"]
    id2 = dependencies2.name_index_map["org.apache.tools.ant.util.regexp.RegexpMatcher"]

    print(dependencies1.matrix[id1])
    print(dependencies2.matrix[id2])


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


def export_reference_solution(name, file_path, dependencies_mapper):
    reference_labels = create_clustering_based_on_packages(file_path, dependencies_mapper)
    reference_clusters = map_labels_to_cluster_array(reference_labels, dependencies_mapper)
    save_clusters(reference_clusters, f"{name}_reference.rsf")


def import_clustering_solution(file_path, dependencies_mapper):
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


def calculate_mojo(sol_labels, reference_lables, dependencies_mapper):
    sol_clusters = map_labels_to_cluster_array(sol_labels, dependencies_mapper)
    reference_clusters = map_labels_to_cluster_array(reference_lables, dependencies_mapper)

    save_clusters(sol_clusters, "solution.rsf")
    save_clusters(reference_clusters, "reference.rsf")

    mojo = subprocess.run(["java", "-jar", "D:\\Util\\doctorat\\mojo\\mojorun.jar", "solution.rsf", "reference.rsf"],
                          capture_output=True, text=True)
    mojofm = subprocess.run(
        ["java", "-jar", "D:\\Util\\doctorat\\mojo\\mojorun.jar", "solution.rsf", "reference.rsf", "-fm"],
        capture_output=True, text=True)

    print(mojo.stdout.strip(), end=",")
    print(mojofm.stdout.strip(), end=",")


def draw_graph(G, cluster_nodes, cut_prefix):
    import plotly.graph_objects as go
    import networkx as nx

    pos = nx.spring_layout(G, k=0.75, iterations=50)

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
        node_text.append(node.replace(cut_prefix, ""))

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="bottom center",
        hoverinfo='text',
        marker=dict(
            size=10,  # Smaller node size
            color=node_color,
            line=dict(color='Black', width=1)),
        textfont=dict(
            size=13,
            color='Black'),
    )

    # Create a trace for edge weights
    # edge_annotations = []
    # for edge in G.edges(data=True):
    #     x0, y0 = pos[edge[0]]
    #     x1, y1 = pos[edge[1]]
    #     edge_annotations.append(
    #         dict(
    #             x=(x0 + x1) / 2, y=(y0 + y1) / 2,
    #             xref="x", yref="y",
    #             text=str(edge[2]['weight']),  # assuming the attribute is 'weight'
    #             showarrow=False,
    #             font=dict(size=9)
    #         )
    #     )

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

    fig.update_layout(title_text="")

    # Show plot
    fig.show()

    import plotly.io as pio
    fig.update_layout(
        autosize=False,
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


def ant_diff_results():
    dependencies_sd = DependenciesBuilder(f"D:\\Util\\doctorat\\PhdProject\\results\\structural_dep_ant.csv")
    louvian_sd = LouvainClustering(dependencies_sd)

    dependencies_ld = DependenciesBuilder(f"D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_20_sd_ld.csv",
                                          dependencies_sd)

    louvian_ld = LouvainClustering(dependencies_ld)

    match_dict = {}
    for i in set(louvian_sd.labels):
        match_dict[i] = check_mapping(louvian_sd.labels, louvian_ld.labels, i)

    print(match_dict)

    for i in range(0, len(louvian_ld.labels)):
        if louvian_sd.labels[i] != louvian_ld.labels[i]:
            if match_dict[louvian_sd.labels[i]] and louvian_ld.labels[i] != match_dict[louvian_sd.labels[i]]:
                print(louvian_ld.index_name_map[i])

    louvian_sd.print_clusters()
    louvian_ld.print_clusters()


def create_graphs():
    import networkx as nx

    dependencies_sd = DependenciesBuilder(f"D:\\Util\\doctorat\\PhdProject\\results\\structural_dep_ant.csv")
    louvian_sd = LouvainClustering(dependencies_sd)

    dependencies_ld = DependenciesBuilder(
        f"D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_20_sd_ld.csv")

    louvian_ld = LouvainClustering(dependencies_ld)

    G = nx.Graph()
    dependencies = dependencies_sd
    names = [
        'org.apache.tools.ant.taskdefs.Concat',
        'org.apache.tools.ant.taskdefs.Concat$1',
        'org.apache.tools.ant.taskdefs.Concat$MultiReader',
        'org.apache.tools.ant.taskdefs.Concat$TextElement'
    ]

    for name in names:
        G.add_node(name)
        index = dependencies.name_index_map[name]
        for j in range(0, dependencies.n):
            if dependencies.matrix[index][j] != 0:
                other = dependencies.index_name_map[j]
                G.add_node(other)
                G.add_edge(name, other, weight=dependencies.matrix[index][j])

            if dependencies.matrix[j][index] != 0:
                other = dependencies.index_name_map[j]
                G.add_node(other)
                G.add_edge(name, other,weight=dependencies.matrix[j][index])

    draw_graph(G, names, "org.apache.tools.ant.")