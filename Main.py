import sys

from AnalysisManager import AnalysisManager
import os


class Main:
    def __init__(self):
        self.repo_list = ["E:\\faculta\\Master\\TestProjects\\bluecove",
                          "E:\\faculta\\Master\\TestProjects\\aima-java",
                          "E:\\faculta\\Master\\TestProjects\\powermock",
                          "E:\\faculta\\Master\\TestProjects\\restfb",
                          "E:\\faculta\\Master\\TestProjects\\RxJava",
                          "E:\\faculta\\Master\\TestProjects\\metro-jax-ws",
                          "E:\\faculta\\Master\\TestProjects\\mockito",
                          "E:\\faculta\\Master\\TestProjects\\grizzly",
                          "E:\\faculta\\Master\\TestProjects\\shipkit",
                          "E:\\faculta\\Master\\TestProjects\\OpenClinica",
                          "E:\\faculta\\Master\\TestProjects\\robolectric",
                          "E:\\faculta\\Master\\TestProjects\\aeron",
                          "E:\\faculta\\Master\\TestProjects\\antlr4",
                          "E:\\faculta\\Master\\TestProjects\\mcidasv",
                          "E:\\faculta\\Master\\TestProjects\\ShareX",
                          "E:\\faculta\\Master\\TestProjects\\aspnetboilerplate",
                          "E:\\faculta\\Master\\TestProjects\\orleans",
                          "E:\\faculta\\Master\\TestProjects\\cli",
                          "E:\\faculta\\Master\\TestProjects\\cake",
                          "E:\\faculta\\Master\\TestProjects\\Avalonia",
                          "E:\\faculta\\Master\\TestProjects\\EntityFrameworkCore",
                          "E:\\faculta\\Master\\TestProjects\\jellyfin",
                          "E:\\faculta\\Master\\TestProjects\\PowerShell",
                          "E:\\faculta\\Master\\TestProjects\\WeiXinMPSDK",
                          "E:\\faculta\\Master\\TestProjects\\ArchiSteamFarm",
                          "E:\\faculta\\Master\\TestProjects\\VisualStudio",
                          "E:\\faculta\\Master\\TestProjects\\CppSharp"]

    def get_results(self):
        for repo in self.repo_list:
            print("________________________________________"+repo+"_____________________________________________")
            analysis_manager = AnalysisManager(self, repo)
            analysis_manager.set_xml_files_list(repo + "/~Temp/")
            analysis_manager.process_data()

    '''
    This method is called for the entire process of converting to xml, saving git diff files and counting
    logical and structural dependencies for a selected repo from UI.
    '''
    def process_files(self, project_path):
        analysis_manager = AnalysisManager(self, project_path)
        print("Converting to XML .......")
        analysis_manager.convert_to_xml()
        analysis_manager.set_xml_files_list(project_path + "/~Temp/")
        print("Getting commits .......")
        analysis_manager.get_git_commits()
        print("Processing data .......")
        analysis_manager.process_data()

    '''
        This method is called for getting git commits statistics for all the repos that I have.
        Nr of git commits with less than 5, 10, 20, inf files changed. And average per repo.
    '''
    def get_commits_statistic(self):
        for repo in self.repo_list:
            print("______________________________________________________________________________________")
            print(repo)
            repo = repo + "\\~diffs"
            sum_commits = 0
            nr_commits = 0
            commits_under_5 = 0
            commits_under_10 = 0
            commits_under_20 = 0
            commits_above_20 = 0
            for file in os.listdir(repo):
                nr_commits += 1
                file = file.replace('.txt', '')
                nr_of_commits_str = file.split('FilesChanged_')[1]
                commit_size = int(nr_of_commits_str)
                if commit_size <= 5:
                    commits_under_5 += 1
                elif commit_size <= 10:
                    commits_under_10 += 1
                elif commit_size <= 20:
                    commits_under_20 += 1
                else:
                    commits_above_20 += 1
                sum_commits += commit_size

            print(str(commits_under_5) + "," + str(commits_under_10) + "," + str(commits_under_20) + "," + str(
                commits_above_20)
                  + "," + str(sum_commits / nr_commits))


if __name__ == '__main__':
    m = Main()
    if len(sys.argv) > 1:
        m.process_files(sys.argv[1])
    else:
        m.get_results()
