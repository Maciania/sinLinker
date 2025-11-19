import tkinter as tk
from tkinter import Tk, Text, BOTH, X, N, LEFT, RIGHT, END, ttk, scrolledtext
from tkinter.ttk import Frame, Label, Entry, Button

class MyFileDialog(Frame):
    """Класс с контейнером из трех элементов для выбора файла из директории проекта
    Используется для выбора файла проекта *omx и файла карты в который добавляются привязки"""

    def __init__(self, master, labelTxt: str, btnTxt: str, cmd, help_title='title', help_label='label'):
        """
        :param master: родительский фрейм
        :param labelTxt: текст для Label
        :param btnTxt: текст для кнопки
        :param cmd: команда для выполнения при нажатии на кнопку
        :param help_title: заголовок окна помощи
        :param help_label: текст помощи
        """
        super().__init__(master)
        self.master = master
        self.labelTxt = labelTxt
        self.btnTxt = btnTxt
        self.cmd = cmd
        self.help_title = help_title
        self.help_label = help_label

        self.__init_ui()

    def __init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.label = Label(self, text=self.labelTxt)
        self.entry = Entry(self, state='disabled')
        self.btn = Button(self, text=self.btnTxt, command=self.cmd)
        self.help_btn = Button(self, text='?', command=self.open_help_window, width=2)

        self.__pack_ui()

    def __pack_ui(self):
        """Упаковка элементов интерфейса"""
        self.label.pack(side="left", padx=10)
        self.entry.pack(side="left", expand=True, fill=X)
        self.btn.pack(side="left", padx=3)
        self.help_btn.pack(side="left", padx=0)

        # Упаковываем сам фрейм в родительский контейнер
        self.pack(anchor=tk.W, padx=5, pady=3, fill=tk.X)

    def setNewTxt(self, newText):
        """Установка нового текста в поле ввода"""
        self.entry.configure(state='normal')
        self.entry.delete(0, END)
        self.entry.insert(tk.INSERT, newText)
        self.entry.configure(state='disabled')

    def getText(self):
        """Получение текста из поля ввода"""
        return self.entry.get()

    def open_help_window(self):
        """Открытие окна помощи"""
        HelpWindow(self.help_title, self.help_label,
                   self.help_btn.winfo_rootx(),
                   self.help_btn.winfo_rooty())


class MyComboBox(Frame):
    """Класс с контейнером из двух элементов для выбора поля из комбобокса"""

    def __init__(self, master, labelTxt: str, bindCombo=None, help_title='title', help_label='label'):
        super().__init__(master)
        self.master = master
        self.labelTxt = labelTxt
        self.bindCombo = bindCombo
        self.help_title = help_title
        self.help_label = help_label
        self.__init_ui()
        # self.pack(anchor=tk.W, padx=5, pady=3, fill=tk.X)

    def __init_ui(self):
        self.label = Label(self, text=self.labelTxt)
        self.combo = ttk.Combobox(self)
        self.help_btn = Button(self, text='?', command=self.open_help_window, width=2)

        if self.bindCombo is not None:
            self.combo.bind("<<ComboboxSelected>>", self.bindCombo)

        self.label.pack(side="left", padx=10)
        self.combo.pack(side="left", expand=True, fill=X, padx=3)
        self.help_btn.pack(side="left", padx=0)

    def setValues(self, values):
        self.combo['values'] = values
        self.combo.current(0)

    def set_index(self, index):
        self.combo.current(index)

    def getValue(self):
        return self.combo.get()

    def getId(self):
        return self.combo.current()

    def get_combobox_index(self, value, case_sensitive=False):
        """
        Получить индекс значения в Combobox

        Args:
            combobox: объект ttk.Combobox
            value: искомое значение
            case_sensitive: учитывать регистр (по умолчанию False)

        Returns:
            int: индекс элемента или -1 если не найден
        """
        values = self.combo['values']

        if case_sensitive:
            # Поиск с учетом регистра
            try:
                return values.index(value)
            except ValueError:
                return -1
        else:
            # Поиск без учета регистра
            value_lower = value.lower()
            for i, item in enumerate(values):
                if str(item).lower() == value_lower:
                    return i
            return None


    def open_help_window(self):
        HelpWindow(self.help_title, self.help_label,
                   self.help_btn.winfo_rootx(),
                   self.help_btn.winfo_rooty())


