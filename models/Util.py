from models.ClassModel import ClassModel
from models.AttributeModel import AttributeModel
from models.MethodModel import MethodModel

import xml.etree.ElementTree as ET


class Util:
    def __init__(self, working_dir):
        self.working_dir = working_dir

    def save_to_xml(self, class_list):
        data = ET.Element('data')
        for class_item in class_list:
            try:
                class_element = ET.SubElement(data, 'class')
                # add class details
                class_name = ET.SubElement(class_element, 'name')
                class_name.text = class_item.get_name()
                superclass = ET.SubElement(class_element, 'superclass')
                superclass.text = class_item.get_super_class()
                class_file = ET.SubElement(class_element, 'file')
                class_file.text = class_item.get_file_path()

                # add attributes
                attrib_element = ET.SubElement(class_element, 'attributes')
                for attrib_item in class_item.get_attributes():
                    attrib = ET.SubElement(attrib_element, 'attribute')
                    attrib_name = ET.SubElement(attrib, 'name')
                    attrib_name.text = attrib_item.get_name()
                    attrib_type = ET.SubElement(attrib, 'type')
                    attrib_type.text = attrib_item.get_type()
                    attrib_call = ET.SubElement(attrib, 'calls')
                    attrib_call.text = attrib_item.get_calls()

                method_element = ET.SubElement(class_element, 'methods')
                for method_item in class_item.get_methods():
                    method = ET.SubElement(method_element, 'method')
                    method_name = ET.SubElement(method, 'name')
                    method_name.text = method_item.get_name()
                    method_type = ET.SubElement(method, 'type')
                    method_type.text = method_item.get_type()

                    locals_element = ET.SubElement(method, 'locals')
                    for attrib_item in method_item.get_locals():
                        local = ET.SubElement(locals_element, 'attribute')
                        attrib_name = ET.SubElement(local, 'name')
                        attrib_name.text = attrib_item.get_name()
                        attrib_type = ET.SubElement(local, 'type')
                        attrib_type.text = attrib_item.get_type()
                        attrib_call = ET.SubElement(local, 'calls')
                        attrib_call.text = str(attrib_item.get_calls())

                git_links_element = ET.SubElement(class_element,
                                                  'gitlinksbelow5')
                git_list = ",".join(class_item.get_git5_links())
                git_links_element.text = git_list

                git_links_element = ET.SubElement(class_element,
                                                  'gitlinkbelow10')
                git_list = ",".join(class_item.get_git10_links())
                git_links_element.text = git_list

                git_links_element = ET.SubElement(class_element,
                                                  'gitlinkbelow20')
                git_list = ",".join(class_item.get_git20_links())
                git_links_element.text = git_list

                git_links_element = ET.SubElement(class_element,
                                                  'gitlinktotal')
                git_list = ",".join(class_item.get_git_links_total()) #use .git_links_total instead of method because of set
                git_links_element.text = git_list

                code_related_element = ET.SubElement(class_element,
                                                     'codelinks')
                related_list = ",".join(class_item.get_structural_related_links())
                code_related_element.text = related_list
            except BaseException as e:
                print(e)

        # create xml
        try:
            _data = ET.tostring(data)
            file = open(self.working_dir + "\items_comm4.xml", "w+")
            file.write(_data.decode("utf-8"))
        except BaseException as e:
            print(e)

    def load_structure(self, file):
        class_list = set()

        tree = ET.parse(file)
        root = tree.getroot()

        try:
            for item in root.findall("class"):
                class_model = ClassModel()

                class_model.set_file(self.get_item_text_by_name(item, "file"))
                class_model.set_name(self.get_item_text_by_name(item, "name"))
                class_model.set_super_class(
                    self.get_item_text_by_name(item, "super"))

                attributes_item = self.get_item_by_name(item, "attributes")
                if attributes_item:
                    for attrib in attributes_item.findall("attribute"):
                        attribute_model = AttributeModel()
                        attribute_model.set_type(
                            self.get_item_text_by_name(attrib, "name"))
                        attribute_model.set_name(
                            self.get_item_text_by_name(attrib, "type"))
                        calls = self.get_item_text_by_name(attrib, "calls")
                        if calls is not None:
                            attribute_model.set_calls(int(calls))
                        else:
                            attribute_model.set_calls(0)
                        class_model.add_attribute(attribute_model)

                methods_item = self.get_item_by_name(item, "methods")
                if methods_item:
                    for method in methods_item.findall("method"):
                        method_model = MethodModel()

                        method_model.set_type(
                            self.get_item_text_by_name(method, "name"))
                        method_model.set_name(
                            self.get_item_text_by_name(method, "type"))

                        locals_item = self.get_item_by_name(method, "locals")
                        if locals_item:
                            for attrib in locals_item.findall("attribute"):
                                attribute_model = AttributeModel()
                                attribute_model.set_type(
                                    self.get_item_text_by_name(attrib, "name"))
                                attribute_model.set_name(
                                    self.get_item_text_by_name(attrib, "type"))
                                calls = self.get_item_text_by_name(
                                    attrib, "calls")
                                if calls is not None:
                                    attribute_model.set_calls(int(calls))
                                else:
                                    attribute_model.set_calls(0)
                                method_model.add_locals(attribute_model)

                        class_model.add_method(method_model)

                git_links5 = self.get_item_text_by_name(item, "gitlinksbelow5")
                if git_links5:
                    class_model.git_links_below5 = git_links5.split(',')

                git_links10 = self.get_item_text_by_name(
                    item, "gitlinkbelow10")
                if git_links10:
                    class_model.git_links_below10 = git_links10.split(',')

                git_links20 = self.get_item_text_by_name(
                    item, "gitlinkbelow20")
                if git_links20:
                    class_model.git_links_below20 = git_links20.split(',')

                git_links_total = self.get_item_text_by_name(
                    item, "gitlinktotal")
                if git_links20:
                    class_model.git_links_total = git_links_total.split(',')

                code_links = self.get_item_text_by_name(item, "codelinks")
                if code_links:
                    class_model.set_related(code_links.split(','))

                class_list.add(class_model)
        except BaseException as e:
            print(e)

        return class_list

    def get_text(self, atr):
        if atr is not None:
            text = atr.text
            return text
        else:
            return "None"

    def get_item_by_name(self, item, name):
        new = item.find(name)
        return new

    def get_item_text_by_name(self, item, name):
        new = item.find(name)
        return self.get_text(new)
