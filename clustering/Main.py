import sys
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


def delete_row_column(matrix, n):
    matrix_array = np.array(matrix)

    result_matrix = np.delete(matrix_array, n, axis=0)
    result_matrix = np.delete(result_matrix, n, axis=1)

    return result_matrix


def build_and_measure(dependencies_path, reference_solution_path, original_dependencies):
    print(os.path.basename(dependencies_path), end=',')
    dependencies = DependenciesBuilder(dependencies_path, original_dependencies)

    louvian = LouvainClustering(dependencies)
    print(len(louvian.clusters), end=",")
    print(dependencies.n, end=",")

    reference_labels = import_clustering_solution(reference_solution_path, dependencies)

    print(round(calculate_modularity(original_dependencies.matrix, louvian.labels), 3), end=",")
    print(round(calculate_modularity(original_dependencies.matrix, reference_labels), 3), end=",")

    print(round(metrics.get_modularity(original_dependencies.matrix, louvian.labels), 3), end=",")
    print(round(metrics.get_modularity(original_dependencies.matrix, reference_labels), 3), end=",")

    calculate_mojo(louvian.labels, reference_labels, dependencies)


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
    run_project("ant")
    run_project("catalina")
    run_project("hibernate")
    run_project("gson")
    run_project("RxJava")

# with RedirectPrintToFile('./../results/output.txt'):


run_all()