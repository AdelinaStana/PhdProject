import sys
import os

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


def build_and_measure(file_path, median=0):
    print(os.path.basename(file_path), end=',')
    dependencies = DependenciesBuilder(file_path, median)

    louvian = LouvainClustering(dependencies)
    print(len(louvian.clusters), end=",")

    reference_labels = create_clustering_based_on_packages(file_path, dependencies)

    print(round(calculate_modularity(dependencies.matrix, louvian.labels), 3), end=",")
    print(round(calculate_modularity(dependencies.matrix, reference_labels), 3), end=",")

    print(round(metrics.get_modularity(dependencies.matrix, louvian.labels), 3), end=",")
    print(round(metrics.get_modularity(dependencies.matrix, reference_labels), 3), end=",")

    print(round(silhouette_score(dependencies.matrix, louvian.labels, metric='euclidean'), 2), end=",")
    print(round(silhouette_score(dependencies.matrix, reference_labels, metric='euclidean'), 2), end=",")

    calculate_mojo(louvian.labels, reference_labels, dependencies)


"""
Median Ant: 125
Median Catalina: 255
Median Hibernate: 106
"""


def run_project(name, median=0):
    build_and_measure(f"D:\\Util\\doctorat\\PhdProject\\results\\sd_{name}.csv")

    for i in range(10, 101, 10):
        build_and_measure(f"D:\\Util\\doctorat\\PhdProject\\results\\computed\\{name}_git_strength_{i}_ld.csv", median)

    for i in range(10, 101, 10):
        build_and_measure(f"D:\\Util\\doctorat\\PhdProject\\results\\computed\\{name}_git_strength_{i}_sd_ld.csv", median)


def run_all():
    # run_project("ant", 125)
    # run_project("catalina", 210)
    run_project("catalina", 306)


# with RedirectPrintToFile('./../results/output.txt'):

run_all()
