import argparse
import os

from AnalysisManager import AnalysisManager


class Main:
    def __init__(self, path, output, threshold, getfiles):
        self.repo = path
        self.output_dir = output
        self.threshold = threshold
        self.get_files = getfiles

    '''
    This method is called for the entire process of converting to xml, saving git diff files and counting
    logical and structural dependencies for a selected repo from UI.
    '''

    def get_results(self):
        print("***************************************" + self.repo + "*************************************")
        analysis_manager = AnalysisManager(self, self.repo, self.output_dir)
        if self.get_files:
            print("Converting to XML ...")
            analysis_manager.convert_to_xml()
            print("Getting commits ...")
            analysis_manager.get_git_commits()

        analysis_manager.set_xml_files_list(self.repo + "/~Temp/")
        print("Processing data ...")
        analysis_manager.process_data()

    '''
        This method is called for getting git commits statistics for all the repos that I have.
        Nr of git commits with less than 5, 10, 20, inf files changed. And average per repo.
    '''

    def get_commit_statistics(self):
        print("*************************************** COMMIT STATISTICS *************************************")
        repo_diff_path = self.repo + "\\~diffs"
        sum_commits = 0
        nr_commits = 0
        commits_under_5 = 0
        commits_under_10 = 0
        commits_under_20 = 0
        commits_above_20 = 0
        for file in os.listdir(repo_diff_path):
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

        print("Nr of commits with less than 5 files: " + str(commits_under_5))
        print("Nr of commits with more than 5 and less then 10 files: " + str(commits_under_10))
        print("Nr of commits with more than 10 and less then 20 files: " + str(commits_under_20))
        print("Nr of commits with more than 20 files: " + str(commits_above_20))
        print("Average nr of files/commit: " + str(round(sum_commits / nr_commits, 2)))

        print(str(commits_under_5) + "," + str(commits_under_10) + "," + str(commits_under_20) + "," + str(
            commits_above_20) + "," + str(round(sum_commits / nr_commits, 2)))


if __name__ == '__main__':
    option = argparse.ArgumentParser()
    option.add_argument('--repoPath', dest='repoPath', default="", type=str,
                        help='path to git repository')
    option.add_argument('--outputPath', dest='outputPath', default="", type=str,
                        help='path of output folder')
    option.add_argument('--threshold', dest='threshold', default=0, type=int,
                        help='threshold for accepted length of git files in a commit')
    option.add_argument('--getFiles', dest='getFiles', default=False, type=bool,
                        help='download git diffs and convert source code to xml')
    option.add_argument('--getStatistics', dest='getStatistics', default=False, type=bool,
                        help='print repository commit statistics')
    option.add_argument('--all', dest='all', default=False, type=bool,
                        help='run all existing build-in repositories')

    args = option.parse_args()
    runner = Main(args.repoPath, args.outputPath, args.threshold, args.getFiles)
    if not args.all:
        runner.get_results()
        if args.getStatistics:
            runner.get_commit_statistics()
    else:
        repo_list = ["E:\\faculta\\Master\\TestProjects\\bluecove",
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

        for repo in repo_list:
            runner.repo = repo
            runner.get_commit_statistics()
            runner.get_results()
