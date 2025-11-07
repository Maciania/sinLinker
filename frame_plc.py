import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from datetime import datetime
# import random
import re

from gui import MyFileDialog, MyComboBox, MyScrollText, MyLabelFrame, ControlField, UniversalTable
from libOmx import LibOmxFile
from map import MapFile
from omx import OmxFile
# import SinLib
from excell import ConfExcellFile


class FramePLC(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.myMap = None
        self.myOmx = None
        self.myLibOmx = None
        self.ConfExcell = None
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
            'omx': MyFileDialog(self, 'Файл проекта OMX :', 'Открыть', cmd=self.select_omx_file, help_title= self.help_info['omx']['title'], help_label=self.help_info['omx']['label']),
            'map': MyFileDialog(self, 'Файл карты :', 'Открыть', cmd=self.select_map_file, help_title= self.help_info['map']['title'], help_label=self.help_info['map']['label']),
            'libOmx': MyFileDialog(self, 'Файл библиотеки Lib :', 'Открыть', cmd=self.select_libOmx_file, help_title= self.help_info['libOmx']['title'], help_label=self.help_info['libOmx']['label']),
            'conf_excell': MyFileDialog(self, 'Конфигуратор Excell:', 'Открыть', cmd=self.select_conf_excell_file, help_title= self.help_info['conf_excell']['title'], help_label=self.help_info['conf_excell']['label']),
            'conType': MyComboBox(self, 'Тип привязки объектов', None),
            # 'table': MyTable(self, bindRowCLick=self.bindRowCLick),
            'table': UniversalTable(self,
                                    columns=("#1", "#2", "#3", "#4", "#5"),
                                    headings=("ID", "Название", "itemID", "Библиотека", "Статус подвязки"),
                                    widths=(30, 120, 80, 100, 120),
                                    insert_rule=self.mytable_insert_rule,
                                    highlight_rules={
                                            'highlight_yellow': ('yellow', 'black'),
                                            'highlight_red': ('red', 'white'),
                                            'highlight_black': ('black', 'yellow')
                                        },
                                    bindRowClick=self.bindRowCLick
                                    ),
            'conTable': UniversalTable(self,
                                    columns=("#1", "#2", "#3", "#4"),
                                    headings=("№", "Сигнал", "Тип", "Привязка"),
                                    widths=(30, 120, 120, 120),
                                    insert_rule=self.conntable_insert_rule,
                                    highlight_rules={
                                        'highlight_yellow': ('yellow', 'black'),
                                        'highlight_grey': ('grey77', 'black'),
                                    }
                                    ),
            'btn': ControlField(self,
                                ('Получить объекты', self.get_obj),
                                ('Подвязать выбранное', self.link_one_instance),
                                ('Полная привязка', self.write_to_map))
        }

    def pack_widgets(self):
        order = ['omx', 'libOmx', 'map', 'conType', 'conf_excell', 'table', 'conTable', 'btn']
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
    def select_omx_file(self):
        filename = fd.askopenfilename(filetypes=[('OMX files', '*.omx')])
        if filename:
            self.fields['omx'].setNewTxt(filename)
            self.myOmx = OmxFile(omx_path=filename)

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
        # print(f'row_val {row_val}')

        tag_list = self.myLibOmx.get_lib_tag_list(row_val[1])
        # print(f'tag_list {tag_list}')

        full_path_tag_list = [i[0] for i in tag_list]
        # print(f'full_path_tag_list {full_path_tag_list}')

        self.link_dict = self.check_link_one_instance(row_val[0], full_path_tag_list)
        # print(f'self.link_dict {self.link_dict}')

        self.fields['conTable'].clear()


        # lib = self.myLibOmx.get_lib_prefix(row_val[1])
        # node_path = row_val[0]
        # item_id = self.get_item_id(row_val[0])


        j = 0
        for i in tag_list:
            j += 1
            # Допишем в поле с номером информацию по расхождению пути с ожидаемым
            modifed_num = j

            # Обработка исключения для ПАЗов и Алармов
            expected_path = f'{row_val[0]}.{i[0]}'

            if 'dbEPS' in self.link_dict[i[0]]:
                expected_path = expected_path .replace('Item', 'AREA', 1)
            if 'dbAlarms' in self.link_dict[i[0]]:
                expected_path = expected_path.replace('Item', 'SZS', 1)

            #
            # print(f'желаемый тег {expected_path}')
            # if (expected_path == self.link_dict[i[0]]):
            #     print('Пути совпали')

            # Модификация первого столбца нижней таблицы с тегами
            if expected_path != self.link_dict[i[0]] and self.link_dict[i[0]] != 'None':
                modifed_num = f'{j} -есть расхождения*'


            self.fields['conTable'].insert(modifed_num, i[0], i[1],self.link_dict[i[0]])


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
                # print('******************')
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
        tags = ()
        if conn_status == 'None':
            tags = ('highlight_yellow',)
        elif str(i).endswith('*'):
            tags = ('highlight_grey',)
        return values, tags