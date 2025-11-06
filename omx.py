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
            # children = [
            #     child for child in element
            #     if child.tag.split("}")[-1] == "object"
            # ]

            children = [
                child for child in element
                if child.tag.split("}")[-1].endswith("object")
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


    def insert_object_at_end(
            self,
            parent_path: str,
            name: str,
            base_type: str,
            aspect: str,
            uuid: str,
            comment: str = "My Comment"
    ):
        """
        Вставляет новый <object> в конец указанной родительской секции,
        корректно обрабатывая вложенность и сохраняя оригинальные отступы
        (включая перед закрывающим </object> родителя).
        """
        parent = self.find_element_by_path(parent_path)
        parent_name = parent.get("name")

        with open(self.file_path, "r", encoding="utf-8") as f:
            xml = f.read()

        # 1️⃣ Ищем открывающий тег родителя
        open_pat = re.compile(rf'<object\b[^>]*\bname="{re.escape(parent_name)}"[^>]*>', re.MULTILINE)
        open_match = open_pat.search(xml)
        if not open_match:
            raise ValueError(f"Не найден XML-блок для '{parent_name}'")

        scan_pos = open_match.end()

        # 2️⃣ Ищем соответствующий закрывающий тег </object> родителя
        tag_iter = re.finditer(r'<(/)?object\b([^>]*)/?>', xml[scan_pos:], re.DOTALL)
        depth = 0
        closing_abs_start = None
        closing_abs_end = None
        for m in tag_iter:
            full = m.group(0)
            is_closing = m.group(1) == '/'
            self_closing = full.rstrip().endswith('/>')
            tag_start = scan_pos + m.start()
            tag_end = scan_pos + m.end()

            if is_closing:
                if depth == 0:
                    closing_abs_start = tag_start
                    closing_abs_end = tag_end
                    break
                else:
                    depth -= 1
            elif not self_closing:
                depth += 1

        if closing_abs_start is None:
            raise ValueError(f"Не удалось найти закрывающий </object> для '{parent_name}'")

        # 3️⃣ Вырезаем внутренности родителя
        inner_xml = xml[open_match.end():closing_abs_start]

        # 4️⃣ Определяем базовые отступы
        ind_match = re.search(r'\n([ \t]+)<object\b', inner_xml)
        base_indent = ind_match.group(1) if ind_match else "    "
        inner_indent = base_indent + "    "

        # Определяем отступ перед закрывающим тегом
        prefix_before_closing = xml[:closing_abs_start]
        last_newline = prefix_before_closing.rfind('\n')
        closing_indent = ""
        if last_newline != -1:
            after_nl = prefix_before_closing[last_newline + 1: closing_abs_start]
            closing_indent = re.match(r'([ \t]*)', after_nl).group(1) if after_nl else ""

        # 5️⃣ Формируем новый блок <object>
        new_object_block = (
            f"\n{base_indent}<object name=\"{name}\" uuid=\"{uuid}\" "
            f"base-type=\"{base_type}\" aspect=\"{aspect}\">\n"
            f"{inner_indent}<attribute type=\"unit.System.Attributes.Comment\" "
            f"value=\"{comment}\" xmlns=\"system\" />\n"
            f"{inner_indent}<attribute type=\"unit.Lib.Attributes.IO.ID_Item\" "
            f"value=\"{name}\" xmlns=\"system\" />\n"
            f"{base_indent}</object>"
        )

        # 6️⃣ Вставляем перед закрывающим тегом родителя с сохранением исходного отступа
        new_inner = inner_xml.rstrip() + new_object_block + f"\n{closing_indent}"
        new_xml = xml[:open_match.end()] + new_inner + xml[closing_abs_start:]

        # 7️⃣ Сохраняем
        new_path = self.file_path.replace(".omx", ".omx")
        with open(new_path, "w", encoding="utf-8") as f:
            f.write(new_xml)

        print(f"✅ Новый объект добавлен в '{parent_path}' → {new_path}")
        return new_path
