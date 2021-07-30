from Graph import Graph
import numpy as np
import matplotlib.pyplot as plt
import statistics


class PlotCountResults:
    def __init__(self, structure_manager, output_dir):
        self.output_dir = output_dir
        self.structure_manager = structure_manager
        self.proj_name = self.structure_manager.working_dir.replace("/~results", "").split("\\")[-1]
        self.working_dir = self.structure_manager.working_dir.replace("~Temp", "~results")

    def start_count(self):
        self.build_max_commit_plot()

    def build_all_commit_plot(self):
        x = []
        y = []
        max_val = set()
        try:
            for classItem in self.structure_manager.get_class_list():
                x.append(classItem.unique_id)
                y.append(classItem.commits_count)
                max_val.add(classItem.commits_count)
        except BaseException as e:
            print(e)

        max_val = list(max_val)
        med = statistics.mean(max_val)
        print(med)

        colors = (0, 0, 0)
        area = np.pi * 3
        plt.clf()
        plt.scatter(x, y, s=area, c=colors, alpha=0.5)
        plt.title(self.proj_name)
        plt.xlabel('LD unique id')
        plt.ylabel('commits involved')
        plt.axhline(y=med, color='b')
        plt.savefig(self.output_dir+"\\fig_"+self.proj_name+"_allcommits.png")

    def build_max_commit_plot(self):
        x = []
        y = []
        max_val = set()
        try:
            for classItem in self.structure_manager.get_class_list():
                x.append(classItem.unique_id)
                values = classItem.git_links_below_commit_size_threshold.values()
                max_occ = 0
                if values:
                    max_occ = max(values)
                y.append(max_occ)
                max_val.add(max_occ)
        except BaseException as e:
            print(e)

        max_val = list(max_val)
        med = statistics.mean(max_val)
        print(med)

        i = 0
        for nr in max_val:
            if nr > med:
                i += 1

        print(i)

        colors = (0, 0, 0)
        area = np.pi * 3
        plt.clf()
        plt.scatter(x, y, s=area, c=colors, alpha=0.5)
        plt.title(self.proj_name)
        plt.xlabel('LD unique id')
        plt.ylabel('commits involved')
        plt.axhline(y=med, color='b')
        plt.savefig(self.output_dir+"\\fig_"+self.proj_name+"_maxOcc.png")