class MyLabelFrame(Frame):
    """Класс для вывода объектов участвующих в подвязке"""

    def __init__(self, master, labelTxt: str, bindEntry, init_enable:bool=False):
        super().__init__(master)
        self.master = master
        self.labelTxt = labelTxt
        self.bindEntry = bindEntry
        self.init_enable = init_enable
        self.__init_ui()

        if self.init_enable:
            self.enable()

        # self.pack(anchor=tk.W, padx=5, pady=3, fill=tk.X)

    def __init_ui(self):
        self.label = Label(self, text=self.labelTxt)
        self.entry = Entry(self, state='disabled')

        if self.bindEntry is not None:
            self.entry.bind("<Return>", self.bindEntry)

        self.label.pack(side="left", padx=10)
        self.entry.pack(side="left", expand=True, fill=X)

    def setNewTxt(self, newText):
        if not self.init_enable:
            self.enable()
        self.entry.delete(0, END)
        self.entry.insert(tk.INSERT, newText)
        if not self.init_enable:
            self.disable()

    def enable(self):
        self.entry.configure(state='normal')

    def disable(self):
        self.entry.configure(state='disabled')

    def setFocus(self):
        self.entry.focus_set()

    def getValue(self):
        return self.entry.get()

    def clear(self):
        self.enable()
        self.entry.delete(0, END)
        self.disable()


class ControlField(Frame):
    """Класс с набором кнопок управления"""

    def __init__(self, master, *args):
        super().__init__(master)
        self.master = master
        self.buttons = args
        self.__init_ui()
        # self.pack(anchor=tk.W, padx=5, pady=3, fill=tk.X)

    def __init_ui(self):
        for btn_text, btn_cmd in self.buttons:
            btn = Button(self, text=btn_text, command=btn_cmd)
            # btn.pack(side="left", padx=2, expand=True, fill=X)
            btn.pack(side="left", padx=2, expand=True, fill=X)


class MyScrollText(Frame):
    """Класс прокручиваемого текста"""

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.__init_ui()
        self.pack(anchor=tk.W, padx=5, pady=3, fill=tk.BOTH, expand=True)

    def __init_ui(self):
        self.sTxt = scrolledtext.ScrolledText(
            self,
            wrap=tk.WORD,
            height=12,
            font=("Times New Roman", 10),
            state='disabled'
        )
        self.sTxt.pack(side="left", expand=True, fill=BOTH)

    def setNewTxt(self, newText):
        self.sTxt.configure(state='normal')
        self.sTxt.insert(tk.INSERT, newText + '\n')
        self.sTxt.configure(state='disabled')

    def clear(self):
        self.sTxt.configure(state='normal')
        self.sTxt.delete('1.0', END)
        self.sTxt.configure(state='disabled')


class UniversalTable(Frame):
    """Универсальная таблица Treeview"""

    def __init__(self, master, columns, headings, widths, insert_rule=None, highlight_rules=None, bindRowClick=None):
        """
        :param master: родительский виджет
        :param columns: список идентификаторов колонок ("#1", "#2", ...)
        :param headings: список заголовков
        :param widths: список ширин
        :param insert_rule: функция для вставки строки (values -> (values, tags))
        :param highlight_rules: словарь {tag: (background, foreground)}
        :param bindRowClick: функция-обработчик события выбора строки
        """
        super().__init__(master)
        self.master = master
        self.insert_rule = insert_rule
        self.highlight_rules = highlight_rules or {}
        self.__init_ui(columns, headings, widths, bindRowClick)

    def __init_ui(self, columns, headings, widths, bindRowClick):
        self.tree = ttk.Treeview(self, show="headings", columns=columns)

        # Настройка заголовков и ширины
        for col, head, width in zip(columns, headings, widths):
            self.tree.heading(col, text=head)
            self.tree.column(col, width=width)

        # Добавление скроллбара
        self.ysb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.ysb.set)

        # Упаковка
        self.tree.pack(side="left", expand=True, fill=BOTH)
        self.ysb.pack(side="left", fill=BOTH)

        # Привязка обработчика клика
        if bindRowClick:
            self.tree.bind("<<TreeviewSelect>>", bindRowClick)

        # Настройка подсветки
        for tag, (bg, fg) in self.highlight_rules.items():
            self.tree.tag_configure(tag, background=bg, foreground=fg)

    def insert(self, *values):
        """Вставка строки с использованием правила insert_rule"""
        tags = ()
        if self.insert_rule:
            values, tags = self.insert_rule(values)
        self.tree.insert("", END, values=values, tags=tags)

    def clear(self):
        """Очистка таблицы"""
        for i in self.tree.get_children():
            self.tree.delete(i)

    def get_selected(self, cols=(1, 3)):
        """Возвращает значения выбранных строк (по умолчанию 1 и 3 столбцы)"""
        selected_list = []
        for item_id in self.tree.selection():
            selected_list.append(tuple(self.tree.set(item_id, c) for c in cols))
        return selected_list


class HelpWindow(Frame):
    """Окно подсказок"""

    def __init__(self, title: str, labelTxt: str, btn_x, btn_y, master=None):
        super().__init__(master)
        self.title = title
        self.labelTxt = labelTxt
        self.btn_x = btn_x
        self.btn_y = btn_y
        self.__init_ui()

    def __init_ui(self):
        self.window = tk.Toplevel(self)
        self.window.wm_title(self.title)
        self.window.geometry(f"600x100+{self.btn_x - 600}+{self.btn_y + 20}")
        self.label = Label(self.window, text=self.labelTxt)
        self.label.pack(side="top", fill="both", expand=True, padx=0, pady=0)
