import numpy as np

'''
MQ = 1/k(ΣAi + 1/(k(k-1)/2)Eij, k > 1
     A1,                         k = 1

k - number of clusters

Ai - the Intra-Connectivity of the ith cluster

Ai = mi/Ni^2 
i - cluster number
Ni - components number
Ni^2 - maximum intra-edge dependencies
mi - intra-edge dependencies


Eij - the Inter-Connectivity between the ith and jth clusters

Eij = eij/2NiNj , i <> j
    = 0         , i = j
i - cluster i
j - cluster j
Ni - components of cluster i
Nj - components of cluster j
eij - inter-edge dependencies

'''


def calculate_components_number(cluster_labels, cluster_id):
    return np.count_nonzero(cluster_labels == cluster_id)   # calculate components number


def calculate_intraconnectivity(adj_matrix, cluster_labels, cluster_id):
    num_nodes = adj_matrix.shape[0]
    mi = 0.0  # intra-edge dependencies

    for i in range(num_nodes):
        if cluster_labels[i] == cluster_id:
            for j in range(num_nodes):
                if cluster_labels[j] == cluster_id:
                    if adj_matrix[i, j] != 0:
                        mi += 1

    Ni = calculate_components_number(cluster_labels, cluster_id)

    # Ai = mi/Ni^2
    interconnectivity = mi / (pow(Ni, 2))
    return interconnectivity


def calculate_interconnectivity(adj_matrix, cluster_labels, cluster_id_i, cluster_id_j):
    if cluster_id_i == cluster_id_j:
        return 0

    Ni = calculate_components_number(cluster_labels, cluster_id_i)
    Nj = calculate_components_number(cluster_labels, cluster_id_j)

    if Ni == 0 or Nj == 0:
        return 0

    indices_i = np.where(cluster_labels == cluster_id_i)[0]
    indices_j = np.where(cluster_labels == cluster_id_j)[0]

    eij = 0.0  # inter-edge dependencies

    for i in indices_i:
        for j in indices_j:
            if adj_matrix[i, j] != 0 and i != j:
                eij += 1

    # Eij = eij/2NiNj
    interconnectivity = eij / (2 * Ni * Nj)
    return interconnectivity


def calculate_modularity(adj_matrix, labels):
    unique_labels = sorted(set(labels))
    k = len(unique_labels)

    if k == 1:
        return calculate_intraconnectivity(adj_matrix, labels, 0)

    sum_intraconnectivity = 0
    for i in unique_labels:
        sum_intraconnectivity += calculate_intraconnectivity(adj_matrix, labels, i)

    sum_interconnectivity = 0
    for i in unique_labels:
        for j in unique_labels:
            if i < j:
                sum_interconnectivity += calculate_interconnectivity(adj_matrix, labels, i, j)

    modularity = ((1 / k) * sum_intraconnectivity) + ((1 / ((k * (k - 1)) / 2)) * sum_interconnectivity)
    return modularity
