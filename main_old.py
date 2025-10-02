# import sys
# import os
#
#
# def setup_logging():
#     if getattr(sys, 'frozen', False):
#         base_path = os.path.dirname(sys.executable)
#     else:
#         base_path = os.path.dirname(os.path.abspath(__file__))
#
#     log_path = os.path.join(base_path, "app.log")
#     log_file = open(log_path, "a", encoding="utf-8", buffering=1)  # buffering=1 = построчная запись
#     sys.stdout = log_file
#     sys.stderr = log_file
#
#     print("=" * 40)
#     print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Приложение запущено")
#
#
# # --- ВАЖНО: вызываем прямо тут ---
# setup_logging()
#
# from tkinter import filedialog as fd
# # import os
# from data_files import SinLib
# from libOmx import LibOmxFile
# from map import *
# from omx import *
# from gui import *
# from excell import *
# import random
# # import sys
# # from datetime import datetime
#
#
# class MapLinker(Frame):
#
#     def __init__(self):
#         super().__init__()
#
#         # создаем набор вкладок
#         notebook = ttk.Notebook()
#         notebook.pack(expand=True, fill=tk.BOTH)
#
#         # создаем пару фреймвов
#         self.frame1 = ttk.Frame(notebook)
#         self.frame2 = ttk.Frame(notebook)
#
#         self.myMap = None  # Экземпляр класса для карты
#         self.myOmx = None  # Экземпляр класса для OMX файла
#         self.master.title("Map Linker XML")
#         self.myAtrMap = None # Экземпляр класса для карты атрибутов
#         self.myExcell = None  # Экземпляр класса с экселем в котором есть связь экземпляр-атрибут
#         self.attrList = None  # Список атрибутов из карты атрибутов
#         self.ConfExcell = None # Экземпляр конфигуратора Эксель, который делает Саня
#         self.attrListExcell = None  # Список экземпляр-атрибут из экселя
#         self.attrListDict = [] # Список из словарей cnt, id, value, newValue
#         self.instApp = [] # Список экземпляров из выбранного модуля приложения ПЛК
#         self.link_dict = {} # Словарь node_path:nodeId выбранной строки
#         self.instAppDict = []  # Список из словарей  id, path, item_id, lib, con_stat для экземпляров в карте адресов
#
#         self.sheet = None # Лист файла excell
#         self.path_col = None # Столбец с path тега
#         self.atr_col = None # Столбец с записываемым атрибутом
#
#         # добавляем фреймы в качестве вкладок
#         notebook.add(self.frame1, text="Карта ПЛК")
#         notebook.add(self.frame2, text="Карта атрибутов")
#
#         # Описание окон help
#         self.help_info = {
#             'omx': ['Помощь по omx',
#                     'Файл проекта с расширением .omx\n'
#                     'Файл находится в директории проекта по пути: \AS\Li\n'
#                     'Утилиту нужно поместить по пути \AS\Li и при открытии появится файл с раширением .omx'],
#
#             'map': ['Помощь по карте подвязок',
#                     'Файл карты подвязок с расширением .xml\n'
#                     'Файл находится в директории проекта по пути: \AS\Li\n'
#                     'Утилиту нужно поместить по пути \AS\Li и при открытии появится файл с раширением .omx\n'
#                     'Правильно будет использовать утилиту на тестовом проекте, а затем через экспорт в AStudio\n'
#                     'выгрузить подвязки в xls формате и импортировать их в боевой проект, но можно и рискнуть'],
#
#             'iosObj': ['Помощь по выбору участка (ЛСУ) в IOS_APP',
#                        'Выбор папки с объектами для подвязки с определенной структурой\n'
#                        '1 уровень - Название участка (SDM, UKL, NSPT и т.д.)\n'
#                        '2 уровень - Тип объектов (AI, DI, MTR и т.д.)\n'
#                        '3 уровень - Объекты \n'
#                        'Обязательно создавать объекты в AStudio в IOS_APP именно в такой структуре!!!'],
#
#             'iosType': ['Помощь по выбору типов в IOS_APP',
#                         'Выбор папки с типом подвязываемого объекта внтури папки с названием участка\n'
#                         'Используются следующие названия:\n'
#                         'AI, DI, MTR, PID, VLVD, VLVA\n'
#                         'Обязательно создавать папки AStudio в IOS_APP именно с такими наименованиями!!!']
#         }
#         self.create_widgets()
#
#
#     def create_widgets(self):
#         # Создаем словарь полей как в оригинале
#         self.fields = {
#                 'omx': MyFileDialog(self.frame1, 'Файл проекта OMX :', 'Открыть', cmd=self.select_omx_file,
#                                     help_title=self.help_info.get('omx')[0], help_label=self.help_info.get('omx')[1]),
#                 'map': MyFileDialog(self.frame1, 'Файл карты :', 'Открыть', cmd=self.select_map_file,
#                                     help_title=self.help_info.get('map')[0], help_label=self.help_info.get('map')[1]),
#                 'libOmx': MyFileDialog(self.frame1, 'Файл библиотеки Lib :', 'Открыть', cmd=self.select_libOmx_file,
#                                 help_title=self.help_info.get('map')[0], help_label=self.help_info.get('map')[1]),
#                 'conf_excell': MyFileDialog(self.frame1, 'Конфигуратор Excell:', 'Открыть',
#                                       cmd=self.select_conf_excell_file,
#                                       help_title=self.help_info.get('omx')[0],
#                                       help_label=self.help_info.get('omx')[1]),
#                 'iosObj': MyComboBox(self.frame1, 'Список объектов в IosApp :', bindCombo=self.selected_iosApp,
#                                      help_title=self.help_info.get('iosObj')[0],
#                                      help_label=self.help_info.get('iosObj')[1]),
#                 'iosType': MyComboBox(self.frame1, 'Тип :', bindCombo=None,
#                                       help_title=self.help_info.get('iosType')[0],
#                                       help_label=self.help_info.get('iosType')[1]),
#                 'table': MyTable(self.frame1, bindRowCLick=self.bindRowCLick),
#                 'conTable': ConnTable(self.frame1),
#                 'log': MyScrollText(self.frame1),
#                 'nodePath': MyLabelFrame(self.frame1, 'NodePath :', bindEntry=self.connect_node_path),
#                 'nodeId': MyLabelFrame(self.frame1, 'NodeId :', bindEntry=self.connect_node_id),
#                 'btn': ControlField(self.frame1,
#                                     ('Получить объекты', self.get_obj),
#                                     ('Проверить подвязку', self.check_connection),
#                                     # ('Привязать один экземпляр', self.link_one_instance),
#                                     ('Полная привязка', self.get_itemId_from_excell)),
#
#                 'fd_atr': MyFileDialog(self.frame2, 'Файл карты атрибутов:', 'Открыть', cmd=self.select_attrMap_file,
#                                 help_title=self.help_info.get('omx')[0], help_label=self.help_info.get('omx')[1]),
#                 'fd_excell': MyFileDialog(self.frame2, 'Исходник Excell:', 'Открыть',
#                                 cmd=self.select_excell_file,
#                                 help_title=self.help_info.get('omx')[0],
#                                 help_label=self.help_info.get('omx')[1]),
#                 'table_attr': AttrTable(self.frame2),
#                 'btn_attr': ControlField(self.frame2,
#                                 ('Проверить файл Excell', self.get_attr_from_excell),
#                                 ('Записать в Альфу', self.write_attr_xml)),
#                 'cb_sheets': MyComboBox(self.frame2, 'Название листа в Excell:',
#                                 bindCombo=self.select_cb_sheets,
#                                 help_title=self.help_info.get('iosObj')[0],
#                                 help_label=self.help_info.get('iosObj')[1]),
#                 'cb_path_col': MyComboBox(self.frame2, 'Столбец с полным path:',
#                                     bindCombo=self.select_cb_path_col,
#                                     help_title=self.help_info.get('iosObj')[0],
#                                     help_label=self.help_info.get('iosObj')[1]),
#                 'cb_atr_col': MyComboBox(self.frame2, 'Столбец с записываемым атрибутом:',
#                                       bindCombo=self.select_cb_path_col,
#                                       help_title=self.help_info.get('iosObj')[0],
#                                       help_label=self.help_info.get('iosObj')[1]),
#             }
#
#             # Упаковываем все виджеты в столбец
#         self.pack_widgets()
#
#     # Упаковка по порядку через widgets_order
#     def pack_widgets(self):
#         widgets_order = [
#             'omx', 'libOmx', 'map', 'conf_excell', 'table','conTable',
#             'btn', 'fd_atr', 'fd_excell',
#             'cb_sheets','cb_path_col', 'cb_atr_col', 'table_attr', 'btn_attr'
#         ]
#
#         # Очистка перед переупаковкой (на случай повторного вызова)
#         for widget in self.fields.values():
#             widget.pack_forget()
#
#         # Упаковка в правильном порядке
#         for widget_name in widgets_order:
#             widget = self.fields[widget_name]
#             if widget_name in ['table', 'table_attr']:
#                 widget.pack(anchor=tk.W, padx=5, pady=2, fill=tk.BOTH, expand=True)
#             else:
#                 widget.pack(anchor=tk.W, padx=5, pady=3, fill=tk.X)
#
#
#     # Выбор OMX файла
#     def select_omx_file(self):
#         filename = fd.askopenfilename(title='Open a file', initialdir=os.getcwd(), filetypes=[('All files', '*.omx')])
#         self.fields['omx'].setNewTxt(filename)
#         self.myOmx = OmxFile(omx_path=filename)
#         # self.myOmx.get_instance_list()
#         # self.get_obj_in_iosApp()
#
#     def select_libOmx_file(self):
#         filename = fd.askopenfilename(title='Open a file', initialdir=os.getcwd(), filetypes=[('All files', '*.omx')])
#         self.fields['libOmx'].setNewTxt(filename)
#         self.myLibOmx = LibOmxFile(omx_path=filename)
#         # self.myLibOmx.get_type_members_from_namespace_path("Types.Valve.OPC_UA.Valve_PLC")
#         # self.myLibOmx.print_test("unit.Types.Valve.OPC_UA.Valve_PLC")
#         # self.myLibOmx.print_test('unit.Types.AI.OPC_UA.AI_PLC')
#         # self.myLibOmx.get_type_members_from_namespace_path("Types.Valve.OPC_UA.Valve_PLC")
#
#
#     # Выбор файла с картой
#     def select_map_file(self):
#         filename = fd.askopenfilename(title='Open a file', initialdir=os.getcwd(), filetypes=[('All files', '*.xml')])
#         self.fields['map'].setNewTxt(filename)
#         self.myMap = MapFile(map_path=filename)
#         # self.get_obj_in_iosApp()
#
#     # Выбор файла с картой атрибутов
#     def select_attrMap_file(self):
#         filename = fd.askopenfilename(title='Open a file', initialdir=os.getcwd(),
#                                           filetypes=[('All files', '*.xml')])
#         self.fields['fd_atr'].setNewTxt(filename)
#         self.myAtrMap = AttrMapFile(map_path=filename)
#         self.attrList = self.myAtrMap.get_attr()
#         self.insert_attrListDict_noval()
#         self.insert_atr_noval()
#
#     def insert_attrListDict_noval(self):
#         self.attrList = self.myAtrMap.get_attr()
#         self.attrListDict.clear()
#         for i in self.attrList:
#             self.attrListDict.append({'cnt': i[0], 'id': i[1], 'value': i[2], 'newValue': None})
#
#     # Выбор файла эксель с полем path и значением атрибутов
#     def select_excell_file(self, cnt=0):
#         filename = fd.askopenfilename(title='Open a file', initialdir=os.getcwd(),
#                                           filetypes=[('All files', '*.xlsx')])
#         self.fields['fd_excell'].setNewTxt(filename)
#         # self.myExcell = ExcellFile(file_path=filename, sheet_name='30 - Флотация')
#         self.myExcell = ExcellFile(file_path=filename)
#         # self.attrListExcell = self.myExcell.getData(6, 10)
#         # print(self.myExcell.getSheetNames())
#         self.fields['cb_sheets'].setValues(self.myExcell.getSheetNames())
#
#     # Выбор листа excell файла
#     def select_cb_sheets(self, event):
#         self.sheet = self.fields['cb_sheets'].getValue()
#         self.fields['cb_path_col'].setValues(self.myExcell.getColNames(self.sheet))
#         self.fields['cb_atr_col'].setValues(self.myExcell.getColNames(self.sheet))
#
#
#     def select_cb_path_col(self, event):
#         self.path_col = self.fields['cb_path_col'].getValue()
#
#     def select_cb_atr_col(self, event):
#         self.atr_col = self.fields['cb_atr_col'].getValue()
#
#
#     def get_attr_from_excell(self):
#         self.attrListExcell = self.myExcell.getData(self.fields['cb_path_col'].getId(), self.fields['cb_atr_col'].getId(), self.sheet)
#         # print(*self.attrListExcell)
#         newAtrListDict = self.attrListDict[:]
#         for i in newAtrListDict:
#             for j in self.attrListExcell:
#                 # print(i)
#                 if i['id'] == j[0]:
#                     i['newValue'] = j[1]
#                     # print(i)
#                     break
#             else:
#                 continue
#
#         self.attrListDict = newAtrListDict[:]
#         self.fields['table_attr'].clear()
#         self.insert_atr_table()
#         self.fields['table_attr'].highlightRow()
#
#     def insert_atr_noval(self):
#         self.fields['table_attr'].clear()
#         for i in self.attrListDict:
#             self.fields['table_attr'].insert(i['cnt'], i['id'], i['value'],None)
#
#
#
#     # Вставка в таблицу для атрибутов списка словарей
#     def insert_atr_table(self):
#         self.fields['table_attr'].clear()
#         for i in self.attrListDict:
#             self.fields['table_attr'].insert(i['cnt'], i['id'], i['value'], '' if i['newValue'] is None else i['newValue'])
#
#     # редактирование файла карты атрибутов
#     def write_attr_xml(self):
#         for i in self.attrListDict:
#             if i['newValue'] is not None:
#                 print(self.myAtrMap.set_attr_value(i['id'], i['newValue']))
#
#         self.myAtrMap.save_to_file()
#         self.insert_attrListDict_noval()
#         self.insert_atr_noval()
#
#
# #********************** Вкладка карта подвязок ***************************
#
    # Проверяем подвязку по выбранной карте
    # def checkLinking(self):
    #     self.fields['log'].clear()
    #     self.fields['table'].clear()
    #     iosApp = self.fields['iosObj'].getValue()
    #     iosAppType = self.fields['iosType'].getValue()
    #     cnt = 0
    #     for i in self.myOmx.get_objName(iosApp, iosAppType):
    #         cnt += 1
    #         self.fields['log'].setNewTxt(f'{cnt}.Имя: {i:<10} Тип: {self.myOmx.get_base_type(iosApp, iosAppType, i)} '
    #                                      f'Библиотека: {self.myOmx.get_lib_name(iosApp, iosAppType, i)} '
    #                                      f'Подвязка: {self.myMap.checkLink(iosApp, iosAppType, i)}')
    #
    #         self.fields['table'].insert(cnt, i, self.myOmx.get_base_type(iosApp, iosAppType, i),
    #                                     self.myOmx.get_lib_name(iosApp, iosAppType, i),
    #                                     self.myMap.checkLink(iosApp, iosAppType, i))
    #
    # # сохранить тег в файл
    # def save_map(self):
    #     self.myMap.write_XML_to_map()
    #
    # # Установить значение переменной node_path_tag при нажатии Enter в поле ввода entry_node_path
    # def connect_node_path(self, event):
    #     node_path_tag.set(self.fields['nodePath'].getValue())
    #     self.fields['nodePath'].clear()
    #
    # # Установить значение переменной node_path_tag при нажатии Enter в поле ввода entry_node_path
    # def connect_node_id(self, event):
    #     node_id_tag.set(self.fields['nodeId'].getValue())
    #     self.fields['nodeId'].clear()
    #
    # # Связвание объектов
    # def start_linking(self):
    #     global linkink_object
    #
    #     self.fields['log'].clear()
    #     self.fields['log'].setNewTxt('Связывание')
    #
    #     iosApp = self.fields['iosObj'].getValue()
    #     iosAppType = self.fields['iosType'].getValue()
    #
    #     for i in self.myOmx.get_objName(iosApp, iosAppType):
    #         if not self.myMap.checkLink(iosApp, iosAppType, i):
    #
    #             print(i, self.myMap.checkLink(iosApp, iosAppType, i), self.myOmx.get_lib_name(iosApp, iosAppType, i))
    #             if self.myOmx.get_lib_name(iosApp, iosAppType, i) == 'SineticLib':
    #
    #                 if iosAppType == 'AI' or iosAppType == 'AI1':
    #                     linkink_object = SinLib.AI(self.get_node_path(iosApp, iosAppType, i),
    #                                                self.get_node_id(iosApp, iosAppType, i))
    #
    #                 if iosAppType == 'FC_CTRL':
    #                     linkink_object = SinLib.FC_CTRL(self.get_node_path(iosApp, iosAppType, i),
    #                                                     self.get_node_id(iosApp, iosAppType, i))
    #
    #                 for j in range(linkink_object.loopCnt()):
    #                     xmlObj = self.myMap.create_XMLtag(linkink_object[j][0],
    #                                                       linkink_object[j][1])  # создаем объект тега
    #                     self.myMap.insert_XML_to_map(xmlObj)  # вставляем объект в карту
    #
    #
    #     self.save_map()  # сохраняем файл
    #     self.fields['log'].setNewTxt('Карта подвязки успешно обновлена')
    #
    # # Получить node-path объекта по имени и произвести процедуры с полем ввода
    # def get_node_path(self, iosAppObj, iosAppObjType, obj_name):
    #
    #      # Ждем ввода в поле node_path, подставляем туда node_path из свойства объекта
    #     self.fields['log'].setNewTxt(f'Связать {obj_name} подтверди node_path <ENTER>')
    #
    #     self.fields['nodePath'].setNewTxt(self.myOmx.get_node_path(iosAppObj, iosAppObjType, obj_name))
    #     # self.insert_to_node_path(self.myOmx.get_Obj_node_path(object_name))  # Вставляем в поле путь до объекта
    #
    #     self.fields['nodePath'].enable()
    #     self.fields['nodePath'].setFocus()
    #     # self.entry_node_path.configure(state='normal')  # активируем поле для ввода
    #     # self.entry_node_path.focus_set()  # устанавливаем курсор в поле
    #
    #     root.wait_variable(node_path_tag)  # ждем ввода значения и нажатия Enter в поле
    #     node_path = node_path_tag.get()  # Получаем значения поля после нажатия кнопки Enter
    #
    #     self.fields['nodePath'].disable()
    #     # self.entry_node_path.configure(state='disabled')  # деактивируем поле
    #     self.fields['log'].setNewTxt(f'Типу: {obj_name} присвоен node_path: {node_path}')
    #
    #     return node_path
    #
    # # Аналогично получаем node_id
    # def get_node_id(self, iosAppObj, iosAppObjType, obj_name):
    #     # self.header_r3[
    #     #     'text'] = f'Связать {object_name} Тип: {self.myOmx.get_Obj_base_type(object_name)}, подтверди node_id <ENTER>'
    #
    #     self.fields['nodeId'].setNewTxt(self.myOmx.get_node_id(iosAppObj, iosAppObjType, obj_name))
    #     # self.insert_to_node_id(self.myOmx.get_Obj_node_id(object_name))
    #
    #     self.fields['nodeId'].enable()
    #     self.fields['nodeId'].setFocus()
    #     # self.entry_node_id.configure(state='normal')
    #     # self.entry_node_id.focus_set()  # устанавливаем курсор в поле
    #     root.wait_variable(node_id_tag)  # ждем ввода значения и нажатия Enter в поле
    #     node_id = node_id_tag.get()
    #
    #     self.fields['nodeId'].disable()
    #     # self.entry_node_id.configure(state='disabled')
    #
    #     self.fields['log'].setNewTxt(f'Типу: {obj_name} присвоен node_id: {node_id}')
    #     # self.insert_to_st(f'Типу: {self.myOmx.get_Obj_base_type(object_name)} присвоен node_id: {node_id}')
    #
    #     return node_id
    #
    # # Заполняем комбобокс сущетсвующими папками с типами (AI, DI и т.д.)
    # def selected_iosApp(self, event):
    #     self.fields['iosType'].setValues(self.myOmx.get_types_in_iosApp(self.fields['iosObj'].getValue()))
    #
    # # Заполняем комбобокс объектами из IosApp
    # def get_obj_in_iosApp(self):
    #     # Проверка на выбранный файлы OMX и MAP
    #     if len(self.fields['omx'].getText()) != 0 and len(self.fields['map'].getText()) != 0:
    #         self.fields['iosObj'].setValues(self.myOmx.get_objects_iosApp())
    #         self.selected_iosApp(0)
    #
    # def get_obj(self):
    #     """
    #     Получить данные по экземплярам в application модуля с программой ПЛК
    #     """
    #     self.instApp = self.myOmx.get_instance_list()
    #     self.fields['table'].clear()
    #     j = 0
    #     for i in self.instApp:
    #         j += 1
    #         lib = self.myOmx.get_base_type_by_path(i)
    #         appStr = i.split('.')
    #         noAppPath = f'{appStr[-2]}_{appStr[-1]}'
    #         item_id = self.ConfExcell.getItemId(self.myLibOmx.get_lib_prefix(lib), noAppPath)
    #         print(
    #             f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Путь:{noAppPath} Чарт:{self.myLibOmx.get_lib_prefix(lib)} item_id:{item_id}")
    #         conn_status = self.check_connection(i, lib)
    #         self.instAppDict.append({'id': j, 'path': i, 'item_id': item_id, 'lib': lib, 'con_stat':conn_status})
    #
    #     self.insert_to_map_table()
    #     self.print_instAppDict()
    #
    # def insert_to_map_table(self):
    #     """ Вставка списка словарей self.instAppDict в таблицу 'table'"""
    #
    #     for i in self.instAppDict:
    #         # appStr = i['path'].split('.')
    #         # noAppPath = f'{appStr[-2]}_{appStr[-1]}'
    #         # i['item_id'] = self.ConfExcell.getItemId(self.myLibOmx.get_lib_prefix(i['lib']),
    #         #                                          noAppPath)
    #         # print(i)
    #         self.fields['table'].insert(i['id'], i['path'], i['item_id'], i['lib'], i['con_stat'])
    #     self.fields['table'].highlightRow()
    #
    #     # iosApp = self.fields['iosObj'].getValue()
    #     # iosAppType = self.fields['iosType'].getValue()
    #     # self.fields['table'].clear()
    #     # cnt = 0
    #     # for i in self.myOmx.get_objName(iosApp, iosAppType):
    #     #     cnt += 1
    #     #     self.fields['log'].setNewTxt(f'{cnt}.Имя: {i:<10} Тип: {self.myOmx.get_base_type(iosApp, iosAppType, i)} '
    #     #                                  f'Библиотека: {self.myOmx.get_lib_name(iosApp, iosAppType, i)}')
    #     #
    #     #     self.fields['table'].insert(cnt, i, self.myOmx.get_base_type(iosApp, iosAppType, i),
    #     #                                 self.myOmx.get_lib_name(iosApp, iosAppType, i), None)
    #
    # # def on_tree_select(event):
    # #     # This function will be called when a row is selected
    # #     selected_items = self.fields['table'].selection()  # Get the ID(s) of the selected item(s)
    # #     for item_id in selected_items:
    # #         item_values = self.fields['table'].item(item_id, 'values') # Get the data values of the selected item
    # #         print(f"Selected Item ID: {item_id}, Values: {item_values}")
    #
    # def bindRowCLick(self, event):
    #     row_val = self.fields['table'].on_tree_select()
    #     tag_list = self.myLibOmx.get_lib_tag_list(row_val[1])
    #     # full_path_tag_list = [f'{row_val[0]}.{i[0]}' for i in tag_list]
    #     full_path_tag_list = [i[0] for i in tag_list]
    #     self.link_dict = self.check_link_one_instance(row_val[0], full_path_tag_list)
    #     # print(row_val[0])
    #     # print(row_val[1])
    #     self.fields['conTable'].clear()
    #
    #     j = 0
    #     for i in tag_list:
    #         j += 1
    #         self.fields['conTable'].insert(j, i[0], i[1],self.link_dict[i[0]])
    #     self.fields['conTable'].highlightRow()
    #
    #
    #
    # def check_link_one_instance(self, path:str, tag_list:list):
    #     """ Проверить подвязку по тегам одного экземпляра"""
    #
    #     link_dict = {}
    #     for i in tag_list:
    #         link_dict.update({i:self.myMap.check_link(str(path+'.'+i))})
    #     return link_dict
    #
    # def link_one_instance(self):
    #     """ Создание и отправка секции с группой тегов по экземпляру в файл карты"""
    #     lib = self.myLibOmx.get_lib_prefix(self.fields['table'].on_tree_select()[1])
    #     node_path = self.fields['table'].on_tree_select()[0]
    #     item_id = random.randint(20, 35)
    #     xmlObj = None
    #     for tag, node_id in self.link_dict.items():
    #         if node_id == "None":
    #             # print(self.myLibOmx.get_lib_prefix(self.fields['table'].on_tree_select()[1]))
    #             xmlObj = self.myMap.create_XMLtag(lib, node_path, tag, item_id)
    #             self.myMap.insert_XML_to_map(xmlObj)
    #
    #     self.save_map()
    #
    #
    # def select_conf_excell_file(self, cnt=0):
    #     """ Выбор файла эксель конфигуратора в котором есть связь itemId:Позиция экземпляра"""
    #     filename = fd.askopenfilename(title='Open a file', initialdir=os.getcwd(),
    #                                       filetypes=[('All files', '*.xlsx'), ('All files', '*.xlsm')])
    #     self.fields['conf_excell'].setNewTxt(filename)
    #     self.ConfExcell = ConfExcellFile(file_path=filename)
    #     self.ConfExcell.init_itemid_list()
    #
    #     # self.fields['cb_sheets'].setValues(self.myExcell.getSheetNames())
    #
    # def get_itemId_from_excell(self):
    #     """ Проход по экземплярам, затием по тегам экземпляров, создание XML структур и добавление их в файл """
    #
    #     for i in self.instAppDict:
    #         if i['item_id'] not in ["None", 'none']:
    #             full_path_tag_list = [j[0] for j in self.myLibOmx.get_lib_tag_list(i['lib'])]
    #             for tag, node_id in self.check_link_one_instance(i['path'], full_path_tag_list).items():
    #                 self.myMap.insert_XML_to_map(self.myMap.create_XMLtag(self.myLibOmx.get_lib_prefix(i['lib']), i['path'], tag, i['item_id']))
    #     self.save_map()
    #
    #
    # def check_connection(self, path:str ,lib:str):
    #     """ Проверка привязки по всем эксземплярам и всем тегам каждого экземпляра"""
    #     # for i in self.instAppDict:
    #     conn_list = []
    #     full_path_tag_list = [j[0] for j in self.myLibOmx.get_lib_tag_list(lib)]
    #     for tag, node_id in self.check_link_one_instance(path, full_path_tag_list).items():
    #         if node_id == "None":
    #             conn_list.append(False)
    #         else:
    #             conn_list.append(True)
    #
    #     set_list = set(conn_list)
    #     conn_list.clear()
    #     if len(set_list) == 2:
    #         return 'Частично'
    #     if True in set_list:
    #         return 'Полностью'
    #     return 'Отсутсвует'
    #
    #
    # def print_instAppDict(self):
    #     for i in self.instAppDict:
    #         print("*" * 40)
    #         print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] №:{i['id']} Путь:{i['path']} itemId:{i['item_id']} Библиотека:{i['lib']} Статус:{i['con_stat']}")

#
#
#
# if __name__ == '__main__':
#
#     root = Tk()
#     node_path_tag = tk.StringVar()  # тег ПЛК
#     node_id_tag = tk.StringVar()  # тег ПЛК
#     root.geometry("640x700")
#     app = MapLinker()
#     root.mainloop()
