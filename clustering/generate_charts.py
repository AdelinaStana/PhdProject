import matplotlib.pyplot as plt
import numpy as np


def create_combined_chart(arr0, arr1, arr2, arr3, arr4, arr5, arr6, arr7, arr8, output_file='combined_chart.png'):
    indices = np.arange(len(arr1))
    bar_width = 0.3
    x_labels = np.arange(10, 110, 10)

    arr1_new = np.array(arr1) - np.array(arr2)

    fig = plt.figure(figsize=(10, 8))
    gs = fig.add_gridspec(3, 1, height_ratios=[2, 1, 1])

    ax1 = fig.add_subplot(gs[0, 0])
    bars0 = ax1.bar(indices - bar_width, arr0, bar_width, color='steelblue', label='Structural dep. (SD)',
                    edgecolor='lightgray')
    bars1 = ax1.bar(indices, arr2, bar_width, label='LD that are also SD', color='#ffdd99', edgecolor='lightgray',
                    hatch='//')
    bars2 = ax1.bar(indices, arr1_new, bar_width, bottom=arr2, label='Logical dep. (LD)', color='lightgray',
                    edgecolor='lightgray')


    ax1.set_xticks(indices)
    ax1.set_xticklabels(x_labels, fontsize=12)
    ax1.legend(loc='upper center', fontsize=14, bbox_to_anchor=(0.5, 1.15), ncol=3, frameon=False)

    ax2 = fig.add_subplot(gs[1, 0])
    ax2.plot(x_labels, arr3, label='MQ Louvain', marker='o', color='gray')
    ax2.plot(x_labels, arr4, label='MQ Leiden', marker='s', color='#ffdd99')
    ax2.plot(x_labels, arr5, label='MQ DBSCAN', marker='^', color='steelblue')


    ax2.set_xticks(x_labels)
    ax2.set_xticklabels(x_labels, fontsize=12)
    ax2.legend(loc='upper center', fontsize=14, bbox_to_anchor=(0.5, 1.25), ncol=3, frameon=False)

    ax3 = fig.add_subplot(gs[2, 0])
    ax3.plot(x_labels, arr6, label='MoJo Louvain', marker='x', color='gray')
    ax3.plot(x_labels, arr7, label='MoJo Leiden', marker='d', color='#ffdd99')
    ax3.plot(x_labels, arr8, label='MoJo DBSCAN', marker='p', color='steelblue')


    ax3.set_xticks(x_labels)
    ax3.set_xticklabels(x_labels, fontsize=12)  # Increase fontsize for x-tick labels
    ax3.set_xlabel('LD strength threshold', fontsize=14)
    ax3.legend(loc='upper center', fontsize=14, bbox_to_anchor=(0.5, 1.25), ncol=3, frameon=False)

    # Adjust layout
    plt.subplots_adjust(hspace=0.25)
    fig.tight_layout()

    # Save the plot
    plt.savefig(output_file)
    plt.show()


