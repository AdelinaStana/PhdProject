import matplotlib.pyplot as plt
import numpy as np


def create_combined_chart(arr0, arr1, arr2, arr3, arr4, output_file='combined_chart.png'):
    indices = np.arange(len(arr1))
    bar_width = 0.3
    x_labels = np.arange(10, 110, 10)

    arr1_new = np.array(arr1) - np.array(arr2)

    fig = plt.figure(figsize=(10, 8))
    gs = fig.add_gridspec(3, 1, height_ratios=[2, 1, 1])

    ax1 = fig.add_subplot(gs[0, 0])
    bars0 = ax1.bar(indices - bar_width, arr0, bar_width, color='steelblue', label='Structural dependencies', edgecolor='lightgray', hatch='//')
    bars1 = ax1.bar(indices, arr2, bar_width, label='Logical dependencies that are also structural', color='green', edgecolor='lightgray', hatch='+')
    bars2 = ax1.bar(indices, arr1_new, bar_width, bottom=arr2, label='Logical dependencies', color='lightgray')

    ax1.set_xticks(indices)
    ax1.set_xticklabels(x_labels)
    ax1.legend(loc='upper right', fontsize=14)

    ax2 = fig.add_subplot(gs[1, 0])
    ax2.plot(x_labels, arr3, label='MQ', marker='o', color='cornflowerblue')
    ax2.set_xticks(x_labels)
    ax2.legend(loc='upper right', fontsize=14)

    ax3 = fig.add_subplot(gs[2, 0])
    ax3.plot(x_labels, arr4, label='MoJo', marker='x', color='steelblue')
    ax3.set_xticks(x_labels)
    ax3.set_xlabel('LD strength threshold')
    ax3.legend(loc='upper right', fontsize=14)

    plt.subplots_adjust(hspace=0.5)
    fig.tight_layout()

    plt.savefig(output_file)
    plt.show()


'''
For Ant
arr1 = [320, 215, 174, 152, 138, 120, 106, 92, 79, 64]
arr2 = [116, 85, 72, 64, 61, 57, 51, 44, 36, 28]
arr3 = [0.144, 0.116, 0.126, 0.124, 0.121, 0.124, 0.115, 0.115, 0.114, 0.103]
arr4 = [178, 215, 207, 208, 210, 187, 210, 210, 210, 205]


Catalina
arr1 = [406, 303, 249, 208, 198, 177, 164, 127, 116, 110]
arr2 = [91, 94, 81, 72, 70, 65, 61, 51, 44, 42]
arr3 = [0.255, 0.265, 0.253, 0.243, 0.248, 0.237, 0.232, 0.225, 0.222, 0.222]
arr4 = [71, 81, 88, 89, 91, 87, 92, 95, 90, 90]


Hibernate
arr1 = [1450, 1325, 1222, 915, 900, 848, 459, 450, 432, 356]
arr2 = [225, 249, 238, 218, 226, 215, 155, 166, 159, 136]
arr3 = [0.124, 0.144, 0.149, 0.131, 0.14, 0.113, 0.105, 0.093, 0.093, 0.067]
arr4 = [1842, 1868, 1870, 1859, 1913, 1913, 1917, 1924, 1924, 1924]

Gson
arr1 = [66, 50, 41, 31, 31, 28, 26, 18, 18, 18]
arr2 = [21, 19, 23, 17, 17, 18, 16, 11, 11, 11]
arr3 = [0.215, 0.182, 0.165, 0.165, 0.165, 0.164, 0.164, 0.188, 0.188, 0.188]
arr4 = [21, 22, 22, 22, 22, 22, 22, 42, 42, 42]
'''

arr0 = [517, 517, 517, 517, 517, 517, 517, 517, 517, 517]
arr1 = [320, 215, 174, 152, 138, 120, 106, 92, 79, 64]
arr2 = [116, 85, 72, 64, 61, 57, 51, 44, 36, 28]
arr3 = [0.144, 0.116, 0.126, 0.124, 0.121, 0.124, 0.115, 0.115, 0.114, 0.103]
arr4 = [178, 215, 207, 208, 210, 187, 210, 210, 210, 205]

create_combined_chart(arr0, arr1, arr2, arr3, arr4)
