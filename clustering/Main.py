import sys
import os
from enum import Enum

from clustering import Utils
from clustering.LouvainClustering import LouvainClustering
from clustering.DependenciesBuilder import DependenciesBuilder
from ModularizationQuality import *
from clustering.Utils import *

'''
Measurements:
'''

from sknetwork.clustering import metrics
from sklearn.metrics import silhouette_score


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

"""
#diff(f"D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_90_sd_ld.csv",
f"D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_100_sd_ld.csv", 125)


"""
def diff(file_path1, file_path2, median=0):
    # calculate clustering for path1
    print(os.path.basename(file_path1), end=',')
    dependencies1 = DependenciesBuilder(file_path1, median)
    louvian1 = LouvainClustering(dependencies1)
    reference_labels1 = create_clustering_based_on_packages(file_path1, dependencies1)

    print(len(louvian1.clusters), end=",")
    print(dependencies1.n, end=",")

    calculate_mojo(louvian1.labels, reference_labels1, dependencies1)

    # calculate clustering for path2
    print(os.path.basename(file_path2), end=',')
    dependencies2 = DependenciesBuilder(file_path2, median)
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


def build_and_measure(file_path, median=0):
    print(os.path.basename(file_path), end=',')
    dependencies = DependenciesBuilder(file_path, median)

    louvian = LouvainClustering(dependencies)
    print(len(louvian.clusters), end=",")
    print(dependencies.n, end=",")

    reference_labels = create_clustering_based_on_packages(file_path, dependencies)

    print(round(calculate_modularity(dependencies.matrix, louvian.labels), 3), end=",")
    print(round(calculate_modularity(dependencies.matrix, reference_labels), 3), end=",")

    print(round(metrics.get_modularity(dependencies.matrix, louvian.labels), 3), end=",")
    print(round(metrics.get_modularity(dependencies.matrix, reference_labels), 3), end=",")

    calculate_mojo(louvian.labels, reference_labels, dependencies)


"""
Median Ant: 125
Median Catalina: 255
Median Hibernate: 106
"""


def run_project(name, median=0):
    build_and_measure(f"D:\\Util\\doctorat\\PhdProject\\results\\structural_dep_{name}.csv")

    for i in range(10, 101, 10):
        build_and_measure(f"D:\\Util\\doctorat\\PhdProject\\results\\computed\\{name}_git_strength_{i}_ld.csv", median)

    for i in range(10, 101, 10):
        build_and_measure(f"D:\\Util\\doctorat\\PhdProject\\results\\computed\\{name}_git_strength_{i}_sd_ld.csv",
                          median)


def run_all():
    run_project("ant", 125)
    run_project("catalina", 210)
    run_project("hibernate", 100)


# with RedirectPrintToFile('./../results/output.txt'):

run_all()




