import sys
import os
from datetime import datetime

class Logger:
    def __init__(self, filename="app.log"):
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        log_path = os.path.join(base_path, filename)
        self.log_file = open(log_path, "a", encoding="utf-8", buffering=1)  # buffering=1 = построчная запись

        sys.stdout = self.log_file
        sys.stderr = self.log_file

        self.write("=" * 40)
        self.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Приложение запущено")

    def write(self, msg: str):
        print(msg)