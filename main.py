import tkinter as tk
from map_linker import MapLinker
from logger import Logger

if __name__ == "__main__":
    print(">>> Запуск программы")
    try:
        # Logger()
        print(">>> Logger инициализирован")

        root = tk.Tk()
        print(">>> Tkinter окно создано")

        root.geometry("900x700")
        root.title("sLinker Карты адресов, атрибутов")
        print(">>> Настроены параметры окна")

        app = MapLinker(master=root)
        print(">>> MapLinker создан")

        app.pack(fill="both", expand=True)
        print(">>> MapLinker упакован в окно")

        print(">>> Переход в root.mainloop()")
        root.mainloop()
        print(">>> mainloop завершён")

    except Exception as e:
        import traceback
        traceback.print_exc()
        input("Нажми Enter для выхода...")


