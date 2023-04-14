from clustering.ClusterEvaluator import ClusterEvaluator
from clustering.ClusteringAnalyzer import ClusteringAnalyzer

c1 = ClusteringAnalyzer('data.csv', cutoff_scale=1)
c1.fit()
c1.print_cluster_info()
c2 = ClusteringAnalyzer('data2.csv', cutoff_scale=1)
c2.fit()
c2.print_cluster_info()

eval = ClusterEvaluator()
print(eval.compute_mojo(c1.labels, c2.labels))

