import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from datetime import datetime
from objectMnemos import ObjectMnemos

from gui import MyFileDialog, ControlField, UniversalTable


class FrameInitPath(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.ObjectMnemosInst = None
        self.inst_list = []
        self.omobj_list = [] # Список словарей в формате [id, filename, name, uuid, cnt_blockicons]

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
            'object_dir': MyFileDialog(self, 'Путь к object c мнемосхемами :', 'Открыть', cmd=self.select_object_dir,
                                       help_title=self.help_info['omx']['title'],
                                       help_label=self.help_info['omx']['label']),
            'object_table': UniversalTable(self,
                                        columns=("#1", "#2", "#3", "#4", "#5"),
                                        headings=("№", "Файл", "Название", "uuid", "кол-во блокиконок"),
                                        widths=(30, 50, 50, 150, 50),
                                        insert_rule=self.object_table_insert_rule,
                                        highlight_rules={
                                            'highlight_row': ('lightgreen', 'black')
                                        },
                                       bindRowClick=self.test
                                        ),
            'inst_table': UniversalTable(self,
                                        columns=("#1", "#2", "#3", "#4", "#5"),
                                        headings=("№", "name", "base_type", "initPath", "apSource"),
                                        widths=(30, 100, 100, 150, 150),
                                        # insert_rule=self.object_table_insert_rule,
                                        # highlight_rules={
                                        #         'highlight_row': ('lightgreen', 'black')
                                        #             },
                                        #            bindRowClick=self.test
                                                    ),
            'btn': ControlField(self,
                                ('Получить объекты', self.get_blockicons),
                                # ('Проверить подвязку', self.check_connection),
                                ('Полная привязка', self.get_blockicons))
        }

    def pack_widgets(self):
        order = ['object_dir', 'object_table', 'inst_table', 'btn']
        for w in order:
            widget = self.fields[w]
            if w == 'object_table':
                widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=3)
            else:
                widget.pack(fill=tk.X, padx=5, pady=3)

    def select_object_dir(self):
        """ Выбор директории object в папке с проектом"""

        # dirname = fd.askdirectory(initialdir=os.getcwd())
        dirname = fd.askdirectory(initialdir='C:\\Users\\sinetic\\Desktop\\new_mak_zif\\HMI\\objects')
        if dirname:
            self.fields['object_dir'].setNewTxt(dirname)
            self.ObjectMnemosInst = ObjectMnemos(objectDir_path=dirname)
            self.omobj_list = self.ObjectMnemosInst.get_files_info()
            self.insert_to_omobj_table()

    def get_blockicons(self, event):
        """ Получить информацию по мнемосхеме и встваить в таблицу с блокиконками """
        file = self.fields['object_table'].get_selected(cols=(0, 1))[0][1]
        self.inst_list = self.ObjectMnemosInst.get_data_from_omobj(file)
        self.fields['inst_table'].clear()
        self.insert_to_inst_table()

    def object_table_insert_rule(self, values):
        """ Подсвечиваем строки где есть бллокиконки """
        id, filename, name, uuid, cnt_blockicons = values
        tags = ('highlight_row',) if cnt_blockicons > 0 else ()
        return values, tags

    def insert_to_omobj_table(self):
        for row in self.omobj_list:
            id, filename, name, uuid, cnt_blockicons = row
            self.fields['object_table'].insert(id, filename, name, uuid, cnt_blockicons)

    def insert_to_inst_table(self):
        for row in self.inst_list:
            id, name, base_type,init_path, ap_source = row
            self.fields['inst_table'].insert(id, name, base_type,init_path, ap_source)


