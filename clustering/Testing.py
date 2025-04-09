import scipy.stats as stats


def run_anova_and_print(label, group1, group2, group3):
    f_stat, p_value = stats.f_oneway(group1*10, group2, group3)
    print(f"{label} ANOVA F-statistic: {f_stat:.4f}")
    if p_value < 0.05:
        print(f"{label} p_value: {p_value:.4f} (< 0.05 -> Statistically significant differences found.)")
    else:
        print(f"{label} p_value: {p_value:.4f} (>= 0.05 -> No statistically significant difference.)")


Ant_MQ_SD_Louvain = [0.114]
Ant_MQ_LD_Louvain = [0.506, 0.547, 0.558, 0.580, 0.604, 0.587, 0.577, 0.576, 0.606, 0.611]
Ant_MQ_SDLD_Louvain = [0.355, 0.318, 0.282, 0.340, 0.248, 0.244, 0.238, 0.246, 0.258, 0.214]

Ant_MoJoFM_SD_Louvain = [46.02]
Ant_MoJoFM_LD_Louvain = [65.57, 68, 71.7, 71.53, 73.98, 70.48, 71.43, 70.13, 71.88, 75.51]
Ant_MoJoFM_SDLD_Louvain = [55.18, 52.39, 53.19, 51.99, 52.59, 50.8, 51.00, 45.22, 46.02, 50.8]

Ant_MQ_SD_Leiden = [0.101]
Ant_MQ_LD_Leiden = [0.506, 0.547, 0.558, 0.580, 0.604, 0.587, 0.577, 0.576, 0.606, 0.611]
Ant_MQ_SDLD_Leiden = [0.254, 0.365, 0.265, 0.317, 0.298, 0.271, 0.281, 0.255, 0.268, 0.227]

Ant_MoJoFM_SD_Leiden = [52.99]
Ant_MoJoFM_LD_Leiden = [65.57, 68, 71.7, 71.53, 73.98, 70.48, 71.43, 70.13, 71.88, 75.51]
Ant_MoJoFM_SDLD_Leiden = [54.98, 53.78, 54.78, 53.19, 56.77, 54.38, 52.99, 45.82, 47.01, 50.4]

Ant_MQ_SD_DBSCAN = [0.144]
Ant_MQ_LD_DBSCAN = [0.435, 0.505, 0.585, 0.602, 0.633, 0.650, 0.661, 0.709, 0.705, 0.691]
Ant_MQ_SDLD_DBSCAN = [0.147, 0.149, 0.159, 0.146, 0.146, 0.155, 0.155, 0.155, 0.155, 0.155]

Ant_MoJoFM_SD_DBSCAN = [25.1]
Ant_MoJoFM_LD_DBSCAN = [39.02, 53.5, 50, 53.06, 56.1, 51.43, 51.65, 50.65, 56.6, 56.93]
Ant_MoJoFM_SDLD_DBSCAN = [25.9, 26.49, 24.5, 24.7, 24.7, 25.1, 25.1, 25.1, 25.1, 25.1]


run_anova_and_print("Ant Louvain MQ", Ant_MQ_SD_Louvain, Ant_MQ_LD_Louvain, Ant_MQ_SDLD_Louvain)
run_anova_and_print("Ant Louvain MoJoFM", Ant_MoJoFM_SD_Louvain, Ant_MoJoFM_LD_Louvain, Ant_MoJoFM_SDLD_Louvain)
run_anova_and_print("Ant Leiden MQ", Ant_MQ_SD_Leiden, Ant_MQ_LD_Leiden, Ant_MQ_SDLD_Leiden)
run_anova_and_print("Ant Leiden MoJoFM", Ant_MoJoFM_SD_Leiden, Ant_MoJoFM_LD_Leiden, Ant_MoJoFM_SDLD_Leiden)
run_anova_and_print("Ant DBSCAN MQ", Ant_MQ_SD_DBSCAN, Ant_MQ_LD_DBSCAN, Ant_MQ_SDLD_DBSCAN)
run_anova_and_print("Ant DBSCAN MoJoFM", Ant_MoJoFM_SD_DBSCAN, Ant_MoJoFM_LD_DBSCAN, Ant_MoJoFM_SDLD_DBSCAN)
print("")

