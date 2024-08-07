import argparse
import os

from Statistics import *
from AnalysisManager import AnalysisManager


class MainRunner:
    def __init__(self, output, threshold, download_files=False):
        self.output_dir = output
        self.threshold = threshold
        self.get_files = download_files

    def get_results(self, repo, jar_file):
        """
        This method is called for the entire process of converting to xml, saving git diff files and counting
        logical and structural dependencies for a selected repo from UI.
        """
        print("***************************************" + repo + "*************************************")
        analysis_manager = AnalysisManager(repo, self.output_dir, self.threshold, jar_file)

        if self.get_files:
            print("Converting to XML ...")
            analysis_manager.load_files_from_repo()
            analysis_manager.convert_to_xml()
            print("Getting commits ...")
            analysis_manager.get_git_commits()

        analysis_manager.load_files_from_repo()
        analysis_manager.set_xml_files_list(repo + "/~Temp/")
        print("Processing data ...")
        analysis_manager.process_data()


def run_regression_test():
    """
    The regression was run for all three projects and the following counters in this order:
    CounterCommit; CounterOccurrences; CounterStrengthConfidence; CounterStrength
    compare: "D:\\Util\\doctorat\\PhdProject\\results\\results_old.txt"
    """
    if os.path.exists("D:\\Util\\doctorat\\TestProjects\\results\\results.txt"):
        os.remove("D:\\Util\\doctorat\\TestProjects\\results\\results.txt")

    runner = MainRunner("D:\\Util\\doctorat\\TestProjects\\results", 20)

    repo_dict = {
        "D:\\Util\\doctorat\\TestProjects\\ant": "D:\\Util\\doctorat\\TestProjects\\jars\\ant.jar",
        "D:\\Util\\doctorat\\TestProjects\\catalina": "D:\\Util\\doctorat\\TestProjects\\jars\\tomcat-catalina-9.0.4.jar",
        "D:\\Util\\doctorat\\TestProjects\\hibernate": "D:\\Util\\doctorat\\TestProjects\\jars\\hibernate-core-5.2.12.Final.jar"
    }

    for repo in repo_dict:
        if os.path.exists(repo):
            runner.get_results(repo, repo_dict[repo])


if __name__ == '__main__':
    option = argparse.ArgumentParser()
    option.add_argument('--repoPath', dest='repoPath', default="", type=str,
                        help='path to git repository')
    option.add_argument('--outputPath', dest='outputPath', default="D:\\Util\\doctorat\\TestProjects\\results", type=str,
                        help='path of output folder')
    option.add_argument('--threshold', dest='threshold', default=20, type=int,
                        help='threshold for accepted length of git files in a commit')
    option.add_argument('--getFiles', dest='getFiles', default=False, type=bool,
                        help='download git diffs and convert source code to xml')

    args = option.parse_args()
    runner = MainRunner(args.outputPath, args.threshold, args.getFiles)

    # run_regression_test()

    repo_dict = {
             "D:\\Util\\doctorat\\TestProjects\\ant": "D:\\Util\\doctorat\\TestProjects\\jars\\ant.jar",
             "D:\\Util\\doctorat\\TestProjects\\catalina": "D:\\Util\\doctorat\\TestProjects\\jars\\tomcat-catalina-9.0.4.jar",
             "D:\\Util\\doctorat\\TestProjects\\hibernate": "D:\\Util\\doctorat\\TestProjects\\jars\\hibernate-core-5.2.12.Final.jar",
             "D:\\Util\\doctorat\\TestProjects\\gson": "D:\\Util\\doctorat\\TestProjects\\jars\\gson-2.10.1.jar",
             # "D:\\Util\\doctorat\\TestProjects\\RxJava": "D:\\Util\\doctorat\\TestProjects\\jars\\rxjava-3.1.8.jar",
    }

    for repo in repo_dict.keys():
        Statistics.get_commit_statistics(repo)

    # for repo in repo_dict:
    #     runner.get_results(repo, repo_dict[repo])
