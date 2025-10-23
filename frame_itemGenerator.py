import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from datetime import datetime
# import random
import re

# from lxml.parser import result

from gui import MyFileDialog, MyComboBox, MyScrollText, MyLabelFrame, ControlField, UniversalTable
from libOmx import LibOmxFile
from map import MapFile
from omx import OmxFile
# import SinLib
from excell import ConfExcellFile


class FrameItemGenerator(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.myMap = None
        self.myOmx = None
        self.myLibOmx = None
        self.ConfExcell = None
        self.itemsInExcell = [] # Список с укрупненными данными с конфигуратора
        self.instAppDict = []
        self.instApp = []
        self.link_dict = {} # Словарь node_path:nodeId выбранной строки

        self.help_info = {
            'omx': {'title':
                            'Omx файл проекта или модуля',
                        'label':
                            'Файл модуля проекта с расширением .omx\n'
                            'Находится в директории проекта по пути: DS_PROJ\\PLC_GMO\\Regul\\Основной ПЛК 1 АСУТП Щитовой КиП1 \n'
                            'если необходимо подвязать карту для Основной ПЛК 1 АСУТП Щитовой КиП1\n'
                            'аналогично можно сделать для любого модуля с картой OPCUA\n'
                            'из этого файла собирается информация по всем существующим экземплярам которые необходимо подвязать в карте'},

            'map': {'title':
                            'Файл карты адресов в модуле',
                        'label':
                            'Файл карты адресов с расширением .xml\n'
                            'Находится в директории проекта по пути: DS_PROJ\\PLC_GMO\\Regul\\Основной ПЛК 1 АСУТП Щитовой КиП1\\GMO_30_PLC_R1\\DS_Maps\n'
                            'В этот файл добавляются секции xml для экземпляров из модуля проекта omx:'},

            'libOmx': {'title':
                            'Omx файл библиотеки со всеми типовыми объектами',
                        'label':
                            'Файл модуля проекта с раcширением .omx\n'
                            'Находится в директории проекта по пути: DS_LIB\\Lib \n'
                            'из этого файла берется структура тегов для каждого эксземпляра в OMX модуле'},

            'conf_excell': {'title':
                           'Файл конфигуратора для проекта ПЛК',
                       'label':
                           'Файл конфигуратора excell c раcширением .xlsx или .xlsm\n'
                           'Из файла собирается информация по всем вкладкам dbAI, dbDI и т.д. \n'
                           '(обязательно использовать стандратные наименования вкладок) \n'
                           'На каждом лиcте должна быть строка с item (число) и Enum_name (строка типа _90_11_FIT1)\n'
                            'Которая должна соотвествовать экземпляру в модуле проекта типа Application._90_11.FIT1\n'
                           'В программе происходит поиск по соответствию Application._90_11.FIT1 и _90_11_FIT1'}

                }


        self.create_widgets()
        self.pack_widgets()




    def create_widgets(self):
        self.fields = {
            'module_dir': MyFileDialog(self, 'Путь к папке с модулем :', 'Открыть', cmd=self.select_module_dir,
                                       help_title=self.help_info['omx']['title'],
                                       help_label=self.help_info['omx']['label']),
            'omx': MyFileDialog(self, 'Файл проекта OMX :', 'Открыть', cmd=self.select_omx_file, help_title= self.help_info['omx']['title'], help_label=self.help_info['omx']['label']),
            'map': MyFileDialog(self, 'Файл карты :', 'Открыть', cmd=self.select_map_file, help_title= self.help_info['map']['title'], help_label=self.help_info['map']['label']),
            'libOmx': MyFileDialog(self, 'Файл библиотеки Lib :', 'Открыть', cmd=self.select_libOmx_file, help_title= self.help_info['libOmx']['title'], help_label=self.help_info['libOmx']['label']),
            'conf_excell': MyFileDialog(self, 'Конфигуратор Excell:', 'Открыть', cmd=self.select_conf_excell_file, help_title= self.help_info['conf_excell']['title'], help_label=self.help_info['conf_excell']['label']),
            # 'conType': MyComboBox(self, 'Тип привязки объектов', None),
            # 'table': MyTable(self, bindRowCLick=self.bindRowCLick),
            'table': UniversalTable(self,
                                    columns=("#1", "#2", "#3", "#4", "#5"),
                                    headings=("ID", "Тип", "Кол-во", "Библиотека", "Статус подвязки"),
                                    widths=(30, 120, 80, 100, 120),
                                    insert_rule=self.mytable_insert_rule,
                                    highlight_rules={
                                            'highlight_yellow': ('yellow', 'black'),
                                            'highlight_red': ('red', 'white'),
                                            'highlight_black': ('black', 'yellow')
                                        },
                                    bindRowClick=self.insert_to_item_table
                                    ),
            'item_table': UniversalTable(self,
                                    columns=("#1", "#2", "#3", "#4"),
                                    headings=("№ п/п", "Enum_Name", "№ item", "Привязка"),
                                    widths=(30, 120, 120, 120),
                                    insert_rule=self.conntable_insert_rule,
                                    highlight_rules={
                                        'highlight_row': ('yellow', 'black')
                                    }
                                    ),
            'btn': ControlField(self,
                                ('Получить item', self.insert_to_table),
                                # ('Подвязать выбранное', self.link_one_instance),
                                ('Добавить item', self.insert_item))
        }

    def pack_widgets(self):
        order = ['omx', 'libOmx', 'map', 'conf_excell', 'table', 'item_table', 'btn']
        for w in order:
            widget = self.fields[w]
            if w == 'table':
                widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=3)
            else:
                widget.pack(fill=tk.X, padx=5, pady=3)
            if w == 'conType':
                self.fields['conType'].setValues(['Через конфигуратор ПЛУ', 'Нумерация Item по текущему экземпляру'])

    # ------------------------------
    # Методы для вкладки 1
    # ------------------------------
    def select_module_dir(self):
        """ Выбор директории c модулем (сокращаем действия на 2 действия)"""

        # dirname = fd.askdirectory(initialdir=os.getcwd())
        dirname = fd.askdirectory(initialdir='C:\\Users\\sinetic\\Desktop\\new_mak_zif\\DS_PROJ\\PLC_GMO\\Regul')

        if dirname:

            found_path = self.find_dir_upwards(dirname, "DS_LIB")

            if found_path:
                print(f"Папка DS_LIB найдена: {found_path}")
                for lib_path in os.listdir(found_path):
                    if os.path.isdir(os.path.join(found_path, lib_path)) and lib_path.lower() == 'lib':
                        full_lib_path = os.path.join(found_path, lib_path)
                        for lib in os.listdir(full_lib_path):
                            if os.path.isfile(os.path.join(full_lib_path, lib)) and os.path.splitext(os.path.join(full_lib_path, lib))[1] == '.omx':
                                full_lib_omx_file = os.path.join(full_lib_path, lib)
                                # print(full_lib_omx_file)
                                self.fields['libOmx'].setNewTxt(full_lib_omx_file)
                                self.myLibOmx = LibOmxFile(omx_path=full_lib_omx_file)

            else:
                print("Папка DS_LIB не найдена выше по дереву.")

            self.fields['module_dir'].setNewTxt(dirname)
            for module_path in os.listdir(dirname):
                if os.path.isdir(os.path.join(dirname, module_path)):
                    full_module_path = os.path.join(dirname, module_path)
                    for omx_path in os.listdir(full_module_path):
                        # Ищем omx файл проекта модуля
                        if os.path.isfile(os.path.join(full_module_path, omx_path)) and os.path.splitext(os.path.join(full_module_path, omx_path))[1] == '.omx':
                            full_omx_path = os.path.join(full_module_path, omx_path)
                            # print(omx_path)
                            self.fields['omx'].setNewTxt(full_omx_path)
                            self.myOmx = OmxFile(omx_path=full_omx_path)
                            self.instApp = self.myOmx.get_instance_list()

                        # Здесь можно найти карту
                        if os.path.isdir(os.path.join(full_module_path, omx_path)) and omx_path == 'DS_Maps':
                            ds_map_dir = os.path.join(full_module_path, omx_path)
                            for map in os.listdir(ds_map_dir):
                                if 'diagn' not in map.lower():
                                    full_map_path = os.path.join(ds_map_dir, map)
                                    # print(map)
                                    self.fields['map'].setNewTxt(full_map_path)
                                    self.myMap = MapFile(map_path=full_map_path)


    # Ищем директорию DS_LIB и возвращаем полный путь
    def find_dir_upwards(self, start_path, target_dir_name):
        """ Метод для поиска """
        current_dir = os.path.abspath(start_path)

        while True:
            # Проверяем, есть ли нужная папка в текущей директории
            possible_path = os.path.join(current_dir, target_dir_name)
            if os.path.isdir(possible_path):
                return possible_path

            # Поднимаемся на уровень выше
            parent_dir = os.path.dirname(current_dir)

            # Если дошли до корня — выходим
            if parent_dir == current_dir:
                return None

            current_dir = parent_dir


    def select_omx_file(self):
        filename = fd.askopenfilename(filetypes=[('OMX files', '*.omx')])
        if filename:
            self.fields['omx'].setNewTxt(filename)
            self.myOmx = OmxFile(omx_path=filename)
            self.instApp = self.myOmx.get_instance_list()

    def select_map_file(self):
        filename = fd.askopenfilename(filetypes=[('XML files', '*.xml')])
        if filename:
            self.fields['map'].setNewTxt(filename)
            self.myMap = MapFile(map_path=filename)

    def select_libOmx_file(self):
        filename = fd.askopenfilename(filetypes=[('OMX files', '*.omx')])
        if filename:
            self.fields['libOmx'].setNewTxt(filename)
            self.myLibOmx = LibOmxFile(omx_path=filename)

    def select_conf_excell_file(self, cnt=0):
        """ Выбор файла эксель конфигуратора в котором есть связь itemId:Позиция экземпляра"""
        filename = fd.askopenfilename(title='Open a file', initialdir=os.getcwd(),
                                          filetypes=[('All files', '*.xlsx'), ('All files', '*.xlsm')])
        self.fields['conf_excell'].setNewTxt(filename)
        self.ConfExcell = ConfExcellFile(file_path=filename)
        self.ConfExcell.init_itemid_list()


    def get_obj_from_excell(self):
        """ Формируем таблицу с названиями вкладок на конфигураторе и кол-во item-ов на нем"""
        for item_type in self.ConfExcell.getSheetNames():
            print(item_type)
        for key, value in self.ConfExcell.items_list.items():
            print(key, len(value))


    def insert_to_table(self):
        """ Вставка данных по конфигуратору по существующим item из конфигуратора в таблицу """
        self.fields['table'].clear()
        i = 1
        for key, value in self.ConfExcell.items_list.items():
            self.fields['table'].insert(i, key, len(value), self.ConfExcell.items_lib.get(key), None)
            i += 1


    def insert_to_item_table(self, event):
        """ Вставка данных по конфигуратору по существующим item из конфигуратора в таблицу """
        self.fields['item_table'].clear()

        item_type = self.fields['table'].get_selected()[0][0]
        # print(self.fields['table'].get_selected()[0][0])

        """
        Фильтрует элементы списка, оставляя только те,
        где строка начинается с 'Application.<second_part>.',
        и возвращает список чисел из квадратных скобок.
        """
        res = [
            int(re.search(r'\[(\d+)\]', s).group(1))
            for s in self.instApp
            if s.startswith(f"Application.{item_type}.")
        ]

        i = 1
        for key, value in self.ConfExcell.items_list.get(item_type, {}).items():
            self.fields['item_table'].insert(i, key, value, "Существует" if value in res else None)
            i += 1

    def insert_item(self):
        """ Вставка выделенного item в Application модуля"""
        try:
            item_type = self.fields['table'].get_selected()[0][0]
            item_lib = self.fields['table'].get_selected()[0][1]
            item_id = self.fields['item_table'].get_selected()[0][0]
            item_id_num = self.fields['item_table'].get_selected()[0][1]
            print(item_type, item_id)

            self.myOmx.insert_object_at_end(
            parent_path=f"Application.{item_type}",
            name=f"{item_id_num}",
            base_type=f"{item_lib}",
            aspect="unit.Lib.Aspects.PLC",
            uuid="aed15cf9-d7a3-426d-8d5b-ade6523fbeb6"
            )

        except IndexError:
            print(f"Не выделена строка во второй таблице")

        # self.myOmx.save("C:\\Users\\sinetic\\Desktop\\sinLinker\\data_files\\GMO_30_PLC_R3_modified.omx")


    def get_obj(self):
        """
        Получить данные по экземплярам в application модуля с программой ПЛК
        """
        self.instAppDict.clear()
        self.instApp = self.myOmx.get_instance_list()
        self.fields['table'].clear()
        j = 0

        print(*self.instApp)

        for i in self.instApp:
            j += 1
            lib = self.myOmx.get_base_type_by_path(i)
            # print(
            #     f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Библиотека:{lib} для пути:{i}")
            item_id = self.get_item_id(i)
            # print(
            #     f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Путь:{i} Чарт:{self.myLibOmx.get_lib_prefix(lib)} item_id:{item_id}")

            conn_status = self.check_connection(i, lib)

            # if item_id is not None:
            self.instAppDict.append({'id': j, 'path': i, 'item_id': item_id, 'lib': lib, 'con_stat':conn_status})

        self.insert_to_map_table()
        # self.print_instAppDict()

    def insert_to_map_table(self):
        """ Вставка списка словарей self.instAppDict в таблицу 'table'"""

        for i in self.instAppDict:
            self.fields['table'].insert(i['id'], i['path'], i['item_id'], i['lib'], i['con_stat'])
        # self.fields['table'].highlightRow()


    def bindRowCLick(self, event):
        row_val = self.fields['table'].get_selected()[0]
        tag_list = self.myLibOmx.get_lib_tag_list(row_val[1])
        full_path_tag_list = [i[0] for i in tag_list]
        self.link_dict = self.check_link_one_instance(row_val[0], full_path_tag_list)
        self.fields['conTable'].clear()

        j = 0
        for i in tag_list:
            j += 1
            self.fields['conTable'].insert(j, i[0], i[1],self.link_dict[i[0]])
        # self.fields['conTable'].highlightRow()


    def check_link_one_instance(self, path:str, tag_list:list):
        """ Проверить подвязку по тегам одного экземпляра"""

        link_dict = {}
        for i in tag_list:
            link_dict.update({i:self.myMap.check_link(str(path+'.'+i))})
        return link_dict


    def link_one_instance(self):
        """ Создание и отправка секции с группой тегов по экземпляру в файл карты"""

        for item in self.fields['table'].get_selected():

            lib = self.myLibOmx.get_lib_prefix(item[1])
            node_path = item[0]
            item_id = self.get_item_id(node_path)

            tag_list = self.myLibOmx.get_lib_tag_list(item[1])
            full_path_tag_list = [i[0] for i in tag_list]
            link_dict = self.check_link_one_instance(item[0], full_path_tag_list)

            if 'None' in link_dict.values():

                # print(f'Привязка выбранного {lib}, {node_path}, {item_id}, словарь подвязок {link_dict}')

                if item_id is not None:
                    for tag, node_id in link_dict.items():
                        if node_id == "None":
                            xmlObj = self.myMap.create_XMLtag(lib, node_path, tag, item_id)
                            self.myMap.insert_XML_to_map(xmlObj)

        self.save_map()


    def get_item_id_from_tag(self, node_path):
        """ Получить item Id из экземпляра по его названию в проекте"""
        try:
            result = re.search(r'\[(\d+)]', node_path)
            if result:
                return result.group(1)
            else:
                return None
        except (AttributeError, TypeError) as e:
            print(f"Ошибка при обработке текста: {e}")
            return None


    def get_item_id(self, node_path):
        """ Получить значение itemId взависимости от выбранного режима подвязки в комбобоксе conType"""
        item_id = None

        con_type = self.fields['conType'].getId()

        if con_type == 0: # Через конфигуратор ПЛК
            item_id = self.get_item_id_from_config(node_path)

        if con_type == 1:  # По номеру item в названии
            item_id = self.get_item_id_from_tag(node_path)

        return item_id


    def get_item_id_from_config(self, node_path):
        """  Получить item Id экземпляра по соответствию в конфигураторе ПЛК на листе файла excell"""
        try:
            lib = self.myOmx.get_base_type_by_path(node_path)
            appStr = node_path.split('.')
            noAppPath = f'{appStr[-2]}_{appStr[-1]}'
            item_id = self.ConfExcell.getItemId(self.myLibOmx.get_lib_prefix(lib), noAppPath)
            if item_id:
                return item_id
            else:
                return None
        except (AttributeError, TypeError) as e:
            print(f"Ошибка при обработке текста: {e}")
            return None


    def write_to_map(self):
        """ Проход по экземплярам, затем по тегам экземпляров, создание XML структур и добавление их в файл """

        for i in self.instAppDict:
            if i['item_id'] not in ["None", 'none', None]:
                full_path_tag_list = [j[0] for j in self.myLibOmx.get_lib_tag_list(i['lib'])]
                print('******************')
                print(*full_path_tag_list)
                for tag, node_id in self.check_link_one_instance(i['path'], full_path_tag_list).items():
                    self.myMap.insert_XML_to_map(self.myMap.create_XMLtag(self.myLibOmx.get_lib_prefix(i['lib']), i['path'], tag, i['item_id']))
        self.save_map()
        # self.fields['table'].highlightRow()


    def check_connection(self, path:str ,lib:str):
        """ Проверка привязки по всем эксземплярам и всем тегам каждого экземпляра"""
        # for i in self.instAppDict:
        conn_list = []
        full_path_tag_list = [j[0] for j in self.myLibOmx.get_lib_tag_list(lib)]
        for tag, node_id in self.check_link_one_instance(path, full_path_tag_list).items():
            if node_id == "None":
                conn_list.append(False)
            else:
                conn_list.append(True)

        if len(conn_list) > 0:
            set_list = set(conn_list)
        else:
            return "Нет секции в Lib"

        # print(f'Список статусов подвязки тегов в экземплярах: {conn_list}')
        # print(f'Множество статусов подвязки тегов в экземплярах: {set_list}')

        conn_list.clear()
        if len(set_list) == 2:
            return 'Частично'
        if True in set_list:
            return 'Полностью'
        return 'Отсутствует'

    # сохранить тег в файл
    def save_map(self):
        self.myMap.write_XML_to_map()

    def mytable_insert_rule(self, values):
        obj_id, obj_name, obj_type, base_type, con_status = values
        tags = ()
        if con_status == 'Частично':
            tags = ('highlight_yellow',)
        elif con_status == 'Отсутствует':
            tags = ('highlight_red',)
        elif con_status == 'Нет секции в Lib':
            tags = ('highlight_black',)
        return values, tags

    def conntable_insert_rule(self, values):
        i, obj_id, obj_type, conn_status = values
        tags = ('highlight_row',) if conn_status == 'None' else ()
        return values, tags