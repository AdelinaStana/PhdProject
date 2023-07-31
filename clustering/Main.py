from clustering.LouvianClustering import LouvianClustering
from clustering.MSTClustering import MMSTClustering
from clustering.DependenciesBuilder import DependenciesBuilder

dependencies = DependenciesBuilder('data.csv')

louvian = LouvianClustering(dependencies)
louvian.print_clusters()

mst = MMSTClustering(dependencies)
mst.print_clusters()


