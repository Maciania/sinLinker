import tkinter as tk
from map_linker import MapLinker
from logger import setup_logger

if __name__ == "__main__":

    logger = setup_logger()
    logger.info('Logger инициализирован')
    logger.info("Запуск программы")
    try:

        root = tk.Tk()
        logger.info('Tkinter окно создано')

        root.geometry("900x700")
        root.title("sLinker Карты адресов, атрибутов")
        logger.info('Настроены параметры окна')

        app = MapLinker(master=root)
        logger.info('MapLinker создан')

        app.pack(fill="both", expand=True)
        logger.info('MapLinker упакован в окно')

        logger.info('Переход в root.mainloop()')
        root.mainloop()
        logger.info('mainloop завершён')

    except Exception as e:
        logger.exception("Произошла ошибка:")

