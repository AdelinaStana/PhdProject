
"""
Mojo stands for "Minimum Overlapping Join Operations", and it is a metric used to compare two clusterings based on their
 similarity. Specifically, it measures the number of pairwise disagreements between two clusterings, where a
 disagreement occurs when two points that are in the same cluster in one clustering are assigned to different clusters
 in the other clustering, or vice versa.


 The Mojo metric returns a score between 0 and 1 that measures the similarity between two clusterings.
  A Mojo score of 1 indicates that the two clusterings are identical, while a score of 0 indicates that the two
  clusterings are completely different.


"""


class ClusterEvaluator:
    def compute_mojo(self, cluster1, cluster2):
        """Compute the Mojo metric to compare two clusterings."""
        if len(cluster1) != len(cluster2):
            return 0
        num_points = len(cluster1)
        num_pairs = num_points * (num_points - 1) // 2

        num_disagreements = 0
        for i in range(num_points):
            for j in range(i+1, num_points):
                if (cluster1[i] == cluster1[j]) != (cluster2[i] == cluster2[j]):
                    num_disagreements += 1

        mojo = 1 - (num_disagreements / num_pairs)

        return mojo