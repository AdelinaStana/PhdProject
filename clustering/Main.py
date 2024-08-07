import sys
import ModularizationQualityNew
import ModularizationQuality
from clustering import Utils
from clustering.MSTClustering import MSTClusteringWrapper
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


def print_name(dependencies_path_sd, dependencies_path_ld):
    if dependencies_path_sd and dependencies_path_ld:
        strength = dependencies_path_ld.split("_")[-2]
        print(f"SD+LD({strength})", end=',')
        return
    if dependencies_path_sd:
        print(f"SD", end=',')
        return
    if dependencies_path_ld:
        strength = dependencies_path_ld.split("_")[-2]
        print(f"LD ({strength})", end=',')
        return


def build_and_measure(dependencies_path_sd, dependencies_path_ld, reference_solution_path):
    print_name(dependencies_path_sd, dependencies_path_ld)
    dependencies = DependenciesBuilder(dependencies_path_sd, dependencies_path_ld)

    # reference_labels = import_clustering_solution_labels(reference_solution_path, dependencies)
    # print(round(ModularizationQuality.calculate_modularity(original_dependencies.matrix, reference_labels), 3),
    #       end=",")
    print(dependencies.n, end=",")

    louvian = LouvainClustering(dependencies)
    print(len(louvian.clusters), end=",")

    print(round(ModularizationQuality.calculate_modularity(dependencies.matrix, louvian.labels), 3),
          end=",")
    calculate_mojo(louvian.labels, reference_solution_path, dependencies)

    mst = MSTClusteringWrapper(dependencies)
    print(len(mst.clusters), end=",")

    print(round(ModularizationQuality.calculate_modularity(dependencies.matrix, mst.labels), 3),
          end=",")

    calculate_mojo(mst.labels, reference_solution_path, dependencies)


def run_project(name):
    build_and_measure(f"D:\\Util\\doctorat\\PhdProject\\results\\SD\\structural_dep_{name}.csv", None,
                      f"D:\\Util\\doctorat\\PhdProject\\results\\baseline\\{name}_reference.rsf")

    print()

    for i in range(10, 101, 10):
        build_and_measure(None, f"D:\\Util\\doctorat\\PhdProject\\results\\LD\\{name}_git_strength_{i}_ld.csv",
                          f"D:\\Util\\doctorat\\PhdProject\\results\\baseline\\{name}_reference.rsf")

        calculate_overlapp(f"D:\\Util\\doctorat\\PhdProject\\results\\LD\\{name}_git_strength_{i}_ld.csv",
                           f"D:\\Util\\doctorat\\PhdProject\\results\\SD\\structural_dep_{name}.csv")

    for i in range(10, 101, 10):
        build_and_measure(f"D:\\Util\\doctorat\\PhdProject\\results\\SD\\structural_dep_{name}.csv",
                          f"D:\\Util\\doctorat\\PhdProject\\results\\LD\\{name}_git_strength_{i}_ld.csv",
                          f"D:\\Util\\doctorat\\PhdProject\\results\\baseline\\{name}_reference.rsf")

        calculate_overlapp(f"D:\\Util\\doctorat\\PhdProject\\results\\LD\\{name}_git_strength_{i}_ld.csv",
                           f"D:\\Util\\doctorat\\PhdProject\\results\\SD\\structural_dep_{name}.csv")


def generate_ref_solutions():
    export_reference_solution("ant",
                              f"D:\\Util\\doctorat\\PhdProject\\results\\LD\\ant_git_strength_100_sd_ld.csv")
    export_reference_solution("catalina",
                               f"D:\\Util\\doctorat\\PhdProject\\results\\LD\\catalina_git_strength_50_sd_ld.csv")
    export_reference_solution("hibernate",
                               f"D:\\Util\\doctorat\\PhdProject\\results\\LD\\hibernate_git_strength_20_sd_ld.csv")
    export_reference_solution("gson",
                                f"D:\\Util\\doctorat\\PhdProject\\results\\LD\\gson_git_strength_10_sd_ld.csv")


def remove_unknown():
    for i in range(10, 101, 10):
        filter_csv_by_names("D:\\Util\\doctorat\\PhdProject\\results\\SD\\structural_dep_gson.csv",
                            f"D:\\Util\\doctorat\\PhdProject\\results\\LD\\gson_git_strength_{i}_ld.csv")


def run_all():
    # create_graphs()
    # diff_results("D:\\Util\\doctorat\\PhdProject\\results\\LD\\ant_git_strength_70_ld.csv",
    #              "D:\\Util\\doctorat\\PhdProject\\results\\LD\\ant_git_strength_80_ld.csv"
    #              )
    # generate_ref_solutions()
    run_project("ant")
    # run_project("catalina")
    # run_project("hibernate")
    # run_project("gson")


run_all()
