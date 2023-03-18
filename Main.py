import argparse
import os

from AnalysisManager import AnalysisManager


class Main:
    def __init__(self, path, output, threshold, get_files, jar=None):
        self.repo = path
        self.output_dir = output
        self.threshold = threshold
        self.get_files = get_files
        self.jar_file = jar

    '''
    This method is called for the entire process of converting to xml, saving git diff files and counting
    logical and structural dependencies for a selected repo from UI.
    '''

    def get_results(self):
        print("***************************************" + self.repo + "*************************************")
        analysis_manager = AnalysisManager(self, self.repo, self.output_dir, self.threshold, self.jar_file)

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


def run_regression_test():
    pass


if __name__ == '__main__':
    option = argparse.ArgumentParser()
    option.add_argument('--repoPath', dest='repoPath', default="", type=str,
                        help='path to git repository')
    option.add_argument('--outputPath', dest='outputPath', default="", type=str,
                        help='path of output folder')
    option.add_argument('--threshold', dest='threshold', default=None, type=int,
                        help='threshold for accepted length of git files in a commit')
    option.add_argument('--getFiles', dest='getFiles', default=False, type=bool,
                        help='download git diffs and convert source code to xml')

    args = option.parse_args()
    runner = Main(args.repoPath, args.outputPath, args.threshold, args.getFiles)

    repo_dict = {
             "D:\\Util\\doctorat\\TestProjects\\ant": "D:\\Util\\doctorat\\TestProjects\\jars\\ant.jar",
             # "D:\\Util\\doctorat\\TestProjects\\catalina": "D:\\Util\\doctorat\\TestProjects\\jars\\tomcat-catalina-9.0.4.jar",
             # "D:\\Util\\doctorat\\TestProjects\\hibernate": "D:\\Util\\doctorat\\TestProjects\\jars\\hibernate-core-5.2.12.Final.jar"
    }

    for repo in repo_dict:
        runner.repo = repo
        runner.jar_file = repo_dict[repo]
        runner.get_results()
