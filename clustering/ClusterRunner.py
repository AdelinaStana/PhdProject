from mst_clustering import MSTClustering
import numpy as np

data = np.genfromtxt('data.csv', delimiter=',')

'''
cutoff_scale : minimum size of edges. All edges larger than cutoff_scale will be removed 
 
approximate: If True, then compute the approximate minimum spanning tree using
        n_neighbors nearest neighbors. If False, then compute the full O[N^2] edges
'''
model = MSTClustering(cutoff_scale=1, approximate=True)
model.fit(data)
labels = model.labels_

print("Labels: "+str(labels))

print("Number of clusters: "+str(len(np.unique(labels))))

nodes = {}
for i in np.unique(labels):
    nodes[i] = set(np.where(labels == i)[0])

for i, cluster_nodes in nodes.items():
    node_values = data[list(cluster_nodes)].astype(int)  # values corresponding to the indices
    node_numbers = [node+1 for node in cluster_nodes]  # convert the indices to the node numbers
    print(f"Nodes associated with label {i}: {node_values.tolist()} (Node numbers: {node_numbers})")
