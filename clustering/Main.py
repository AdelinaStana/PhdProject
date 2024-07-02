import sys
import ModularizationQualityNew
import ModularizationQuality
from clustering import Utils
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


def build_and_measure(dependencies_path, reference_solution_path, original_dependencies):
    print(os.path.basename(dependencies_path), end=',')
    dependencies = DependenciesBuilder(dependencies_path, original_dependencies)
    reference_labels = import_clustering_solution(reference_solution_path, dependencies)

    louvian = LouvainClustering(dependencies)
    print(len(louvian.clusters), end=",")
    print(dependencies.n, end=",")

    if original_dependencies is None:
        original_dependencies = dependencies

    print(round(ModularizationQuality.calculate_modularity(original_dependencies.matrix, louvian.labels), 3),
          end=",")
    print(round(ModularizationQuality.calculate_modularity(original_dependencies.matrix, reference_labels), 3),
          end=",")

    print(round(metrics.get_modularity(original_dependencies.matrix, louvian.labels), 3), end=",")
    print(round(metrics.get_modularity(original_dependencies.matrix, reference_labels), 3), end=",")

    calculate_mojo(louvian.labels, reference_labels, original_dependencies)


def run_project(name):
    dependencies_orig = DependenciesBuilder(f"D:\\Util\\doctorat\\PhdProject\\results\\structural_dep_{name}.csv")

    build_and_measure(f"D:\\Util\\doctorat\\PhdProject\\results\\structural_dep_{name}.csv",
                      f"D:\\Util\\doctorat\\PhdProject\\results\\{name}_reference.rsf", dependencies_orig)

    print()

    for i in range(10, 101, 10):
        build_and_measure(f"D:\\Util\\doctorat\\PhdProject\\results\\computed\\{name}_git_strength_{i}_ld.csv",
                          f"D:\\Util\\doctorat\\PhdProject\\results\\{name}_reference.rsf", None)

        calculate_overlapp(f"D:\\Util\\doctorat\\PhdProject\\results\\computed\\{name}_git_strength_{i}_ld.csv",
                           f"D:\\Util\\doctorat\\PhdProject\\results\\structural_dep_{name}.csv")

    for i in range(10, 101, 10):
        build_and_measure(f"D:\\Util\\doctorat\\PhdProject\\results\\computed\\{name}_git_strength_{i}_sd_ld.csv",
                          f"D:\\Util\\doctorat\\PhdProject\\results\\{name}_reference.rsf", dependencies_orig)

        calculate_overlapp(f"D:\\Util\\doctorat\\PhdProject\\results\\computed\\{name}_git_strength_{i}_sd_ld.csv",
                           f"D:\\Util\\doctorat\\PhdProject\\results\\structural_dep_{name}.csv")


def generate_ref_solutions():
    export_reference_solution2("ant",
                               f"D:\\Util\\doctorat\\PhdProject\\results\\computed\\ant_git_strength_100_sd_ld.csv")
    export_reference_solution2("catalina",
                               f"D:\\Util\\doctorat\\PhdProject\\results\\computed\\catalina_git_strength_10_sd_ld.csv")
    export_reference_solution2("hibernate",
                               f"D:\\Util\\doctorat\\PhdProject\\results\\computed\\hibernate_git_strength_10_sd_ld.csv")
    export_reference_solution2("gson",
                               f"D:\\Util\\doctorat\\PhdProject\\results\\computed\\gson_git_strength_10_sd_ld.csv")


def run_all():
    # create_graphs()
    # ant_diff_results()

    run_project("ant")
    # run_project("catalina")
    # run_project("hibernate")
    # run_project("gson")



run_all()
