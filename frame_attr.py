from datetime import datetime
import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk

from gui import MyFileDialog, MyComboBox, ControlField, UniversalTable
from excell import ExcellFile
from map import AttrMapFile


class FrameAttr(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.myExcell = None    # Экземпляр класса с экселем в котором есть связь экземпляр-атрибут
        self.myAtrMap = None    # Экземпляр класса для карты атрибутов
        self.attrList = []      # Список атрибутов из карты атрибутов
        self.attrListDict = []  # Список из словарей cnt, id, value, newValue
        self.sheet = None       # Лист файла excell
        self.path_col = None    # Столбец с path тега в файле Excell
        self.atr_col = None     # Столбец с записываемым атрибутом в файле Excell



        self.init_dir = os.getcwd()

        self.help_info = {
            'atr_map': {'title':
                            'Карты атрибутов ',
                        'label':
                            'Карта атрибутов с расширением .xml\n'
                            'Находится в директории проекта по пути: DS_PROJ\\PLC_GMO\\Карты атрибутов \n'
                            'или DS_PROJ\\PLC_ORP\\Карты атрибутов'},

            'excell': {'title':
                            'Файл эксель',
                        'label':
                            'Файл эксель с расширением .xlsx\n'
                            'Находится в директории проекта по пути: DS_PROJ\\PLC_GMO\\Карты атрибутов\n'
                            'В файле нужно выбрать столбцы в которых есть соответствие:\n'
                            'экземпляр в карте атрибутов <===> значение атрибута'},

            'sheets': {'title':
                                'Лист Excell на котором есть связь ПУТЬ-АТРИУБТ ',
                        'label':
                            'Файл эксель с расширением .xlsx\n'
                            'Находится в директории проекта по пути: DS_PROJ\\PLC_GMO\\Карты атрибутов\n'
                            'Нужно выбрать лист по названию записываемого атрибута'},

            'path_col': {'title':
                           'Выбор столбца с путем в DevStudio ',
                       'label':
                           'Столбец с path должен содержать путь к экземпляру\n'
                           'Например: GMO.Flotation.HCU._30_26.FV1\n'
                           'Если в файле эксель строки с таким "path"\n'
                            'То запись в карту не произойдет'},

            'atr_col': {'title':
                             'Выбор столбца с значением атрибута для выбранного path',
                         'label':
                             'Столбец с path должен содержать путь к экземпляру\n'
                             'Например: GMO.Flotation.HCU._30_26.FV1\n'
                             'Если в файле эксель строки с таким "path"\n'
                             'То запись в карту не произойдет'}

                }

        self.create_widgets()
        self.pack_widgets()

    def create_widgets(self):
        self.fields = {
            'fd_atr': MyFileDialog(self, 'Файл карты атрибутов:', 'Открыть', cmd=self.select_attrMap_file, help_title= self.help_info['atr_map']['title'], help_label=self.help_info['atr_map']['label']),
            'fd_excell': MyFileDialog(self, 'Исходник Excell:', 'Открыть', cmd=self.select_excell_file, help_title= self.help_info['excell']['title'], help_label=self.help_info['excell']['label']),
            'cb_sheets': MyComboBox(self, 'Название листа:', bindCombo=self.select_cb_sheets, help_title= self.help_info['sheets']['title'], help_label=self.help_info['sheets']['label']),
            'cb_path_col': MyComboBox(self, 'Столбец path:', bindCombo=self.select_cb_path_col, help_title= self.help_info['path_col']['title'], help_label=self.help_info['path_col']['label']),
            'cb_atr_col': MyComboBox(self, 'Столбец атрибут:', bindCombo=self.select_cb_atr_col, help_title= self.help_info['atr_col']['title'], help_label=self.help_info['atr_col']['label']),
            'table_attr': UniversalTable(self,
                            columns=("#1", "#2", "#3", "#4"),
                            headings=("№", "ID", "Value", "NewValue"),
                            widths=(30, 120, 120, 120),
                            insert_rule=self.attrtable_insert_rule,
                            highlight_rules={
                                'highlight_row': ('yellow', 'black')
                            }
                            ),
            'btn_attr': ControlField(self,
                                     ('Проверить файл Excell', self.get_attr_from_excell),
                                  ('Записать в Альфу', self.write_attr_xml))
        }

    def pack_widgets(self):
        order = ['fd_atr', 'fd_excell', 'cb_sheets', 'cb_path_col', 'cb_atr_col', 'table_attr', 'btn_attr']
        for w in order:
            widget = self.fields[w]
            if w == 'table_attr':
                widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=3)
            else:
                widget.pack(fill=tk.X, padx=5, pady=3)

    # Выбор файла с картой атрибутов
    def select_attrMap_file(self):
        """ Выбор файла карты атрибутов, заполнение списка словарей attrListDict с пустым значением newValue"""
        filename = fd.askopenfilename(title='Open a file', initialdir=self.init_dir,
                                          filetypes=[('All files', '*.xml')])
        self.init_dir = os.path.dirname(filename)
        self.fields['fd_atr'].setNewTxt(filename)
        self.myAtrMap = AttrMapFile(map_path=filename)

        self.attrListDict.clear()
        self.attrListDict = self.myAtrMap.get_attr()
        self.insert_atr_table()


    # Выбор файла эксель с полем path и значением атрибутов
    def select_excell_file(self, cnt=0):
        filename = fd.askopenfilename(title='Open a file', initialdir=self.init_dir,
                                          filetypes=[('All files', '*.xlsx')])
        self.init_dir = os.path.dirname(filename)
        self.fields['fd_excell'].setNewTxt(filename)
        self.myExcell = ExcellFile(file_path=filename)
        self.fields['cb_sheets'].setValues(self.myExcell.getSheetNames())

    # Выбор листа excell файла
    def select_cb_sheets(self, event):
        self.sheet = self.fields['cb_sheets'].getValue()
        self.fields['cb_path_col'].setValues(self.myExcell.getColNames(self.sheet))
        self.fields['cb_atr_col'].setValues(self.myExcell.getColNames(self.sheet))


    def select_cb_path_col(self, event):
        self.path_col = self.fields['cb_path_col'].getValue()

    def select_cb_atr_col(self, event):
        self.atr_col = self.fields['cb_atr_col'].getValue()


    def get_attr_from_excell(self):
        """ Обновление newValue в словаре  attrListDict """
        self.attrListExcell = self.myExcell.getData(self.fields['cb_path_col'].getId(), self.fields['cb_atr_col'].getId(), self.sheet)
        self.attrListDict = self.myAtrMap.get_attr()
        # self.clear_newValue()

        for i in self.attrListDict:
            for j in self.attrListExcell:
                # print(i)
                if i['id'] == j[0]:
                    i['newValue'] = j[1]
                    # print(i)
                    break
            else:
                continue

        self.fields['table_attr'].clear()
        self.insert_atr_table()
        self.fields['table_attr'].highlightRow()

    def clear_newValue(self):
        for i in self.attrListDict:
            i['newValue'] = None


    # Вставка в таблицу для атрибутов списка словарей
    def insert_atr_table(self):
        self.fields['table_attr'].clear()
        for i in self.attrListDict:
            self.fields['table_attr'].insert(i['cnt'], i['id'], i['value'], '' if i['newValue'] is None else i['newValue'])

    # редактирование файла карты атрибутов
    def write_attr_xml(self):
        for i in self.attrListDict:
            if i['newValue'] is not None:
                self.myAtrMap.set_attr_value(i['id'], i['newValue'])
                print(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Запись в файл карты атрибутов №:{i['cnt']} путь:{i['id']} значение:{i['newValue']}")

        self.myAtrMap.save_to_file()



    def attrtable_insert_rule(self, values):
        i, obj_id, obj_name, new_obj_name = values
        tags = ('highlight_row',) if obj_name != new_obj_name else ()
        return values, tags