tomcat_louvain_sd_mq = [0.186]
tomcat_louvain_ld_mq = [0.505, 0.538, 0.532, 0.590, 0.604, 0.601, 0.598, 0.618, 0.623, 0.640]
tomcat_louvain_sd_ld_mq = [0.324, 0.287, 0.296, 0.292, 0.294, 0.304, 0.282, 0.283, 0.311, 0.311]

tomcat_louvain_sd_mojo = [77.76]
tomcat_louvain_ld_mojo = [72.47, 68.26, 69.87, 69.70, 70.21, 70.66, 75.32, 79.49, 81.13, 85.00]
tomcat_louvain_sd_ld_mojo = [78.99, 78.22, 79.92, 79.91, 76.53, 77.15, 76.69, 76.23, 78.99, 78.83]

tomcat_leiden_sd_mq = [0.184]
tomcat_leiden_ld_mq = [0.505, 0.538, 0.532, 0.591, 0.604, 0.601, 0.598, 0.618, 0.623, 0.640]
tomcat_leiden_sd_ld_mq = [0.324, 0.320, 0.277, 0.326, 0.301, 0.286, 0.292, 0.282, 0.311, 0.305]

tomcat_leiden_sd_mojo = [76.99]
tomcat_leiden_ld_mojo = [72.47, 67.24, 69.87, 70.71, 70.21, 70.66, 75.32, 79.49, 81.13, 85.00]
tomcat_leiden_sd_ld_mojo = [78.99, 80.06, 75.77, 78.22, 76.23, 76.84, 77.45, 76.38, 78.99, 78.37]

tomcat_dbscan_sd_mq = [0.142]
tomcat_dbscan_ld_mq = [0.393, 0.510, 0.561, 0.572, 0.631, 0.662, 0.676, 0.713, 0.718, 0.735]
tomcat_dbscan_sd_ld_mq = [0.161, 0.189, 0.209, 0.198, 0.196, 0.177, 0.166, 0.153, 0.153, 0.153]

tomcat_dbscan_sd_mojo = [73.31]
tomcat_dbscan_ld_mojo = [67.93, 72.7, 80.33, 83.84, 85.11, 85.63, 88.96, 89.74, 89.62, 89.00]
tomcat_dbscan_sd_ld_mojo = [74.23, 73.31, 73.47, 73.47, 73.31, 73.62, 73.62, 73.47, 73.31, 73.31]


run_anova_and_print("Tomcat Louvain MQ", tomcat_louvain_sd_mq, tomcat_louvain_ld_mq, tomcat_louvain_sd_ld_mq)
run_anova_and_print("Tomcat Louvain MoJoFM", tomcat_louvain_sd_mojo, tomcat_louvain_ld_mojo, tomcat_louvain_sd_ld_mojo)
run_anova_and_print("Tomcat Leiden MQ", tomcat_leiden_sd_mq, tomcat_leiden_ld_mq, tomcat_leiden_sd_ld_mq)
run_anova_and_print("Tomcat Leiden MoJoFM", tomcat_leiden_sd_mojo, tomcat_leiden_ld_mojo, tomcat_leiden_sd_ld_mojo)
run_anova_and_print("Tomcat DBSCAN MQ", tomcat_dbscan_sd_mq, tomcat_dbscan_ld_mq, tomcat_dbscan_sd_ld_mq)
run_anova_and_print("Tomcat DBSCAN MoJoFM", tomcat_dbscan_sd_mojo, tomcat_dbscan_ld_mojo, tomcat_dbscan_sd_ld_mojo)
print("")

Hibernate_MQ_SD_Louvain = [0.09]
Hibernate_MQ_LD_Louvain = [0.389, 0.397, 0.38, 0.417, 0.409, 0.406, 0.516, 0.506, 0.492, 0.524]
Hibernate_MQ_SDLD_Louvain = [0.096, 0.126, 0.121, 0.182, 0.16, 0.161, 0.139, 0.142, 0.136, 0.128]

Hibernate_MoJoFM_SD_Louvain = [52.23]
Hibernate_MoJoFM_LD_Louvain = [57.22, 62.66, 62.45, 63.68, 64.56, 63.26, 69.08, 68.64, 66.93, 65.92]
Hibernate_MoJoFM_SDLD_Louvain = [53.93, 52.85, 55.76, 54.57, 52.37, 52.35, 52.78, 52.83, 52.62, 52.78]

Hibernate_MQ_SD_Leiden = [0.071]
Hibernate_MQ_LD_Leiden = [0.39, 0.397, 0.38, 0.412, 0.409, 0.41, 0.516, 0.506, 0.492, 0.524]
Hibernate_MQ_SDLD_Leiden = [0.099, 0.122, 0.15, 0.163, 0.147, 0.153, 0.154, 0.147, 0.153, 0.114]

