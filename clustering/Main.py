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


def build_and_measure(file_path, name, reference=None):
    print(os.path.basename(file_path), end=',')
    dependencies = DependenciesBuilder(file_path)

    louvian = LouvainClustering(dependencies)
    print(len(louvian.clusters), end=",")
    print(dependencies.n, end=",")

    reference_labels = create_clustering_based_on_packages(file_path, dependencies)

    print(round(calculate_modularity(dependencies.matrix, louvian.labels), 3), end=",")
    print(round(calculate_modularity(dependencies.matrix, reference_labels), 3), end=",")

    print(round(metrics.get_modularity(dependencies.matrix, louvian.labels), 3), end=",")
    print(round(metrics.get_modularity(dependencies.matrix, reference_labels), 3), end=",")

    calculate_mojo(louvian.labels, reference_labels, dependencies)

    calculate_overlapp(file_path, reference)

    #print(calculate_key_classes_percent(dependencies, f"D:\\Util\\doctorat\\PhdProject\\results\\key classes\\{name}_top_half_key_classes.txt"))


"""
Median Ant: 125
Median Catalina: 255
Median Hibernate: 106
"""


def run_project(name):
    build_and_measure(f"D:\\Util\\doctorat\\PhdProject\\results\\structural_dep_{name}.csv", name)

    for i in range(10, 101, 10):
        build_and_measure(f"D:\\Util\\doctorat\\PhdProject\\results\\computed\\{name}_git_strength_{i}_ld.csv", name, f"D:\\Util\\doctorat\\PhdProject\\results\\structural_dep_{name}.csv")

    for i in range(10, 101, 10):
        build_and_measure(f"D:\\Util\\doctorat\\PhdProject\\results\\computed\\{name}_git_strength_{i}_sd_ld.csv",
                          name, f"D:\\Util\\doctorat\\PhdProject\\results\\structural_dep_{name}.csv")


def run_all():
    run_project("ant")
    run_project("catalina")
    run_project("hibernate")
    run_project("gson")
    run_project("RxJava")

# with RedirectPrintToFile('./../results/output.txt'):


run_all()