from scipy import sparse
from sknetwork.clustering import Leiden


class LeidenClustering:
    def __init__(self, dependencies):
        self.index_name_map = dependencies.index_name_map
        leiden = Leiden()
        matrix = sparse.csr_matrix(dependencies.matrix)
        self.labels = leiden.fit_predict(matrix)
        self.clusters = set(self.labels)