import sys
from ModularizationQuality import *
from clustering.MSTClustering import MSTClustering
from clustering.Utils import *

'''
Measurements:
'''

from sknetwork.clustering import metrics


class RedirectPrintToFile:
    def __init__(self, filename):
        self.filename = filename
        self.original_stdout = sys.stdout

    def __enter__(self):
        self.file = open(self.filename, 'w')
        sys.stdout = self.file

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout = self.original_stdout
        self.file.close()



# with RedirectPrintToFile('./../results/output.txt'):

'''
The MQ measurement is bounded between -1 (no cohesion
    within the subsystems) and 1 (no coupling between the
    subsystems).


The score is bounded between -1 for incorrect clustering and +1 for highly dense clustering. Scores around zero 
indicate overlapping clusters.

    The score is higher when clusters are dense and well separated, which relates to a standard concept of a cluster.
    Implemented based on this article:
            https://www.sciencedirect.com/science/article/pii/0377042787901257?via%3Dihub

'''


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

    import matplotlib.pyplot as plt
    import networkx as nx

    # Create graph
    G = nx.Graph()

    names = [
        'org.apache.tools.ant.taskdefs.Concat',
        'org.apache.tools.ant.taskdefs.Concat$1',
        'org.apache.tools.ant.taskdefs.Concat$MultiReader',
        'org.apache.tools.ant.taskdefs.Concat$TextElement'
    ]

    # Add nodes
    for name in names:
        G.add_node(name)

    # Add edges with weights
    for name in names:
        index = dependencies_ld.name_index_map[name]
        for j in range(0, dependencies_ld.n):
            if dependencies_ld.matrix[index][j] != 0:
                other = dependencies_ld.index_name_map[j]
                G.add_edge(name.replace("org.apache.tools.ant.", ""), other.replace("org.apache.tools.ant.", ""), weight=dependencies_ld.matrix[index][j])

    # Define node colors
    node_colors = ['blue' if name in names else 'red' for name in G.nodes()]

    # Draw graph
    pos = nx.spring_layout(G)  # Layout for the graph
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=500, font_size=12, font_weight='bold')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Display
    plt.title('Weighted Graph with Different Node Colors')
    plt.show()


def build_and_measure(dependencies_path, reference_solution_path, original_dependencies):
    print(os.path.basename(dependencies_path), end=',')
    dependencies = DependenciesBuilder(dependencies_path, original_dependencies)
    print(dependencies.n, end=",")

    reference_labels = import_clustering_solution(reference_solution_path, dependencies)

    louvian = LouvainClustering(dependencies)
    print(len(louvian.clusters), end=",")

    mst = MSTClustering(dependencies)
    print(len(mst.clusters), end=",")

    print(round(calculate_modularity(original_dependencies.matrix, louvian.labels), 3), end=",")
    print(round(calculate_modularity(original_dependencies.matrix, mst.labels), 3), end=",")
    print(round(calculate_modularity(original_dependencies.matrix, reference_labels), 3), end=",")

    print(round(metrics.get_modularity(original_dependencies.matrix, louvian.labels), 3), end=",")
    print(round(metrics.get_modularity(original_dependencies.matrix, mst.labels), 3), end=",")
    print(round(metrics.get_modularity(original_dependencies.matrix, reference_labels), 3), end=",")

    calculate_mojo(louvian.labels, reference_labels, dependencies)
    calculate_mojo(mst.labels, reference_labels, dependencies)


def run_project(name):
    dependencies_orig = DependenciesBuilder(f"D:\\Util\\doctorat\\PhdProject\\results\\structural_dep_{name}.csv")

    build_and_measure(f"D:\\Util\\doctorat\\PhdProject\\results\\structural_dep_{name}.csv",
                      f"D:\\Util\\doctorat\\PhdProject\\results\\{name}_reference.rsf", dependencies_orig)
    print()

    for i in range(10, 101, 10):
        build_and_measure(f"D:\\Util\\doctorat\\PhdProject\\results\\computed\\{name}_git_strength_{i}_ld.csv",
                          f"D:\\Util\\doctorat\\PhdProject\\results\\{name}_reference.rsf", dependencies_orig)

        calculate_overlapp(f"D:\\Util\\doctorat\\PhdProject\\results\\computed\\{name}_git_strength_{i}_ld.csv",
                           f"D:\\Util\\doctorat\\PhdProject\\results\\structural_dep_{name}.csv")

    for i in range(10, 101, 10):
        build_and_measure(f"D:\\Util\\doctorat\\PhdProject\\results\\computed\\{name}_git_strength_{i}_sd_ld.csv",
                          f"D:\\Util\\doctorat\\PhdProject\\results\\{name}_reference.rsf", dependencies_orig)

        calculate_overlapp(f"D:\\Util\\doctorat\\PhdProject\\results\\computed\\{name}_git_strength_{i}_sd_ld.csv",
                           f"D:\\Util\\doctorat\\PhdProject\\results\\structural_dep_{name}.csv")


def run_all():
    ant_diff_results()
    # run_project("ant")
    # run_project("catalina")
    # run_project("hibernate")
    # run_project("gson")
    # run_project("RxJava")


run_all()