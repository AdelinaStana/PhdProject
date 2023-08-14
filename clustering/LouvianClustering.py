from sknetwork.clustering import Louvain


class LouvianClustering:
    def __init__(self, dependencies):
        self.index_name_map = dependencies.index_name_map
        louvain = Louvain()
        self.labels = louvain.fit_predict(dependencies.matrix)
        self.clusters = set(self.labels)

    def print_clusters(self):
        print(f"\nLouvianClustering - cluster count: {len(self.clusters)}")

        for cluster in self.clusters:
            count = 0
            print(f"Cluster {cluster}: ", end="")
            for i in range(0, len(self.labels)):
                if self.labels[i] == cluster:
                    print(self.index_name_map[i], end=", ")
                    count += 1
            print(f"\nTotal: {count}")