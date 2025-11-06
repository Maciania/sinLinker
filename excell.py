from datetime import datetime
import json
import pandas as pd

class ExcellFile:
    def __init__(self, file_path):
        self.file_path = file_path
        # Используем ExcelFile для получения списка листов
        self.excel_file = pd.ExcelFile(file_path)
        # self.sheet_name = None

    def getData(self, name_col1, name_col2, sheet_name):
        # Читаем лист Excel
        df = pd.read_excel(self.file_path, sheet_name=sheet_name)

        # Получаем пары (A, B) из всех строк
        pairs = list(zip(df.iloc[:, name_col1], df.iloc[:, name_col2]))  # Если столбцы имеют названия
        self.close()
        return pairs


    def getSheetNames(self):
        return self.excel_file.sheet_names


    def getColNames(self, sheet_name):
        df = pd.read_excel(self.file_path, sheet_name=sheet_name, header=None)

        # Найдём первую непустую строку (предполагаем, что это заголовки)
        header_row_idx = next(
            (i for i, row in df.iterrows() if row.notna().any()),
            None
        )

        if header_row_idx is None:
            return []

        raw_header = df.iloc[header_row_idx].tolist()

        # Чистим заголовки
        clean_header = [
            (str(v).strip() if pd.notna(v) and str(v).strip() else f'Unnamed {i}')
            for i, v in enumerate(raw_header)
        ]

        return clean_header


    def close(self):
        # Закрываем файл (необязательно, но рекомендуется)
        self.excel_file.close()




class ConfExcellFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.excel_file = pd.ExcelFile(file_path)
        self.items_list = {'dbPS':{},
                           'dbEPS': {},
                           'dbPID': {},
                           'dbPID_PWM': {},
                           'dbLock': {},
                           'dbCrush': {},
                           'dbConv': {},
                           'dbARS': {},
                           'dbValve': {},
                           'dbValveReg': {},
                           'dbMotor': {},
                           'dbMotorDP': {},
                           'dbAO': {},
                           'dbDO': {},
                           'dbAM': {},
                           'dbDM': {},
                           'dbAI': {},
                           'dbDI': {}
                           } # словарь списков по всем листам в эксель

        self.items_lib = {'dbPS': 'unit.Lib.Types.PS.OPC_UA.PS_PLC',
                           'dbEPS': 'unit.Lib.Types.EPS.OPC_UA.Area_PLC',
                           'dbPID': 'unit.Lib.Types.PID.OPC_UA.PID_PLC',
                           'dbPID_PWM': 'unit.Lib.Types.PID.OPC_UA.PID_PWM',
                           'dbLock': 'unit.Lib.Types.Lock.OPC_UA.Lock_PLC',
                           'dbCrush': 'unit.Lib.Types.Crusher.OPC_UA.Crush_PLC',
                           'dbConv': 'unit.Lib.Types.Conv.OPC_UA.Conv_PLC',
                           'dbARS': 'unit.Lib.Types.ARS.OPC_UA.ARS_PLC',
                           'dbValve': 'unit.Lib.Types.Valve.OPC_UA.Valve_PLC',
                           'dbValveReg': 'unit.Lib.Types.ValveReg.OPC_UA.ValveReg_PLC',
                           'dbMotor': 'unit.Lib.Types.Motor.OPC_UA.Motor_PLC',
                           'dbMotorDP': 'unit.Lib.Types.MotorDP.OPC_UA.MotorDP_PLC',
                           'dbAO': 'unit.Lib.Types.AO.OPC_UA.AO_PLC',
                           'dbDO': 'unit.Lib.Types.DO.OPC_UA.DO_PLC',
                           'dbAM': 'unit.Lib.Types.AM.OPC_UA.AM_PLC',
                           'dbDM': 'unit.Lib.Types.DM.OPC_UA.DM_PLC',
                           'dbAI': 'unit.Lib.Types.AI.OPC_UA.AI_PLC',
                           'dbDI': 'unit.Lib.Types.DI.OPC_UA.DI_PLC'
                           }


    def getDataFromRow(self, sheet_name, name_col1=0, name_col2=1, start_row=4, skip_empty=True):
        """
        Получить данные из двух столбцов, начиная с заданной строки (по номеру Excel).
        :param name_col1: номер первого столбца (начиная с 0)
        :param name_col2: номер второго столбца (начиная с 0)
        :param sheet_name: имя листа
        :param start_row: номер первой строки в Excel (по умолчанию 4)
        :param skip_empty: пропускать ли строки, где оба значения пустые
        :return: словарь {значение_из_второго_столбца: значение_из_первого_столбца}
        """
        # Читаем лист без заголовка
        df = pd.read_excel(self.file_path, sheet_name=sheet_name, header=None)

        # Срез с нужной строки
        df = df.iloc[start_row - 1:, [name_col1, name_col2]]
        # print(f"срез всей таблицы: {df}")

        # Убираем пустые строки, если нужно
        if skip_empty:
            df = df.dropna(how='all')

        # Преобразуем в словарь ключ: item_ID, значение: Enum_name
        result = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))

        # self.close()
        return result

    def init_itemid_list(self):
        """ Инициализация словарей для каждого чарта (листа эксель)"""
        sheet_names = self.getSheetNames()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Найденные листы в конфигураторе: {sheet_names}")
        for i in self.items_list.keys():
            if i in sheet_names:
                self.items_list[i] = self.getDataFromRow(i, skip_empty=False)
                print(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Лист: {i} найден")
        # print (self.items_list['dbMotor'])
        self.close()
        self.pretty_print_items()



    def getItemId(self, sheet_name: str, obj_path: str):

        try:
            value = self.items_list[sheet_name][obj_path]
        except KeyError:
            value = 'none'
        finally:
            return value

    def close(self):
        # Закрываем файл (необязательно, но рекомендуется)
        self.excel_file.close()

    def getSheetNames(self):
        return list(self.excel_file.sheet_names)

    def pretty_print_items(self):
        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"Данные:\n{json.dumps(self.items_list, indent=4, ensure_ascii=False)}"
        )

