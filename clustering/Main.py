import sys
from clustering.LouvianClustering import LouvianClustering
from clustering.MSTClustering import MSTClustering
from clustering.DependenciesBuilder import DependenciesBuilder
from ModularizationQuality import *
from clustering.Utils import *

'''
Measurements:
'''

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

'''
The MQ measurement is bounded between -1 (no cohesion
    within the subsystems) and 1 (no coupling between the
    subsystems).
    

The score is bounded between -1 for incorrect clustering and +1 for highly dense clustering. Scores around zero 
indicate overlapping clusters.

    The score is higher when clusters are dense and well separated, which relates to a standard concept of a cluster.
    Implemented based on this article:
            https://www.sciencedirect.com/science/article/pii/0377042787901257?via%3Dihub
            
            
 a lower Davies-Bouldin index relates to a model with better separation between the clusters
    Zero is the lowest possible score. Values closer to zero indicate a better partition.            

'''
def build_and_measure(file_path):
    # print(f"============================================ {os.path.basename(file_path)} : {datetime.datetime.now()}
    # ============================================")
    print(os.path.basename(file_path), end=',')
    dependencies = DependenciesBuilder(file_path)

    louvian = LouvianClustering(dependencies)
    # louvian.print_clusters()

    mst = MSTClustering(dependencies)
    # mst.print_clusters()

    reference_labels = map_package_solution_to_labels(file_path, dependencies)

    # print("MQ metric", end=",")
    print(round(calculate_modularity(dependencies.matrix, louvian.labels), 3), end=",")
    print(round(calculate_modularity(dependencies.matrix, reference_labels), 3), end=",")

    # print("sknetwork.clustering.get_modularity", end=",")
    print(round(metrics.get_modularity(dependencies.matrix, louvian.labels), 3), end=",")
    print(round(metrics.get_modularity(dependencies.matrix, reference_labels), 3), end=",")

    # print("sklearn.metrics.silhouette_score", end=",")
    print(round(silhouette_score(dependencies.matrix, louvian.labels, metric='euclidean'), 2), end=",")
    print(round(silhouette_score(dependencies.matrix, reference_labels, metric='euclidean'), 2), end=",")

    # print("sklearn.metrics.davies_bouldin_score", end=",")
    print(round(davies_bouldin_score(dependencies.matrix, louvian.labels), 3), end=",")
    print(round(davies_bouldin_score(dependencies.matrix, reference_labels), 3), end=",")


def run_all():
    '''
    ANT
    '''

    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\sd_ant.csv")
    #
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_10_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_20_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_30_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_40_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_50_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_60_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_70_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_80_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_90_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_100_ld.csv")

    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_10_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_20_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_30_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_40_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_50_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_60_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_70_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_80_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_90_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_100_sd_ld.csv")

    '''
    CATALINA
    '''
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\sd_catalina.csv")
    #
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\catalina_git_strength_10_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\catalina_git_strength_20_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\catalina_git_strength_30_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\catalina_git_strength_40_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\catalina_git_strength_50_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\catalina_git_strength_60_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\catalina_git_strength_70_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\catalina_git_strength_80_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\catalina_git_strength_90_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\catalina_git_strength_100_ld.csv")
    #
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\catalina_git_strength_10_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\catalina_git_strength_20_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\catalina_git_strength_30_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\catalina_git_strength_40_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\catalina_git_strength_50_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\catalina_git_strength_60_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\catalina_git_strength_70_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\catalina_git_strength_80_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\catalina_git_strength_90_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\catalina_git_strength_100_sd_ld.csv")

    '''
    HIBERNATE
    '''

    build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\sd_hibernate.csv")
    #
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\hibernate_git_strength_10_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\hibernate_git_strength_20_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\hibernate_git_strength_30_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\hibernate_git_strength_40_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\hibernate_git_strength_50_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\hibernate_git_strength_60_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\hibernate_git_strength_70_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\hibernate_git_strength_80_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\hibernate_git_strength_90_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\hibernate_git_strength_100_ld.csv")
    #
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\hibernate_git_strength_10_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\hibernate_git_strength_20_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\hibernate_git_strength_30_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\hibernate_git_strength_40_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\hibernate_git_strength_50_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\hibernate_git_strength_60_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\hibernate_git_strength_70_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\hibernate_git_strength_80_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\hibernate_git_strength_90_sd_ld.csv")
    # build_and_measure("D:\\Util\\doctorat\\PhdProject\\results\\computed\\hibernate_git_strength_100_sd_ld.csv")


# with RedirectPrintToFile('./../results/output.txt'):
#     run_all()

run_all()


