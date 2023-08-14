import datetime
import os
import sys

from clustering.LouvianClustering import LouvianClustering
from clustering.MSTClustering import MSTClustering
from clustering.DependenciesBuilder import DependenciesBuilder
from ModularizationQuality import *

'''
Measurements:
'''

import numpy as np
from sknetwork.clustering import metrics
from sklearn.metrics import silhouette_score
from sklearn.metrics import davies_bouldin_score


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


def build_and_measure(file_path):
    print(f"============================================ {os.path.basename(file_path)} : {datetime.datetime.now()} ============================================")
    dependencies = DependenciesBuilder(file_path)

    louvian = LouvianClustering(dependencies)
    louvian.print_clusters()

    mst = MSTClustering(dependencies)
    mst.print_clusters()

    '''
    The MQ measurement is bounded between -1 (no cohesion
    within the subsystems) and 1 (no coupling between the
    subsystems).
    '''
    print("\n\nMQ metric")
    print(np.round(calculate_modularity(dependencies.matrix, louvian.labels), 3))
    print(np.round(calculate_modularity(dependencies.matrix, mst.labels), 3))

    print("sknetwork.clustering.get_modularity")
    print(np.round(metrics.get_modularity(dependencies.matrix, louvian.labels), 3))
    print(np.round(metrics.get_modularity(dependencies.matrix, mst.labels), 3))

    print("sklearn.metrics.silhouette_score")
    '''
    The score is bounded between -1 for incorrect clustering and +1 for highly dense clustering. Scores around zero indicate overlapping clusters.

    The score is higher when clusters are dense and well separated, which relates to a standard concept of a cluster.
    Implemented based on this article:
            https://www.sciencedirect.com/science/article/pii/0377042787901257?via%3Dihub
    '''
    print(np.round(silhouette_score(dependencies.matrix, louvian.labels, metric='euclidean'), 2))
    print(np.round(silhouette_score(dependencies.matrix, mst.labels, metric='euclidean'), 2))

    print("sklearn.metrics.davies_bouldin_score")
    '''
    a lower Davies-Bouldin index relates to a model with better separation between the clusters
    Zero is the lowest possible score. Values closer to zero indicate a better partition.
    '''
    print(np.round(davies_bouldin_score(dependencies.matrix, louvian.labels), 3))
    print(np.round(davies_bouldin_score(dependencies.matrix, mst.labels), 3))


def run_all():
    build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\structural_dep_tomcat-catalina-9.0.4.csv")


with RedirectPrintToFile('./../results/output.txt'):
    run_all()

# run_all()

