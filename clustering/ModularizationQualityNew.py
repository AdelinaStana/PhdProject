import numpy as np

'''
We refer to the internal edges of a cluster as intraedges
(ui), and the edges between two distinct clusters i and j as
interedges ("i;j and "j;i, respectively). If edge weights are not
provided by the MDG, we assume that each edge has a
weight of 1.
'''


def calculate_components_number(cluster_labels, cluster_id):
    return np.count_nonzero(cluster_labels == cluster_id)  # calculate components number


def calculate_intraconnectivity(adj_matrix, cluster_labels, cluster_id):
    num_nodes = adj_matrix.shape[0]
    intra_weight = 0.0

    indices = np.where(cluster_labels == cluster_id)[0]

    for i in indices:
        for j in indices:
            if i != j:
                intra_weight += adj_matrix[i, j]

    return intra_weight


def calculate_interconnectivity(adj_matrix, cluster_labels, cluster_id_i, cluster_id_j):
    if cluster_id_i == cluster_id_j:
        return 0

    indices_i = np.where(cluster_labels == cluster_id_i)[0]
    indices_j = np.where(cluster_labels == cluster_id_j)[0]

    inter_weight = 0.0  # inter-edge dependencies

    for i in indices_i:
        for j in indices_j:
            if i != j:
                inter_weight += adj_matrix[i, j]

    return inter_weight


def calculate_modularity(adj_matrix, labels):
    unique_labels = sorted(set(labels))
    modularity = 0

    for current in unique_labels:
        intraconnectivity = calculate_intraconnectivity(adj_matrix, labels, current)
        cluster_factor = 0
        if intraconnectivity != 0:
            interconnectivity = 0
            for other in unique_labels:
                if current != other:
                    interconnectivity += calculate_interconnectivity(adj_matrix, labels, other, current)

            cluster_factor = 2 * intraconnectivity / (2 * intraconnectivity + interconnectivity)

        modularity += cluster_factor

    return modularity
