from pathlib import Path
import xml.etree.ElementTree as etree
from logger import setup_logger
import re


class ObjectMnemos:
    """ Класс для работы с мнесохемами в папке /objects """
    def __init__(self, objectDir_path):
        self.dir_path = objectDir_path
        self.logger = setup_logger()

    def get_files_info(self):
        """ Вернуть основную информацию о мнемосхеме
            id - № мнемосхемы по порядку
            file - абсолютный путь
            name - имя мнемо в проекте HMI
            uuid - идентификатор мнемо
            кол-во пиктограмм на мнеомхеме"""

        directory = Path(self.dir_path)

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
        """ Вернуть информацию по пиктограммам на нмемосхеме
        counter - № по порядку
        name - название пиктограммы в проекте HMI
        base_type - родительский тип (AI, AI_LSU и т.д.)
        value - значение в поле initPath
         ap_value - значение в поле Ap_Source
         """

        tree = etree.parse(file)
        root = tree.getroot()

        result = []

        # Ищем все объекты
        counter = 1
        for obj in root.findall(".//object"):
            name = obj.attrib.get("name")
            base_type = obj.attrib.get("base-type")

            path_init = None
            path_ap = None
            for init in obj.findall("init"):  # перебираем все теги <init> внутри <object>
                if init.attrib.get("target") == "_Path":  # проверяем атрибут
                    path_init = init
                if init.attrib.get("target") == "_ApSource":  # проверяем атрибут
                    path_ap = init

            if path_init is not None and name:
                value = path_init.attrib.get("value", "")

                try:
                    ap_value = path_ap.attrib.get("ref", "")
                except AttributeError:
                    ap_value = None

                result.append((counter, name, base_type, value, ap_value))
                counter += 1

        return result


    def get_count_object(self, file):
        """ Кол-во объектов с initPAth - т.е. пиктограммы """
        tree = etree.parse(file)
        root = tree.getroot()

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

    def data_from_ap_omobj(self):

        result = []

        ap_omobj_file = Path(self.dir_path + '/AP.omobj')
        if ap_omobj_file.is_file():

            tree = etree.parse(ap_omobj_file)
            root = tree.getroot()

            for obj in root.findall(".//object"):
                result.append(obj.attrib.get("name"))
                # result.append(name)

        return result


    def update_blockicons_data(self, file, obj_name, new_ap, new_initpath):
        """Обновить содержимое блокиконки через точечную текстовую замену"""

        path = Path(file)

        # Определяем кодировку
        encoding = "utf-8"
        with open(path, "rb") as f:
            first_line = f.readline()
            m = re.search(br'encoding="([^"]+)"', first_line)
            if m:
                encoding = m.group(1).decode()

        # Читаем исходный контент
        with open(path, 'r', encoding=encoding) as f:
            content = f.read()

        # Ищем объект по шаблону
        obj_pattern = rf'<object[^>]*name\s*=\s*["\']{re.escape(obj_name)}["\'][^>]*>.*?</object>'
        obj_match = re.search(obj_pattern, content, re.DOTALL | re.IGNORECASE)

        if not obj_match:
            print(f"Объект '{obj_name}' не найден в файле")
            return

        obj_content = obj_match.group(0)
        new_obj_content = obj_content

        # 1. Обновляем _ApSource (используем ref атрибут)
        if new_ap:
            # Находим полный тег init с _ApSource
            ap_pattern = r'<init\s+[^>]*?target\s*=\s*["\']_ApSource["\'][^>]*?/>'
            ap_match = re.search(ap_pattern, new_obj_content, re.IGNORECASE)

            if ap_match:
                old_tag = ap_match.group(0)
                # Убираем старые атрибуты value и ref, и слеш в конце
                clean_tag = re.sub(r'\s+(value|ref)\s*=\s*["\'][^"\']*["\']', '', old_tag)
                clean_tag = clean_tag.rstrip('/>').rstrip()
                # Создаем новый тег с ref атрибутом (без пробела перед />)
                new_tag = clean_tag + f' ref="{new_ap}"/>'
                new_obj_content = new_obj_content.replace(old_tag, new_tag)

        # 2. Обновляем _Path (используем value атрибут)
        if new_initpath:
            # Находим полный тег init с _Path
            path_pattern = r'<init\s+[^>]*?target\s*=\s*["\']_Path["\'][^>]*?/>'
            path_match = re.search(path_pattern, new_obj_content, re.IGNORECASE)

            if path_match:
                old_tag = path_match.group(0)
                # Убираем старый value атрибут и слеш в конце
                clean_tag = re.sub(r'\s+value\s*=\s*["\'][^"\']*["\']', '', old_tag)
                clean_tag = clean_tag.rstrip('/>').rstrip()
                # Создаем новый тег с value атрибутом (без пробела перед />)
                new_tag = clean_tag + f' value="{new_initpath}"/>'
                new_obj_content = new_obj_content.replace(old_tag, new_tag)

        # Заменяем объект в основном контенте
        if new_obj_content != obj_content:
            content = content.replace(obj_content, new_obj_content)

            # Записываем результат
            with open(path, 'w', encoding=encoding) as f:
                f.write(content)

            self.logger.info(f"Файл успешно обновлён с сохранением форматирования для {new_ap}, {new_initpath}")
        else:
            self.logger.info(f"Не было записи для {new_ap}, {new_initpath}")








