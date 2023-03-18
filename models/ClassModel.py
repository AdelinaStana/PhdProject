import os


class ClassModel:
    def __init__(self, parent=None, threshold=None):
        self.parent = parent
        self.superclass = "None"
        self.name = "None"
        self.full_name = "None"
        self.rel_file_path = "None"
        self.unique_id = -1
        self.old_paths = []
        self.attributes = set()
        self.methods = set()
        self.threshold = threshold
        self.git_links_below5 = {}
        self.git_links_below10 = {}
        self.git_links_below20 = {}
        self.git_links_total = {}
        self.git_links_below_commit_size_threshold = {}
        self.structural_relation_list = set()
        self.commits_count = 0  # count number of total commits in which is involved

    def set_name(self, name):
        self.name = name

    def set_full_name(self, name):
        self.full_name = name

    def set_unique_id(self, id):
        self.unique_id = id

    def set_old_paths(self, paths_list):
        self.old_paths = paths_list

    def set_file(self, file):
        self.rel_file_path = file.replace('.xml', '')

    def set_super_class(self, name):
        self.superclass = name

    def add_attribute(self, attrib):
        self.attributes.add(attrib)

    def add_method(self, meth):
        self.methods.add(meth)

    def get_super_class(self):
        return self.superclass

    def get_name(self):
        return self.name

    def get_unique_id(self):
        return self.unique_id

    def get_file_path(self):
        return self.rel_file_path

    def get_all_paths(self):
        return self.old_paths.add(self.rel_file_path)

    def get_file_name(self):
        return os.path.basename(self.rel_file_path)

    def get_attributes(self):
        return self.attributes

    def get_methods(self):
        return self.methods

    def set_related(self, rel_list):
        self.structural_relation_list = rel_list

    def get_structural_related_links(self):
        return self.structural_relation_list

    def has_path(self, path):
        if path == self.rel_file_path:
            return True
        if path in self.old_paths:
           return True
        return False

    def get_nr_of_occ_with(self, link_id):
        if self.threshold:
            return self.git_links_below_commit_size_threshold[link_id]
        else:
            return self.git_links_total[link_id]

    def add_if_exists(self, name, class_dict):
        if name in class_dict.keys() and name != self.name:
            self.structural_relation_list.add(class_dict[name].unique_id)

    def build_related(self, class_dict):
        self.structural_relation_list = set()

        for attrib in self.attributes:
            self.add_if_exists(attrib.get_type(), class_dict)

        for method in self.methods:
            for arg in method.get_args():
                self.add_if_exists(arg.get_type(), class_dict)

            for local in method.get_locals():
                self.add_if_exists(local.get_type(), class_dict)

        if self.superclass != "None":
            self.add_if_exists(self.superclass, class_dict)

        self.attributes.clear()
        self.methods.clear()

        return self

    def print_details(self, UIObj):
        UIObj.print_line("________________________________")
        UIObj.print_line("Class name: " + self.name)
        UIObj.print_line("Superclass: " + self.superclass)
        UIObj.print_line("Attributes: ")
        for attribute in self.attributes:
            UIObj.print_line("Type: " + attribute.get_type() + " Name: " + attribute.get_name())
        UIObj.print_line("Methods:")
        for method in self.methods:
            s = method.get_type() + ": " + method.get_name() + "("
            for arg in method.get_args():
                s = s + "Type: " + arg.get_type() + " Name: " + arg.get_name() + ","
            s += ")"
            UIObj.print_line(s)
            if method.get_locals():
                UIObj.print_line(" Local decl:")
                for local in method.get_locals():
                    UIObj.print_line(" Type: " + local.get_type() + " Name: " + local.get_name())

                UIObj.print_line(" Calls:")
                for local in method.get_locals():
                    if len(local.get_calls()) != 0:
                        UIObj.print_line(" Type: " + local.get_type() + " Name: " + local.get_name())
                        for call in local.get_calls():
                            UIObj.print_line(call)

    def set_git_links(self, links, commit_size, commit_date):
        self.commits_count += 1
        for link in links:
            if link != self.unique_id:
                if self.threshold:
                    if commit_size <= self.threshold:
                        if link not in self.git_links_below_commit_size_threshold.keys():
                            self.git_links_below_commit_size_threshold[link] = 1
                        else:
                            self.git_links_below_commit_size_threshold[link] += 1
                else:
                    if commit_size <= 5:
                        if link not in self.git_links_below5.keys():
                            self.git_links_below5[link] = 1
                        else:
                            self.git_links_below5[link] += 1
                    if commit_size <= 10:
                        if link not in self.git_links_below10.keys():
                            self.git_links_below10[link] = 1
                        else:
                            self.git_links_below10[link] += 1
                    if commit_size <= 20:
                        if link not in self.git_links_below20.keys():
                            self.git_links_below20[link] = 1
                        else:
                            self.git_links_below20[link] += 1

                    if link not in self.git_links_total.keys():
                        self.git_links_total[link] = 1
                    else:
                        self.git_links_total[link] += 1

    ##########################################################################################################

    def get_occurrence_commits_below_5files(self, nr):
        return set(key for key, value in self.git_links_below5.items() if value >= nr)

    def get_occurrence_commits_below_10files(self, nr):
        return set(key for key, value in self.git_links_below10.items() if value >= nr)

    def get_occurrence_commits_below_20files(self, nr):
        return set(key for key, value in self.git_links_below20.items() if value >= nr)

    def get_unfiltered_commit_size_occurrences(self, nr):
        return set(key for key, value in self.git_links_total.items() if value >= nr)

    def get_filtered_commit_size_occurrences(self, nr):
        return set(key for key, value in self.git_links_below_commit_size_threshold.items() if value >= nr)

    #####################################################################################################

    def get_match5_occ(self, nr_of_occ):
        git_links = self.get_occurrence_commits_below_5files(nr_of_occ)
        return self.structural_relation_list.intersection(git_links)

    def get_match10_occ(self, nr_of_occ):
        git_links = self.get_occurrence_commits_below_10files(nr_of_occ)
        return self.structural_relation_list.intersection(git_links)

    def get_match20_occ(self, nr_of_occ):
        git_links = self.get_occurrence_commits_below_20files(nr_of_occ)
        return self.structural_relation_list.intersection(git_links)

    def get_match_occ_total(self, nr_of_occ):
        git_links = self.get_unfiltered_commit_size_occurrences(nr_of_occ)
        return self.structural_relation_list.intersection(git_links)




