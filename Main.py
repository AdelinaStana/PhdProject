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
        analysis_manager = AnalysisManager(self, self.repo, self.output_dir, self.threshold)
        if self.get_files:
            print("Converting to XML ...")
            analysis_manager.load_files_from_repo()
            analysis_manager.convert_to_xml()
            print("Getting commits ...")
            analysis_manager.get_git_commits()

        analysis_manager.load_files_from_repo()
        analysis_manager.set_xml_files_list(self.repo + "/~Temp/")
        print("Processing data ...")
        analysis_manager.process_data()

    '''
        This method is called for getting git commits statistics for all the repos that I have.
        Nr of git commits with less than 5, 10, 20, inf files changed. And average per repo.
    '''

    def get_commit_statistics(self):
        print("*************************************** COMMIT STATISTICS *************************************")
        print("Repo path: " + self.repo)
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
            nr_of_commits_str = file.split('_')[2]
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
    get_files = False
    runner = Main(args.repoPath, args.outputPath, args.threshold, get_files)

    if not args.all:
        runner.get_results()
        if args.getStatistics:
            runner.get_commit_statistics()
    else:
        repo_orig_list = ["D:\\faculta\\Master\\TestProjects\\bluecove",
                     "D:\\faculta\\Master\\TestProjects\\aima-java",
                     "D:\\faculta\\Master\\TestProjects\\powermock",
                     "D:\\faculta\\Master\\TestProjects\\restfb",
                     "D:\\faculta\\Master\\TestProjects\\RxJava",
                     "D:\\faculta\\Master\\TestProjects\\metro-jax-ws",
                     "D:\\faculta\\Master\\TestProjects\\mockito",
                     "D:\\faculta\\Master\\TestProjects\\grizzly",
                     "D:\\faculta\\Master\\TestProjects\\shipkit",
                     "D:\\faculta\\Master\\TestProjects\\OpenClinica",
                     "D:\\faculta\\Master\\TestProjects\\robolectric",
                     "D:\\faculta\\Master\\TestProjects\\aeron",
                     "D:\\faculta\\Master\\TestProjects\\antlr4",
                     "D:\\faculta\\Master\\TestProjects\\mcidasv",
                     "D:\\faculta\\Master\\TestProjects\\ShareX",
                     "D:\\faculta\\Master\\TestProjects\\aspnetboilerplate",
                     "D:\\faculta\\Master\\TestProjects\\orleans",
                     "D:\\faculta\\Master\\TestProjects\\cli",
                     "D:\\faculta\\Master\\TestProjects\\cake",
                     "D:\\faculta\\Master\\TestProjects\\Avalonia",
                     "D:\\faculta\\Master\\TestProjects\\EntityFrameworkCore",
                     "D:\\faculta\\Master\\TestProjects\\jellyfin",
                     "D:\\faculta\\Master\\TestProjects\\PowerShell",
                     "D:\\faculta\\Master\\TestProjects\\WeiXinMPSDK",
                     "D:\\faculta\\Master\\TestProjects\\ArchiSteamFarm",
                     "D:\\faculta\\Master\\TestProjects\\VisualStudio",
                     "D:\\faculta\\Master\\TestProjects\\CppSharp"]

        repo_list_aux = [
            "D:\\faculta\\Doctorat\\TestProjects\\hibernate-orm",
            "D:\\faculta\\Doctorat\\TestProjects\\jmeter",
            "D:\\faculta\\Doctorat\\TestProjects\\log4j",
            "D:\\faculta\\Doctorat\\TestProjects\\wro4j",
            "D:\\faculta\\Doctorat\\TestProjects\\tomcat",
            "D:\\faculta\\Doctorat\\TestProjects\\ant"
        ]

        repo_list = [
            "D:\\faculta\\Doctorat\\TestProjects\\ant",
        ]

        for repo in repo_list:
            runner.repo = repo
            # runner.get_commit_statistics()
            runner.get_results()
