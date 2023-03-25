import numpy as np
from graph_based_clustering import ConnectedComponentsClustering
# docs: https://pypi.org/project/graph-based-clustering/


X = np.array([[0, 1], [1, 0], [1, 1]])

clustering = ConnectedComponentsClustering(
    threshold=0.275,
    metric="euclidean",
    n_jobs=-1,
)

clustering.fit(X)
labels_pred = clustering.labels_

# alternative
labels_pred = clustering.fit_predict(X)

