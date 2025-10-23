import re
from xml.dom import minidom
import xml.etree.ElementTree as ET

from lxml import etree

class OmxFile:
    def __init__(self, omx_path):
        self.file_path = omx_path
        self.tree = etree.parse(self.file_path)
        self.ns = {"ct": "automation.control"}

        # Ищем Application
        self.application_nodes = self.tree.xpath('//ct:object[@name="Application"]', namespaces=self.ns)
        if not self.application_nodes:
            raise ValueError("Элемент <ct:object name='Application'> не найден.")
        self.application = self.application_nodes[0]


    def collect_object_paths(self, element, path_prefix=""):
        paths = []
        name = element.get("name")
        if name:
            current_path = f"{path_prefix}.{name}" if path_prefix else name

            # ищем всех детей, у которых локальное имя тега == "object"
            children = [
                child for child in element
                if child.tag.split("}")[-1] == "object"
            ]

            if children:
                for child in children:
                    paths.extend(self.collect_object_paths(child, current_path))
            else:
                paths.append(current_path)

        return paths


    def get_instance_list(self):
        object_paths = self.collect_object_paths(self.application)
        # for path in object_paths:
        #     print(path, self.get_base_type_by_path(path))
        return object_paths

    def get_base_type_by_path(self, path: str):
        parts = path.split(".")
        current_element = self.application

        for part in parts[1:]:  # пропускаем "Application"
            found = None

            # ищем всех детей, у которых локальное имя тега == "object"
            for child in current_element:
                if child.tag.split("}")[-1] == "object" and child.get("name") == part:
                    found = child
                    break

            if found is None:
                raise ValueError(f"Путь '{path}' не найден (не удалось найти '{part}')")

            current_element = found

        return current_element.get("base-type")

    def find_element_by_path(self, path: str):
        """Возвращает XML-элемент по dot-пути, например Application.dbPS"""
        parts = path.split(".")
        current = self.application
        for part in parts[1:]:
            found = None
            for child in current:
                if child.tag.split("}")[-1] == "object" and child.get("name") == part:
                    found = child
                    break
            if found is None:
                raise ValueError(f"Элемент '{part}' не найден по пути '{path}'")
            current = found
        return current


    def insert_object_at_end(self, parent_path: str, name: str, base_type: str, aspect: str, uuid: str):
        """
        Вставляет новый <object> в конец указанной ветки, сохраняя форматирование.
        """
        parent = self.find_element_by_path(parent_path)
        parent_name = parent.get("name")

        new_object_line = (
            f'<object name="{name}" '
            f'base-type="{base_type}" '
            f'aspect="{aspect}" '
            f'uuid="{uuid}"/>'
        )

        # 1️⃣ Получаем исходный XML как строку
        with open(self.file_path, 'r', encoding='utf-8') as f:
            original_xml = f.read()

        # Пытаемся найти фрагмент <object name="dbPS" ...> ... </object>
        pattern = re.compile(
            rf'(<[^>]*name="{parent_name}"[^>]*>)(.*?)(</[^>]*object\s*>)',
            re.DOTALL
        )

        match = pattern.search(original_xml)
        if not match:
            raise ValueError(f"Не найден XML-блок для '{parent_name}'")

        # Разделяем содержимое на начало, тело и конец
        start_tag, inner_xml, end_tag = match.groups()

        # 2️⃣ Определим уровень отступа
        indent_match = re.search(r'(\n[ \t]+)<object', inner_xml)
        indent = indent_match.group(1) if indent_match else "\n    "

        # 3️⃣ Вставляем новую секцию перед закрывающим тегом
        new_inner_xml = inner_xml.rstrip() + f"{indent}{new_object_line}\n"

        new_xml = original_xml.replace(match.group(0), f"{start_tag}{new_inner_xml}{end_tag}")

        # 4️⃣ Просто сохраняем без дополнительного форматирования
        new_path = self.file_path.replace(".omx", "_new.omx")
        with open(new_path, "w", encoding="utf-8") as f:
            f.write(new_xml)

        print(f"✅ Новый объект добавлен в '{parent_path}' (в конец) → {new_path}")
        return new_path

