from clustering.MojoMetric import ClusterEvaluator
from clustering.MSTCluster import MSTCluster
from clustering.DependenciesMapper import DependenciesMapper

importer = DependenciesMapper('data.csv', 'data2.csv')
sd, ld = importer.convert()


# importer = DependenciesMapper("D:\\Util\\doctorat\\PhdProject\\results\\structural_dep_ant.csv",
#                               "D:\\Util\\doctorat\\PhdProject\\results\\logica_dep_ant.csv")
# sd, ld = importer.convert()

# c1 = MSTCluster(sd, cutoff_scale=2)
# c1.fit()
# c1.print_cluster_info()
# c2 = MSTCluster(ld, cutoff_scale=2)
# c2.fit()
# c2.print_cluster_info()

import numpy as np
from sknetwork.clustering import Louvain
sd = np.array([[0,1,0,0,0,0], [0,0,1,0,0,0],[0,1,0,0,0,0],[0,0,1,0,1,1], [0,0,0,1,0,0], [0,0,0,1,0,0]], np.int32)
louvain = Louvain()
labels = louvain.fit_predict(sd)
print(len(set(labels)))
print(labels)

