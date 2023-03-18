from models.ClassModel import *
import xml
from parsers.Parser import Parser
from models.AttributeModel import AttributeModel


class NameTagParser(Parser):
    def __init__(self, root_dir, unique_id, threshold=None):
        Parser.__init__(self, root_dir, unique_id)
        self.replace = "org"
        self.threshold = threshold

    def get_all_structures(self, root):
        item_list = []
        cls = root.iter("{http://www.srcML.org/srcML/src}class")
        for item in cls:
            item_list.append(item)
        cls = root.iter("{http://www.srcML.org/srcML/src}interface")
        for item in cls:
            item_list.append(item)
        cls = root.iter("{http://www.srcML.org/srcML/src}annotation_defn")
        for item in cls:
            item_list.append(item)
        cls = root.iter("{http://www.srcML.org/srcML/src}enum")
        for item in cls:
            item_list.append(item)
        return item_list

    def get_all(self, root):
        attributes = []
        names = root.iter("{http://www.srcML.org/srcML/src}name")
        for name in names:
            attribute = AttributeModel()
            t = self.get_text(name)
            attribute.set_type(t)
            attribute.set_name(t)

            attributes.append(attribute)
        return attributes

    def get_class_model(self, file, item_list):
        class_list = []

        file_path = file.replace(self.working_dir, 'a/')
        file_path = file_path.replace(".xml", "")
        file_path = file_path.replace("\\", "/")

        rep = file_path.find(self.replace)
        rep = file_path[0:rep]
        base_name = file_path.replace(rep, "")
        extension = os.path.splitext(base_name)[1]
        base_name = base_name.replace(extension, "")
        base_name = base_name.replace("/", ".")

        for item in item_list:
            class_model = ClassModel(threshold=self.threshold)
            item_name = self.get_name(item)

            if item_name != "None":
                self.unique_id += 1

                class_name = base_name
                if not base_name.endswith("."+item_name):
                    class_name = base_name + "$" + item_name

                class_model.set_name(item_name)
                class_model.set_full_name(class_name)
                class_model.set_file(file_path)
                class_model.set_unique_id(self.unique_id)
                class_model.set_super_class(self.get_item_name(item, "super"))

                # workaround
                for attribute in self.get_all(item):
                    class_model.add_attribute(attribute)

                class_list.append(class_model)

        return class_list

    def get_class_list(self, file):
        tree = xml.etree.ElementTree.parse(file)
        root = tree.getroot()

        item_list = self.get_all_structures(root)
        class_list = self.get_class_model(file, item_list)

        return class_list
