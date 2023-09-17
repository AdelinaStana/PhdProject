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
    Ni = 0  # components number
    for label in cluster_labels:
        if label == cluster_id:
            Ni += 1
    return Ni


def calculate_intraconnectivity(adj_matrix, cluster_labels, cluster_id):
    num_nodes = adj_matrix.shape[0]
    mi = 0.0  # intra-edge dependencies

    for i in range(num_nodes):
        if cluster_labels[i] == cluster_id:
            for j in range(num_nodes):
                if cluster_labels[j] == cluster_id:
                    mi += adj_matrix[i, j]

    Ni = calculate_components_number(cluster_labels, cluster_id)

    # Ai = mi/Ni^2
    intraconnectivity = mi / (pow(Ni, 2))
    return intraconnectivity


def calculate_interconnectivity(adj_matrix, cluster_labels, cluster_id_i, cluster_id_j):
    if cluster_id_i == cluster_id_j:
        return 0

    if cluster_id_i not in cluster_labels or cluster_id_j not in cluster_labels:
        return 0

    num_nodes = adj_matrix.shape[0]
    eij = 0.0  # inter-edge dependencies

    for i in range(num_nodes):
        if cluster_labels[i] == cluster_id_i:
            for j in range(num_nodes):
                if cluster_labels[j] == cluster_id_j:
                    eij += adj_matrix[i, j]
    Ni = calculate_components_number(cluster_labels, cluster_id_i)
    Nj = calculate_components_number(cluster_labels, cluster_id_j)

    # Eij = eij/2NiNj
    interconnectivity = eij / (2 * Ni * Nj)
    return interconnectivity


def calculate_modularity(adj_matrix, labels):
    k = len(set(labels))

    if k == 1:
        return calculate_intraconnectivity(adj_matrix, labels, 0)

    sum_intraconnectivity = 0
    for i in range(0, k):
        sum_intraconnectivity += calculate_intraconnectivity(adj_matrix, labels, i)

    sum_interconnectivity = 0
    for i in range(0, k):
        for j in range(0, k):
            sum_interconnectivity += calculate_interconnectivity(adj_matrix, labels, i, j)

    modularity = (1 / k) * sum_intraconnectivity + ((1 / ((k * (k - 1)) / 2)) * sum_interconnectivity)
    return modularity
