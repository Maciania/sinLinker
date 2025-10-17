from lxml import etree

class LibOmxFile:
    def __init__(self, omx_path):
        self.file_path = omx_path
        self.tree = etree.parse(self.file_path)
        self.ns = {
            "ct": "automation.control",
            "sys": "system"
        }
        self.root = self.tree.getroot()

        self.dbDict = {'AI': {'OPC_UA':'dbAI','S7':'dbAI', 'ModbusTCP':'dbAI'},
                       'DI': {'OPC_UA': 'dbDI', 'S7': 'dbDI', 'ModbusTCP': 'dbDI'},
                       'Conv': {'OPC_UA': 'dbConv', 'S7': 'dbConv', 'ModbusTCP': 'dbConv'},
                       'Valve': {'OPC_UA': 'dbValve', 'S7': 'dbValve', 'ModbusTCP': 'dbValve'},
                       'ValveReg': {'OPC_UA': 'dbValveReg', 'S7': 'dbValveReg', 'ModbusTCP': 'dbValveReg'},
                       'PID': {'OPC_UA': 'dbPID', 'S7': 'dbPID', 'ModbusTCP': 'dbPID'},
                       'Motor': {'OPC_UA': 'dbMotor', 'S7': 'dbMotor', 'ModbusTCP': 'dbMotor'},
                       'ARS': {'OPC_UA': 'dbARS', 'S7': 'dbARS', 'ModbusTCP': 'dbARS'},
                       'DO': {'OPC_UA': 'dbDO', 'S7': 'dbDO', 'ModbusTCP': 'dbDO'},
                       'Lock': {'OPC_UA': 'dbLock', 'S7': 'dbLock', 'ModbusTCP': 'dbLock'},
                       'AM': {'OPC_UA': 'dbAM', 'S7': 'dbAM', 'ModbusTCP': 'dbAM'},
                       'DM': {'OPC_UA': 'dbDM', 'S7': 'dbDM', 'ModbusTCP': 'dbDM'},
                       'AUTO': {'OPC_UA': 'dbAuto', 'S7': 'dbAuto', 'ModbusTCP': 'dbAuto'},
                       'Crusher': {'OPC_UA': 'dbCrush', 'S7': 'dbCrush', 'ModbusTCP': 'dbCrush'},
                       'PS': {'OPC_UA': 'dbPS', 'S7': 'dbPS', 'ModbusTCP': 'dbPS'},
                       'AO': {'OPC_UA': 'dbAO', 'S7': 'dbAO', 'ModbusTCP': 'dbAO'},
                       'MotorDP': {'OPC_UA': 'dbMotorDP', 'S7': 'dbMotorDP', 'ModbusTCP': 'dbMotorDP'},
                       'ThickenLift': {'OPC_UA': 'dbThickenLift', 'S7': 'dbThickenLift', 'ModbusTCP': 'dbThickenLift'},
                       'ThickenRot': {'OPC_UA': 'dbThickenRot', 'S7': 'dbThickenRot', 'ModbusTCP': 'dbThickenRot'}
                        }

    def collect_member_paths(self, element, prefix=""):
        paths = []
        name = element.get("name")
        current_path = f"{prefix}.{name}" if prefix else name

        children = element.findall("ct:object", namespaces=self.ns)
        if children:
            for child in children:
                paths.extend(self.collect_member_paths(child, current_path))
        else:
            paths.append(current_path)
        return paths

    def get_type_members_from_namespace_path(self, path: str):
        """
        Использует XPath для поиска строго вложенных <namespace> и <ct:type>:
        Пример входа: Types.Valve.OPC_UA.Valve_PLC
        """
        parts = path.split(".")
        *namespace_parts, type_name = parts

        # Собираем XPath путь: namespace/.../namespace/ct:type[@name=...]
        xpath_query = ""
        for ns in namespace_parts:
            xpath_query += f"/sys:namespace[@name='{ns}']"
        xpath_query += f"/ct:type[@name='{type_name}']"

        # Выполняем поиск
        result = self.root.xpath(xpath_query, namespaces=self.ns)
        if not result:
            raise ValueError(f"Тип '{type_name}' не найден по пути '{path}'")
        type_element = result[0]

        # Собираем пути вложенных членов
        return self.collect_member_paths(type_element)

    def get_lib_prefix(self, full_lib_path: str):
        """ Получить префикс библиотеки по пути к библиотеке"""
        # try:
        #     full_lib = full_lib_path.split('.')
        # except Exception as e:
        #     print(f"Проблема в секции библиотеки lib: {e} для поиска типа экземпляра {full_lib_path}")

        full_lib = full_lib_path.split('.')

        try:
            value = self.dbDict[full_lib[-3]][full_lib[-2]]
        except KeyError:
            value = 'none'
        finally:
            return value



        # return self.dbDict[full_lib[-3]][full_lib[-2]]


    def get_lib_tag_list(self, path: str):
        """
        Получить список сокетов с тегами и отдельно тегов внутри секции (unit.Lib.Types.AI.OPC_UA.AI_PLC)
        """
        tag_list = []
        pathList = path.split('.')

        # print(pathList)
        #
        # print(pathList[2], pathList[-4])
        # print(pathList[3], pathList[-3])
        # print(pathList[4], pathList[-2])



        for i1 in self.root.xpath("sys:namespace", namespaces=self.ns):
            types = i1.get("name")
            if types == pathList[-4]:
                found_types = i1
                # print(f"\n{found_types}НАЙДЕН!!!!!!!!!!!!:")
                break
            # if found is None:
            #     raise ValueError(f"Путь '{path}' не найден (не удалось найти '{part}')")


        for i2 in found_types.xpath("sys:namespace", namespaces=self.ns):
            obj = i2.get("name")
            if obj == pathList[-3]:
                found_obj = i2
                # print(f" found_obj = {found_obj}")
                # print(f"found_obj = {etree.tostring(found_obj, pretty_print=True, encoding='unicode')}")
                break

        for i3 in found_obj.xpath("sys:namespace", namespaces=self.ns):
            protocol = i3.get("name")
            if protocol == pathList[-2]:
                found_protocol = i3
                # print(f"found_protocol = {found_protocol}")
                # print(f"found_protocol = {etree.tostring(found_protocol, pretty_print=True, encoding='unicode')}")
                break

        for i4 in found_protocol.xpath("ct:type", namespaces=self.ns):
            aspect = i4.get("name")
            # print(f"cur found_aspect = {aspect}")
            if aspect == pathList[-1]:
                found_aspect = i4
                # print(f"found_aspect = {etree.tostring(found_aspect, pretty_print=True, encoding='unicode')}")
                # print(f"found_aspect = {found_aspect}")
                break

        try:
            for i5 in found_aspect.xpath("ct:socket", namespaces=self.ns):
                # Ищем в сокете атрибут "Имя узла в OPC"
                node_attr = i5.xpath(".//*[local-name()='attribute' and @type='unit.Server.Attributes.NodeRelativePath']")

                # Если он найден
                if node_attr:
                    node_relative_path_value = node_attr[0].get("value")

                for i6 in i5.xpath("ct:socket-parameter", namespaces=self.ns):
                    # Если в сокете есть атрибут имя узла в OPC
                    if node_attr:
                        # Если ему присвоено значение то добавим его в путь тега иначе пусто
                        if node_relative_path_value:
                            tag_list.append([f"{node_relative_path_value}.{i6.get("name")}", i6.get("type")])
                        else:
                            tag_list.append([i6.get("name"), i6.get("type")])
                    # Если в сокете нет такого атрибута, то добавляем в путь название атрибута
                    else:
                        tag_list.append([f"{i5.get("name")}.{i6.get("name")}", i6.get("type")])

        except UnboundLocalError:
            print(f"Сокеты не обнаружены переходим к поиску параметров для типа: {found_types}, объекта: {found_obj}, протокола: {found_protocol}.\n Нет секции для этого типа в Lib.omx")


        try:
            for i7 in found_aspect.xpath("ct:parameter", namespaces=self.ns):
                tag_list.append([f"{i7.get("name")}", i7.get("type")])
                # print(f"***parameter***{i7.get("name")}***")
        except UnboundLocalError:
            print(f"Найденная секция не подходит под шаблон для типа: {found_types}, объекта: {found_obj}, протокола: {found_protocol}.\n Нет секции для этого типа в Lib.omx")

        return tag_list
