import xml.etree.ElementTree as ET
from datetime import datetime

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

    # def collect_object_paths(self, element, path_prefix=""):
    #     paths = []
    #     name = element.get("name")
    #     if name:
    #         current_path = f"{path_prefix}.{name}" if path_prefix else name
    #         children = element.findall("ct:object", namespaces=self.ns)
    #         if children:
    #             for child in children:
    #                 paths.extend(self.collect_object_paths(child, current_path))
    #         else:
    #             paths.append(current_path)
    #
    #
    #     return paths

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


    # def get_base_type_by_path(self, path: str):
    #     parts = path.split(".")
    #     current_element = self.application
    #
    #     for part in parts[1:]:  # пропускаем "Application"
    #         found = None
    #         for child in current_element.findall("ct:object", namespaces=self.ns):
    #             if child.get("name") == part:
    #                 found = child
    #                 break
    #         if found is None:
    #             raise ValueError(f"Путь '{path}' не найден (не удалось найти '{part}')")
    #         current_element = found
    #
    #     base_type = current_element.get("base-type")
    #
    #     # if base_type == 'NoneType':
    #     #     print(f'NoneType определна для {path}')
    #
    #     return base_type

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

'''
    # Получение списка имен объектов в AstraRegul => IOS_App => SinLib
    def get_SinLib_struct(self):
        # рабочая ветка
        sinLibLst = []
        AstraRegul = self.omx.find('{automation.deployment}domain')
        IosApp = AstraRegul.find('{automation.deployment}application-object')
        for logicObj in IosApp:
            if logicObj.get('name') == 'SinLib':
                for obj in logicObj:
                    sinLibLst.append(obj.get('name'))

        return sinLibLst

    # Получить тип объекта в директории SinLib
    def get_Obj_base_type(self, obj_name):
        AstraRegul = self.omx.find('{automation.deployment}domain')
        IosApp = AstraRegul.find('{automation.deployment}application-object')
        for logicObj in IosApp:
            if logicObj.get('name') == 'SinLib':
                for obj in logicObj:
                    if obj.get('name') == obj_name:
                        return obj.get('base-type').split('.')[-2]

        return None

    # Получить путь объекта по имени в директории SinLib
    def get_Obj_node_path(self, obj_name):
        AstraRegul = self.omx.find('{automation.deployment}domain')
        IosApp = AstraRegul.find('{automation.deployment}application-object')
        for logicObj in IosApp:
            if logicObj.get('name') == 'SinLib':
                for obj in logicObj:
                    if obj.get('name') == obj_name:
                        return '.'.join(obj.get('original').split('.')[
                                        3:])  # Возвращаем путь после 'REGUL_R500_51_1_A', 'Runtime', 'SDM_app'

        return None

    # Получить путь объекта по имени в директории SinLib
    def get_Obj_node_id(self, obj_name):
        AstraRegul = self.omx.find('{automation.deployment}domain')
        IosApp = AstraRegul.find('{automation.deployment}application-object')
        for logicObj in IosApp:
            if logicObj.get('name') == 'SinLib':
                for obj in logicObj:
                    if obj.get('name') == obj_name:
                        return obj.get('original').split('.')[-1]

        return None

    # Получить тип библиотеки из которой экземпляром которой является объект
    def get_Obj_library_type(self, obj_name):
        AstraRegul = self.omx.find('{automation.deployment}domain')
        IosApp = AstraRegul.find('{automation.deployment}application-object')
        for logicObj in IosApp:
            if logicObj.get('name') == 'SinLib':
                for obj in logicObj:
                    if obj.get('name') == obj_name:
                        return obj.get('base-type').split('.')[1]

        return None

    # Получить список объектов (папок с объектами) в IosApp
    def get_objects_iosApp(self):
        return [logicObj.get('name') for logicObj in self.IosApp]

    # Список типов (AI, DI, VLVA и т.д.) внутри объекта (SDM, NS1, NOR и т.д.)
    def get_types_in_iosApp(self, iosAppObj):
        for logicObj in self.IosApp:
            if logicObj.get('name') == iosAppObj:
                return [obj.get('name') for obj in logicObj]

        return None

    # Список названий объектов по пути iosAppObj (SDM, UKL, UPOV) -> iosAppObjType (DI, AI)
    def get_objName(self, iosAppObj, iosAppObjType):
        for logicObj in self.IosApp:
            if logicObj.get('name') == iosAppObj:
                for typesObj in logicObj:
                    if typesObj.get('name') == iosAppObjType:
                        return [obj.get('name') for obj in typesObj]

        return None

    # Вернуть базовый библиотечный тип этого объекта
    # iosAppObj - папка принадлежащая объекту
    # iosAppObjType - папка с типом объектов
    def get_base_type(self, iosAppObj, iosAppObjType, obj_name):
        for logicObj in self.IosApp:
            if logicObj.get('name') == iosAppObj:
                for typesObj in logicObj:
                    if typesObj.get('name') == iosAppObjType:
                        for obj in typesObj:
                            if obj.get('name') == obj_name:
                                return obj.get('base-type').split('.')[-2]

        return None

    # Вернуть название библиотеки экземпляром которой является этот объект
    def get_lib_name(self, iosAppObj, iosAppObjType, obj_name):
        for logicObj in self.IosApp:
            if logicObj.get('name') == iosAppObj:
                for typesObj in logicObj:
                    if typesObj.get('name') == iosAppObjType:
                        for obj in typesObj:
                            if obj.get('name') == obj_name:
                                return obj.get('base-type').split('.')[-4]

    # Получить путь объекта по имени в директории
    def get_node_path(self, iosAppObj, iosAppObjType, obj_name):
        for logicObj in self.IosApp:
            if logicObj.get('name') == iosAppObj:
                for typesObj in logicObj:
                    if typesObj.get('name') == iosAppObjType:
                        for obj in typesObj:
                            if obj.get('name') == obj_name:
                                return '.'.join(obj.get('original').split('.')[
                                                3:])  # Возвращаем путь после 'REGUL_R500_51_1_A', 'Runtime', 'SDM_app'

        return None

    # Получить путь объекта по имени в директории
    def get_node_id(self, iosAppObj, iosAppObjType, obj_name):
        for logicObj in self.IosApp:
            if logicObj.get('name') == iosAppObj:
                for typesObj in logicObj:
                    if typesObj.get('name') == iosAppObjType:
                        for obj in typesObj:
                            if obj.get('name') == obj_name:
                                return obj.get('original').split('.')[-1]

        return None
'''