Hibernate_MoJoFM_SD_Leiden = [52.44]
Hibernate_MoJoFM_LD_Leiden = [58.22, 62.66, 63.04, 63.56, 64.56, 63.39, 69.08, 68.64, 66.93, 65.92]
Hibernate_MoJoFM_SDLD_Leiden = [52.28, 56.21, 54.54, 55.89, 53.31, 53.19, 54.34, 53.35, 53.83, 55.23]

Hibernate_MQ_SD_DBSCAN = [0.128]
Hibernate_MQ_LD_DBSCAN = [0.395, 0.378, 0.378, 0.382, 0.386, 0.379, 0.467, 0.479, 0.473, 0.537]
Hibernate_MQ_SDLD_DBSCAN = [0.121, 0.135, 0.135, 0.134, 0.134, 0.135, 0.13, 0.13, 0.13, 0.128]

Hibernate_MoJoFM_SD_DBSCAN = [46.32]
Hibernate_MoJoFM_LD_DBSCAN = [57.08, 63.36, 65.42, 66.9, 67.02, 65.13, 58.21, 60.49, 58.66, 58.2]
Hibernate_MoJoFM_SDLD_DBSCAN = [46.01, 47.4, 49.45, 49.35, 49.37, 49.31, 47.13, 47.72, 47.72, 47.75]

run_anova_and_print("Hibernate Louvain MQ", Hibernate_MQ_SD_Louvain, Hibernate_MQ_LD_Louvain, Hibernate_MQ_SDLD_Louvain)
run_anova_and_print("Hibernate Louvain MoJoFM", Hibernate_MoJoFM_SD_Louvain, Hibernate_MoJoFM_LD_Louvain, Hibernate_MoJoFM_SDLD_Louvain)
run_anova_and_print("Hibernate Leiden MQ", Hibernate_MQ_SD_Leiden, Hibernate_MQ_LD_Leiden, Hibernate_MQ_SDLD_Leiden)
run_anova_and_print("Hibernate Leiden MoJoFM", Hibernate_MoJoFM_SD_Leiden, Hibernate_MoJoFM_LD_Leiden, Hibernate_MoJoFM_SDLD_Leiden)
run_anova_and_print("Hibernate DBSCAN MQ", Hibernate_MQ_SD_DBSCAN, Hibernate_MQ_LD_DBSCAN, Hibernate_MQ_SDLD_DBSCAN)
run_anova_and_print("Hibernate DBSCAN MoJoFM", Hibernate_MoJoFM_SD_DBSCAN, Hibernate_MoJoFM_LD_DBSCAN, Hibernate_MoJoFM_SDLD_DBSCAN)
print("")

Gson_MQ_SD_Louvain = [0.139]
Gson_MQ_LD_Louvain = [0.565, 0.547, 0.544, 0.635, 0.600, 0.552, 0.579, 0.590, 0.590, 0.590]
Gson_MQ_SDLD_Louvain = [0.317, 0.259, 0.277, 0.277, 0.270, 0.296, 0.295, 0.267, 0.267, 0.267]

Gson_MoJoFM_SD_Louvain = [53.47]
Gson_MoJoFM_LD_Louvain = [62.07, 64.29, 63.64, 69.57, 69.57, 65.00, 66.67, 60.00, 60.00, 60.00]
Gson_MoJoFM_SDLD_Louvain = [64.36, 61.39, 61.39, 61.39, 60.40, 61.39, 59.41, 58.91, 58.91, 58.91]

Gson_MQ_SD_Leiden = [0.129]
Gson_MQ_LD_Leiden = [0.572, 0.547, 0.544, 0.635, 0.600, 0.552, 0.579, 0.590, 0.590, 0.590]
Gson_MQ_SDLD_Leiden = [0.317, 0.259, 0.277, 0.277, 0.270, 0.290, 0.295, 0.263, 0.267, 0.263]

Gson_MoJoFM_SD_Leiden = [55.94]
Gson_MoJoFM_LD_Leiden = [60.34, 64.29, 63.64, 69.57, 69.57, 65.00, 66.67, 60.00, 60.00, 60.00]
Gson_MoJoFM_SDLD_Leiden = [64.36, 61.39, 61.39, 61.39, 60.89, 61.88, 59.41, 59.41, 58.91, 59.41]

