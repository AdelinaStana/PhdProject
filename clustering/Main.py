from clustering.ClusterEvaluator import ClusterEvaluator
from clustering.ClusteringAnalyzer import ClusteringAnalyzer
from clustering.DependenciesImporter import DependenciesImporter

importer = DependenciesImporter('data.csv', 'data2.csv')
sd, ld = importer.convert()

c1 = ClusteringAnalyzer(sd, cutoff_scale=1)
c1.fit()
c1.print_cluster_info()
c2 = ClusteringAnalyzer(ld, cutoff_scale=1)
c2.fit()
c2.print_cluster_info()

eval = ClusterEvaluator()
print(eval.compute_mojo(c1.labels, c2.labels))

