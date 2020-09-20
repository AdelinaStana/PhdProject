import os
from Util import Util


class StructureManager:
    def __init__(self, working_dir):
        self.class_list = set()
        self.class_dict = {}
        self.links_count = {}
        self.working_dir = working_dir + "/~results"
        if not os.path.isdir(self.working_dir):
            os.mkdir(self.working_dir)

        self.util = Util(working_dir)  # used for save and load the analysis performed

    def get_classes_from_jar(self):
        import zipfile
        archive = zipfile.ZipFile('D:\\faculta\\Doctorat\\TestProjects\\jars\\ant.jar', 'r')
        temp_list = archive.namelist()
        jar_cls_list = set()
        for item in temp_list:
            if item.endswith(".class"):
                item = item.replace(".class", "")
                item = item.replace("/", ".")
                jar_cls_list.add(item)

        return jar_cls_list

    def filter_only_jar(self):
        jar_cls_list = self.get_classes_from_jar()
        temp_class_list = set()

        for cls in self.class_list:
            if cls.full_name in jar_cls_list:
                temp_class_list.add(cls)
            else:
                try:
                    self.class_dict.pop(cls.name)
                except KeyError:
                    pass

        self.class_list = temp_class_list

    def add_class(self, class_struct):
        self.class_dict[class_struct.get_name()] = class_struct
        self.class_list.add(class_struct)

    def get_class_list(self):
        return self.class_list

    def get_related(self, class_name):
        try:
            return self.links_count[class_name]
        except BaseException as e:
            print(e)

    def set_git_links_to_class(self, links, commit_size, commit_date):
        try:
            class_links = set()
            for link in links:
                for class_item in self.class_list:
                    if class_item.has_path(link):
                        class_links.add(class_item.get_unique_id())

            for class_item in self.class_list:
                if class_item.get_unique_id() in class_links:
                    class_item.set_git_links(class_links, commit_size, commit_date)
        except BaseException as e:
            print(e)

    def build_related(self):
        try:
            for item in self.class_list:
                item = item.build_related(self.class_dict)
        except BaseException as e:
            print(e)