Gson_MQ_SD_DBSCAN = [0.127]
Gson_MQ_LD_DBSCAN = [0.399, 0.523, 0.606, 0.612, 0.565, 0.584, 0.586, 0.544, 0.544, 0.544]
Gson_MQ_SDLD_DBSCAN = [0.172, 0.136, 0.136, 0.135, 0.135, 0.135, 0.135, 0.134, 0.134, 0.134]

Gson_MoJoFM_SD_DBSCAN = [51.88]
Gson_MoJoFM_LD_DBSCAN = [68.97, 59.52, 66.67, 69.57, 60.87, 60.00, 55.56, 40.00, 40.00, 40.00]
Gson_MoJoFM_SDLD_DBSCAN = [63.86, 53.96, 55.94, 55.94, 55.94, 55.94, 55.94, 55.45, 55.45, 55.45]

run_anova_and_print("Gson Louvain MQ", Gson_MQ_SD_Louvain, Gson_MQ_LD_Louvain, Gson_MQ_SDLD_Louvain)
run_anova_and_print("Gson Louvain MoJoFM", Gson_MoJoFM_SD_Louvain, Gson_MoJoFM_LD_Louvain, Gson_MoJoFM_SDLD_Louvain)
run_anova_and_print("Gson Leiden MQ", Gson_MQ_SD_Leiden, Gson_MQ_LD_Leiden, Gson_MQ_SDLD_Leiden)
run_anova_and_print("Gson Leiden MoJoFM", Gson_MoJoFM_SD_Leiden, Gson_MoJoFM_LD_Leiden, Gson_MoJoFM_SDLD_Leiden)
run_anova_and_print("Gson DBSCAN MQ", Gson_MQ_SD_DBSCAN, Gson_MQ_LD_DBSCAN, Gson_MQ_SDLD_DBSCAN)
run_anova_and_print("Gson DBSCAN MoJoFM", Gson_MoJoFM_SD_DBSCAN, Gson_MoJoFM_LD_DBSCAN, Gson_MoJoFM_SDLD_DBSCAN)


MQ_SD_Louvain = Ant_MQ_SD_Louvain * 10 + tomcat_louvain_sd_mq * 10 + Hibernate_MQ_SD_Louvain * 10 + Gson_MQ_SD_Louvain * 10
MQ_LD_Louvain = Ant_MQ_LD_Louvain + tomcat_louvain_ld_mq + Hibernate_MQ_LD_Louvain + Gson_MQ_LD_Louvain
MQ_SDLD_Louvain = Ant_MQ_SDLD_Louvain + tomcat_louvain_sd_ld_mq + Hibernate_MQ_SDLD_Louvain + Gson_MQ_SDLD_Louvain

MoJoFM_SD_Louvain = Ant_MoJoFM_SD_Louvain * 10 + tomcat_louvain_sd_mojo * 10 + Hibernate_MoJoFM_SD_Louvain * 10 + Gson_MoJoFM_SD_Louvain * 10
MoJoFM_LD_Louvain = Ant_MoJoFM_LD_Louvain + tomcat_louvain_ld_mojo + Hibernate_MoJoFM_LD_Louvain + Gson_MoJoFM_LD_Louvain
MoJoFM_SDLD_Louvain = Ant_MoJoFM_SDLD_Louvain + tomcat_louvain_sd_ld_mojo + Hibernate_MoJoFM_SDLD_Louvain + Gson_MoJoFM_SDLD_Louvain

MQ_SD_Leiden = Ant_MQ_SD_Leiden * 10 + tomcat_leiden_sd_mq * 10 + Hibernate_MQ_SD_Leiden * 10 + Gson_MQ_SD_Leiden * 10
MQ_LD_Leiden = Ant_MQ_LD_Leiden + tomcat_leiden_ld_mq + Hibernate_MQ_LD_Leiden + Gson_MQ_LD_Leiden
MQ_SDLD_Leiden = Ant_MQ_SDLD_Leiden + tomcat_leiden_sd_ld_mq + Hibernate_MQ_SDLD_Leiden + Gson_MQ_SDLD_Leiden

