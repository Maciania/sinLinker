from pathlib import Path
import xml.etree.ElementTree as etree


class ObjectMnemos:
    def __init__(self, objectDir_path):
        self.dir_path = objectDir_path


    def get_files_info(self):
        directory = Path(self.dir_path)
        # files = [f.name for f in directory.iterdir() if f.is_file() and f.name.startswith("Screen_")]
        # print(files)

        result = []

        id = 1
        for file in directory.iterdir():
            if file.is_file() and file.name.startswith("Screen_"):
                result.append([id, file, *self.get_header_data_omobj(file), self.get_count_object(file)])
                id += 1

        return result


    def get_header_data_omobj(self, file):
        tree = etree.parse(file)
        root = tree.getroot()

        name = root.attrib.get("name")
        uuid = root.attrib.get("uuid")

        return name, uuid

    def get_data_from_omobj(self, file):
        tree = etree.parse(file)
        root = tree.getroot()

        result = []

        # Ищем все объекты
        counter = 1
        for obj in root.findall(".//object"):
            name = obj.attrib.get("name")
            base_type = obj.attrib.get("base-type")

            # Находим init с target="_Path"
            # path_init = obj.find('init[@target="_Path"]')

            path_init = None
            path_ap = None
            for init in obj.findall("init"):  # перебираем все теги <init> внутри <object>
                if init.attrib.get("target") == "_Path":  # проверяем атрибут
                    path_init = init
                if init.attrib.get("target") == "_ApSource":  # проверяем атрибут
                    path_ap = init

                    # break  # нашли — можно выйти из цикла

            # path_ap = None
            # for ap in obj.findall("init"):  # перебираем все теги <init> внутри <object>
            #     if obj.attrib.get("target") == "_ApSource":  # проверяем атрибут
            #         path_ap = ap
            #         break  # нашли — можно выйти из цикла


            if path_init is not None and name:
                # print(path_init)
                value = path_init.attrib.get("value", "")

                try:
                    ap_value = path_ap.attrib.get("ref", "")
                except AttributeError:
                    ap_value = None

                result.append((counter, name, base_type, value, ap_value))
                counter += 1

        return result


    def get_count_object(self, file):
        tree = etree.parse(file)
        root = tree.getroot()

        # name = root.attrib.get("name")
        # uuid = root.attrib.get("uuid")

        count = 0

        # Ищем все объекты
        for obj in root.findall(".//object"):
            # name = obj.attrib.get("name")

            # Проверяем наличие init с target="_Path"
            has_path = any(
                init.attrib.get("target") == "_Path"
                for init in obj.findall("init")
            )

            if has_path:
                count += 1

        return count






