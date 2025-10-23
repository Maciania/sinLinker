import tkinter as tk
from tkinter import ttk

from frame_itemGenerator import FrameItemGenerator
from frame_plc import FramePLC
from frame_attr import FrameAttr
from frame_initPath import FrameInitPath

class MapLinker(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill=tk.BOTH)

        self.frame1 = FramePLC(notebook)
        self.frame2 = FrameAttr(notebook)
        self.frame3 = FrameInitPath(notebook)
        self.frame4 = FrameItemGenerator(notebook)

        notebook.add(self.frame1, text="Карта ПЛК")
        notebook.add(self.frame2, text="Карта атрибутов")
        notebook.add(self.frame3, text="Блокиконки")
        notebook.add(self.frame4, text="Генератор item-ов")