MoJoFM_SD_Leiden = Ant_MoJoFM_SD_Leiden * 10 + tomcat_leiden_sd_mojo * 10 + Hibernate_MoJoFM_SD_Leiden * 10 + Gson_MoJoFM_SD_Leiden * 10
MoJoFM_LD_Leiden = Ant_MoJoFM_LD_Leiden + tomcat_leiden_ld_mojo + Hibernate_MoJoFM_LD_Leiden + Gson_MoJoFM_LD_Leiden
MoJoFM_SDLD_Leiden = Ant_MoJoFM_SDLD_Leiden + tomcat_leiden_sd_ld_mojo + Hibernate_MoJoFM_SDLD_Leiden + Gson_MoJoFM_SDLD_Leiden

MQ_SD_DBSCAN = Ant_MQ_SD_DBSCAN * 10 + tomcat_dbscan_sd_mq * 10 + Hibernate_MQ_SD_DBSCAN * 10 + Gson_MQ_SD_DBSCAN * 10
MQ_LD_DBSCAN = Ant_MQ_LD_DBSCAN + tomcat_dbscan_ld_mq + Hibernate_MQ_LD_DBSCAN + Gson_MQ_LD_DBSCAN
MQ_SDLD_DBSCAN = Ant_MQ_SDLD_DBSCAN + tomcat_dbscan_sd_ld_mq + Hibernate_MQ_SDLD_DBSCAN + Gson_MQ_SDLD_DBSCAN

MoJoFM_SD_DBSCAN = Ant_MoJoFM_SD_DBSCAN * 10 + tomcat_dbscan_sd_mojo * 10 + Hibernate_MoJoFM_SD_DBSCAN * 10 + Gson_MoJoFM_SD_DBSCAN * 10
MoJoFM_LD_DBSCAN = Ant_MoJoFM_LD_DBSCAN + tomcat_dbscan_ld_mojo + Hibernate_MoJoFM_LD_DBSCAN + Gson_MoJoFM_LD_DBSCAN
MoJoFM_SDLD_DBSCAN = Ant_MoJoFM_SDLD_DBSCAN + tomcat_dbscan_sd_ld_mojo + Hibernate_MoJoFM_SDLD_DBSCAN + Gson_MoJoFM_SDLD_DBSCAN


run_anova_and_print("Louvain MQ", MQ_SD_Louvain, MQ_LD_Louvain, MQ_SDLD_Louvain)
run_anova_and_print("Louvain MoJoFM", MoJoFM_SD_Louvain, MoJoFM_LD_Louvain, MoJoFM_SDLD_Louvain)
run_anova_and_print("Leiden MQ", MQ_SD_Leiden, MQ_LD_Leiden, MQ_SDLD_Leiden)
run_anova_and_print("Leiden MoJoFM", MoJoFM_SD_Leiden, MoJoFM_LD_Leiden, MoJoFM_SDLD_Leiden)
run_anova_and_print("DBSCAN MQ", MQ_SD_DBSCAN, MQ_LD_DBSCAN, MQ_SDLD_DBSCAN)
run_anova_and_print("DBSCAN MoJoFM", MoJoFM_SD_DBSCAN, MoJoFM_LD_DBSCAN, MoJoFM_SDLD_DBSCAN)


MQ_SD_Louvain = Ant_MQ_SD_Louvain * 4 + tomcat_louvain_sd_mq * 4 + Hibernate_MQ_SD_Louvain * 4 + Gson_MQ_SD_Louvain * 4
MQ_LD_Louvain = Ant_MQ_LD_Louvain[:4] + tomcat_louvain_ld_mq[:4] + Hibernate_MQ_LD_Louvain[:4] + Gson_MQ_LD_Louvain[:4]
MQ_SDLD_Louvain = Ant_MQ_SDLD_Louvain[:4] + tomcat_louvain_sd_ld_mq[:4] + Hibernate_MQ_SDLD_Louvain[:4] + Gson_MQ_SDLD_Louvain[:4]

MQ_SD_Leiden = Ant_MQ_SD_Leiden * 4 + tomcat_leiden_sd_mq * 4 + Hibernate_MQ_SD_Leiden * 4 + Gson_MQ_SD_Leiden * 4
MQ_LD_Leiden = Ant_MQ_LD_Leiden[:4] + tomcat_leiden_ld_mq[:4] + Hibernate_MQ_LD_Leiden[:4] + Gson_MQ_LD_Leiden[:4]
MQ_SDLD_Leiden = Ant_MQ_SDLD_Leiden[:4] + tomcat_leiden_sd_ld_mq[:4] + Hibernate_MQ_SDLD_Leiden[:4] + Gson_MQ_SDLD_Leiden[:4]