'''
For Ant
arr0 = [517, 517, 517, 517, 517, 517, 517, 517, 517, 517]
arr1 = [320, 215, 174, 152, 138, 120, 106, 92, 79, 64]
arr2 = [116, 85, 72, 64, 61, 57, 51, 44, 36, 28]
arr3 = [0.355, 0.318, 0.282, 0.34, 0.248, 0.244, 0.238, 0.246, 0.258, 0.214]
arr4 = [0.254, 0.365, 0.265, 0.317, 0.298, 0.271, 0.281, 0.255, 0.268, 0.227]
arr5 = [0.147, 0.149, 0.159, 0.146, 0.146, 0.155, 0.155, 0.155, 0.155, 0.155]
arr6 = [55.18, 52.39, 53.19, 51.99, 52.59, 50.8, 51, 45.22, 46.02, 50.8]
arr7 = [54.98, 53.78, 54.78, 53.19, 56.77, 54.38, 52.99, 45.82, 47.01, 50.4]
arr8 = [25.9, 26.49, 24.5, 24.7, 24.7, 25.1, 25.1, 25.1, 25.1, 25.1]


Catalina
arr0 = [662, 662, 662, 662, 662, 662, 662, 662, 662, 662]
arr1 = [406, 303, 249, 208, 198, 177, 164, 127, 116, 110]
arr2 = [91, 94, 81, 72, 70, 65, 61, 51, 44, 42]
arr3 = [0.324, 0.287, 0.296, 0.292, 0.294, 0.304, 0.282, 0.283, 0.311, 0.311]
arr4 = [0.324, 0.32, 0.277, 0.326, 0.301, 0.286, 0.292, 0.282, 0.311, 0.305]
arr5 = [0.161, 0.189, 0.209, 0.198, 0.196, 0.177, 0.166, 0.153, 0.153, 0.153]
arr6 = [78.99, 78.22, 79.92, 79.91, 76.53, 77.15, 76.69, 76.23, 78.99, 78.83]
arr7 = [78.99, 80.06, 75.77, 78.22, 76.23, 76.84, 77.45, 76.38, 78.99, 78.37]
arr8 = [74.23, 73.31, 73.47, 73.47, 73.31, 73.62, 73.62, 73.47, 73.31, 73.31]


Hibernate
arr0 = [4414, 4414, 4414, 4414, 4414, 4414, 4414, 4414, 4414, 4414]
arr1 = [1450, 1325, 1222, 915, 900, 848, 459, 450, 432, 356]
arr2 = [225, 249, 238, 218, 226, 215, 155, 166, 159, 136]
arr3 = [0.096, 0.126, 0.121, 0.182, 0.16, 0.161, 0.139, 0.142, 0.136, 0.128]
arr4 = [0.099, 0.122, 0.15, 0.163, 0.147, 0.153, 0.154, 0.147, 0.153, 0.114]
arr5 = [0.121, 0.135, 0.135, 0.134, 0.134, 0.135, 0.13, 0.13, 0.13, 0.128]
arr6 = [53.93, 52.85, 55.76, 54.57, 52.37, 52.35, 52.78, 52.83, 52.62, 52.78]
arr7 = [52.28, 56.21, 54.54, 55.89, 53.31, 53.19, 54.34, 53.35, 53.83, 55.23]
arr8 = [46.01, 47.4, 49.45, 49.35, 49.37, 49.31, 47.13, 47.72, 47.72, 47.75]

Gson
arr1 = [66, 50, 41, 31, 31, 28, 26, 18, 18, 18]
arr2 = [21, 19, 23, 17, 17, 18, 16, 11, 11, 11]
arr3 = [0.215, 0.182, 0.165, 0.165, 0.165, 0.164, 0.164, 0.188, 0.188, 0.188]
arr4 = [21, 22, 22, 22, 22, 22, 22, 42, 42, 42]
'''

arr0 = [210, 210, 210, 210, 210, 210, 210, 210, 210, 210]
arr1 = [66, 50, 41, 31, 31, 28, 26, 18, 18, 18]
arr2 = [21, 19, 23, 17, 17, 18, 16, 11, 11, 11]
arr3 = [0.317, 0.259, 0.277, 0.277, 0.27, 0.296, 0.295, 0.267, 0.267, 0.267]
arr4 = [0.317, 0.259, 0.277, 0.277, 0.27, 0.29, 0.295, 0.263, 0.267, 0.263]
arr5 = [0.172, 0.136, 0.136, 0.135, 0.135, 0.135, 0.135, 0.134, 0.134, 0.134]
arr6 = [64.36, 61.39, 61.39, 61.39, 60.4, 61.39, 59.41, 58.91, 58.91, 58.91]
arr7 = [64.36, 61.39, 61.39, 61.39, 60.89, 61.88, 59.41, 59.41, 58.91, 59.41]
arr8 = [63.86, 53.96, 55.94, 55.94, 55.94, 55.94, 55.94, 55.45, 55.45, 55.45]



create_combined_chart(arr0, arr1, arr2, arr3, arr4, arr5, arr6, arr7, arr8)
