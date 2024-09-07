from scipy import sparse
from sknetwork.clustering import Louvain
from collections import OrderedDict


class LouvainClustering:
    def __init__(self, dependencies):
        self.index_name_map = dependencies.index_name_map
        louvain = Louvain()
        matrix = sparse.csr_matrix(dependencies.matrix)
        self.labels = louvain.fit_predict(matrix)
        self.clusters = set(self.labels)

    def print_clusters(self):
        print(f"\nLouvain Clustering - cluster count: {len(self.clusters)}")

        for cluster in self.clusters:
            packages_dict = {}
            count = 0
            print(f"\n\nCluster {cluster}: ", end="")
            for i in range(0, len(self.labels)):
                if self.labels[i] == cluster:
                    full_name = self.index_name_map[i]
                    print(full_name, end=", ")
                    count += 1

                    # count packages distribution
                    packages = full_name.split(".")[:-1]
                    for package in packages:
                        if package in packages_dict.keys():
                            packages_dict[package] += 1
                        else:
                            packages_dict[package] = 1

            print(f"\nTotal: {count}")
            # print("Distribution: ", end="")
            # # print packages distribution
            # sorted_dict = OrderedDict(sorted(packages_dict.items(), key=lambda item: item[1], reverse=True))
            # for item in sorted_dict.items():
            #     print(f"{item[0]} - {item[1]} [{round((item[1]*100)/count, 1)}%]", end=", ")