MQ_SD_DBSCAN = Ant_MQ_SD_DBSCAN * 4 + tomcat_dbscan_sd_mq * 4 + Hibernate_MQ_SD_DBSCAN * 4 + Gson_MQ_SD_DBSCAN * 4
MQ_LD_DBSCAN = Ant_MQ_LD_DBSCAN[:4] + tomcat_dbscan_ld_mq[:4] + Hibernate_MQ_LD_DBSCAN[:4] + Gson_MQ_LD_DBSCAN[:4]
MQ_SDLD_DBSCAN = Ant_MQ_SDLD_DBSCAN[:4] + tomcat_dbscan_sd_ld_mq[:4] + Hibernate_MQ_SDLD_DBSCAN[:4] + Gson_MQ_SDLD_DBSCAN[:4]

MoJoFM_SD_Louvain = Ant_MoJoFM_SD_Louvain * 4 + tomcat_louvain_sd_mojo * 4 + Hibernate_MoJoFM_SD_Louvain * 4 + Gson_MoJoFM_SD_Louvain * 4
MoJoFM_LD_Louvain = Ant_MoJoFM_LD_Louvain[:4] + tomcat_louvain_ld_mojo[:4] + Hibernate_MoJoFM_LD_Louvain[:4] + Gson_MoJoFM_LD_Louvain[:4]
MoJoFM_SDLD_Louvain = Ant_MoJoFM_SDLD_Louvain[:4] + tomcat_louvain_sd_ld_mojo[:4] + Hibernate_MoJoFM_SDLD_Louvain[:4] + Gson_MoJoFM_SDLD_Louvain[:4]

MoJoFM_SD_Leiden = Ant_MoJoFM_SD_Leiden * 4 + tomcat_leiden_sd_mojo * 4 + Hibernate_MoJoFM_SD_Leiden * 4 + Gson_MoJoFM_SD_Leiden * 4
MoJoFM_LD_Leiden = Ant_MoJoFM_LD_Leiden[:4] + tomcat_leiden_ld_mojo[:4] + Hibernate_MoJoFM_LD_Leiden[:4] + Gson_MoJoFM_LD_Leiden[:4]
MoJoFM_SDLD_Leiden = Ant_MoJoFM_SDLD_Leiden[:4] + tomcat_leiden_sd_ld_mojo[:4] + Hibernate_MoJoFM_SDLD_Leiden[:4] + Gson_MoJoFM_SDLD_Leiden[:4]

MoJoFM_SD_DBSCAN = Ant_MoJoFM_SD_DBSCAN * 4 + tomcat_dbscan_sd_mojo * 4 + Hibernate_MoJoFM_SD_DBSCAN * 4 + Gson_MoJoFM_SD_DBSCAN * 4
MoJoFM_LD_DBSCAN = Ant_MoJoFM_LD_DBSCAN[:4] + tomcat_dbscan_ld_mojo[:4] + Hibernate_MoJoFM_LD_DBSCAN[:4] + Gson_MoJoFM_LD_DBSCAN[:4]
MoJoFM_SDLD_DBSCAN = Ant_MoJoFM_SDLD_DBSCAN[:4] + tomcat_dbscan_sd_ld_mojo[:4] + Hibernate_MoJoFM_SDLD_DBSCAN[:4] + Gson_MoJoFM_SDLD_DBSCAN[:4]


run_anova_and_print("Louvain MQ [10–40]", MQ_SD_Louvain, MQ_LD_Louvain, MQ_SDLD_Louvain)
run_anova_and_print("Louvain MoJoFM [10–40]", MoJoFM_SD_Louvain, MoJoFM_LD_Louvain, MoJoFM_SDLD_Louvain)
run_anova_and_print("Leiden MQ [10–40]", MQ_SD_Leiden, MQ_LD_Leiden, MQ_SDLD_Leiden)
run_anova_and_print("Leiden MoJoFM [10–40]", MoJoFM_SD_Leiden, MoJoFM_LD_Leiden, MoJoFM_SDLD_Leiden)
run_anova_and_print("DBSCAN MQ [10–40]", MQ_SD_DBSCAN, MQ_LD_DBSCAN, MQ_SDLD_DBSCAN)
run_anova_and_print("DBSCAN MoJoFM [10–40]", MoJoFM_SD_DBSCAN, MoJoFM_LD_DBSCAN, MoJoFM_SDLD_DBSCAN)