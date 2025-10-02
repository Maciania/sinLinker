import xml.etree.ElementTree as ET


class MapFile:
    def __init__(self, map_path):
        self.path = map_path
        self.tree = ET.parse(self.path)
        self.file = self.tree.getroot()


    # Получение списка тегов в карте для папки SinLib
    def get_link_for_SinLib(self):
        linkObj = []
        # Все что в карте адресов с из папки SinLib
        for child in self.file.findall('item'):
            node_path = child.find('node-path').text
            if node_path.find('SinLib') != -1:
                linkObj.append(node_path)

        return linkObj

    # Проверка objName на хотябы одну запись в карте адресов для папки SinLib
    def check_linking(self, objName):
        linkObj = []
        # Все что в карте адресов с из папки SinLib
        for child in self.file.findall('item'):
            node_path = child.find('node-path').text
            if node_path.find('SinLib') != -1 and node_path.find(objName) != -1:
                return True  # Есть привязка
        return False  # Нет привязки

    def checkLink(self, obj, type, objName):
        for child in self.file.findall('item'):
            node_path = child.find('node-path').text
            if node_path.find(obj) != -1 and node_path.find(type) != -1 and node_path.find(objName) != -1:
                return True  # Есть привязка
        return False  # Нет привязки

    # def check_link(self, full_tag_path):
    #     """ Проверка на секцию с тегом в карте"""
    #     for child in self.file.findall('item'):
    #         node_path = child.find('node-path').text
    #         if node_path.find(full_tag_path) != -1:
    #             return True  # Есть привязка
    #     return False  # Нет привязки

    def check_link(self, full_tag_path):
        """Проверка на секцию с тегом в карте и возврат nodeId при наличии"""
        for child in self.file.findall('item'):
            node_path_elem = child.find('node-path')
            if node_path_elem is not None and node_path_elem.text:
                if full_tag_path in node_path_elem.text:
                    node_id_elem = child.find('nodeId')
                    if node_id_elem is not None:
                        return node_id_elem.text  # Возвращаем nodeId
        return 'None'  # Нет совпадения




    # Создаем структуру тега в XML виде
    # node_path - путь к тегу в AStudio, например SinLib.mtr1.HMI_CMD
    # node_id - путь к тегу в OPC (UAExpert), например Application.MTR_MTR1.sMtr.HmiCmd
    def create_XMLtag(self, lib, node_path, tag, item_id):

        newObj = ET.Element('item', Binding='Introduced')
        ET.indent(newObj, space='   ', level=0)

        tagStruct = {
            'node-path': f'{node_path}.{tag}',
            'namespace': 'urn:ProsoftSystems:regul_ua_server:iec_data',
            'nodeIdType': 'String',
            'nodeId': f'Application.{lib}.Item[{item_id}].{tag}',
        }

        for key, value in tagStruct.items():
            ET.SubElement(newObj, key).text = value
            ET.indent(newObj, space='   ', level=1)

        # ET.dump(newObj)
        return newObj

    # Вставка объекта xmlObj в файл
    def insert_XML_to_map(self, xmlObj):
        self.file.insert(len(self.file), xmlObj)
        ET.indent(self.file, space='\t', level=0)

    def write_XML_to_map(self):
        self.tree.write(self.path)
        print("**** Запись в файл ****")


class AttrMapFile:
    def __init__(self, map_path):
        self.file = ET.parse(map_path).getroot()
        self.file_path = map_path

    def get_attr(self):
        """Возвращает список всех item в формате (cnt, id, value)"""
        items = []
        cnt = 0
        for item in self.file.findall('item'):
            cnt += 1
            item_id = item.get('id')
            item_value = item.get('value')
            # items.append((cnt, item_id, item_value))
            items.append({'cnt':cnt, 'id': item_id, 'value':item_value, 'newValue':None})
            # print(f"cnt:{cnt}, ID: {item_id}, Value: {item_value}")
        return items

    def set_attr_value(self, item_id: str, new_value: str) -> bool:
        """Изменяет значение value для элемента с заданным id.
        Возвращает True, если изменение прошло успешно, False, если элемент не найден."""
        for item in self.file.findall('item'):
            if item.get('id') == item_id:
                item.set('value', new_value)
                return True
        return False

    def save_to_file(self):
        """Сохраняет изменения в XML файл"""
        tree = ET.ElementTree(self.file)
        tree.write(self.file_path, encoding='utf-8', xml_declaration=True)



