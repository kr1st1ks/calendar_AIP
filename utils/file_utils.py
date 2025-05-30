import json
import os
from PyQt5.QtWidgets import QMessageBox
from collections import defaultdict  # Добавлен импорт defaultdict


def load_schedule_from_file(schedule_manager):
    if os.path.exists("schedule.json"):
        try:
            with open("schedule.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                schedule_manager.schedule = defaultdict(list, data)
            print("Расписание загружено из файла.")
        except Exception as e:
            QMessageBox.warning(None, "Ошибка", f"Не удалось загрузить расписание: {e}")


def save_schedule_to_file(schedule_manager):
    try:
        with open("schedule.json", "w", encoding="utf-8") as file:
            json.dump(dict(schedule_manager.schedule), file, ensure_ascii=False, indent=4)
        print("Расписание сохранено в файл.")
    except Exception as e:
        QMessageBox.warning(None, "Ошибка", f"Не удалось сохранить расписание: {e}")