import json
import os
from PyQt5.QtWidgets import QMessageBox
from collections import defaultdict
import firebase_admin
from firebase_admin import credentials, firestore


# Получаем путь к директории, где находится текущий скрипт
current_dir = os.path.dirname(os.path.abspath(__file__))

# Формируем путь к файлу credentials относительно текущей директории
cred_path = os.path.join(current_dir, "calendar-aip-kr-firebase-adminsdk-fbsvc-68c271d4af.json")

cred = credentials.Certificate(cred_path)

firebase_admin.initialize_app(cred, {
    'projectId': 'calendar-aip-kr'
})

# Инициализация клиента Firestore
db = firestore.client()


def convert_from_firebase_format(firebase_events):
    """Преобразует данные из формата Firebase в промежуточный формат"""
    result = []
    for event in firebase_events:
        result.append({
            "description": event.get("description", ""),
            "endDate": event.get("endDate", ""),
            "tag": event.get("tag", ""),
            "endTime": event.get("endTime", ""),
            "userId": event.get("userId", ""),
            "allDay": event.get("allDay", False),
            "title": event.get("title", ""),
            "startTime": event.get("startTime", ""),
            "color": event.get("color", "#007AFF"),
            "startDate": event.get("startDate", "")
        })
    return result


def convert_to_final_format(intermediate_data):
    """Преобразует промежуточный формат в конечный формат"""
    final_data = {}
    color_list = []

    for event in intermediate_data:
        date = event["startDate"]
        if date not in final_data:
            final_data[date] = []

        # Добавляем цвет в список цветов, если его там еще нет
        if event["color"] not in color_list:
            color_list.append(event["color"])

        # Создаем запись события
        event_entry = {
            "start_time": event["startTime"],
            "end_time": event["endTime"],
            "theme": event["title"],
            "color": event["color"],
            "description": event["description"],
            "userId": event["userId"]
        }

        final_data[date].append(event_entry)

    # Добавляем список цветов в результат
    final_data["color"] = color_list

    return final_data


def get_events_from_firestore():
    """Получает события из Firestore"""
    events_ref = db.collection("events")
    docs = events_ref.stream()

    firebase_events = []
    for doc in docs:
        firebase_events.append(doc.to_dict())

    return firebase_events


def save_to_json(data, filename):
    """Сохраняет данные в JSON файл без поля 'color'"""
    # Создаем копию данных, чтобы не изменять оригинальный словарь
    data_to_save = data.copy()
    # Удаляем поле 'color', если оно существует
    data_to_save.pop("color", None)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=4)

def load_schedule_from_file(schedule_manager):
    if os.path.exists("schedule.json"):
        try:
            # 1. Получаем данные из Firestore
            firebase_events = get_events_from_firestore()

            # 2. Преобразуем в промежуточный формат
            intermediate_data = convert_from_firebase_format(firebase_events)

            # 3. Преобразуем в конечный формат
            final_data = convert_to_final_format(intermediate_data)

            # 4. Сохраняем в JSON файл
            save_to_json(final_data, "schedule.json")

            with open("schedule.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                schedule_manager.schedule = defaultdict(list, data)
            print("Расписание загружено из файла.")
        except Exception as e:
            QMessageBox.warning(None, "Ошибка", f"Не удалось загрузить расписание: {e}")


def convert_to_firebase_format(local_data):
    """Преобразует данные из локального формата в формат Firebase"""
    firebase_events = []

    # Удаляем поле 'color' из данных, так как это отдельный список цветов
    colors = local_data.pop("color", [])

    for date, events in local_data.items():
        for event in events:
            firebase_event = {
                "startDate": date,
                "endDate": date,  # Можно модифицировать при необходимости
                "startTime": event["start_time"],
                "endTime": event["end_time"],
                "title": event.get("theme", ""),  # Используем theme как title
                "description": event.get("description", ""),
                "tag": event.get("theme", ""),  # И theme как tag
                "color": event.get("color", "#007AFF"),
                "allDay": False,  # По умолчанию
                "userId": event.get("userId", "0Md4UBw1r3PmfsqXPM9QYHst1hd2")  # Замените на реальный ID пользователя
            }
            firebase_events.append(firebase_event)

    return firebase_events


def delete_all_events():
    """Удаляет все события из коллекции events"""
    try:
        # Получаем все документы в коллекции
        events_ref = db.collection("events")
        docs = events_ref.stream()

        # Создаем batch для удаления
        batch = db.batch()

        # Добавляем все документы в batch для удаления
        deleted_count = 0
        for doc in docs:
            batch.delete(doc.reference)
            deleted_count += 1

        # Выполняем удаление
        batch.commit()
        print(f"Удалено {deleted_count} событий")
        return True
    except Exception as e:
        print(f"Ошибка при удалении событий: {e}")
        return False


def upload_to_firestore(events):
    """Загружает события в Firestore"""
    try:
        batch = db.batch()
        events_ref = db.collection("events")

        for event in events:
            if isinstance(event, dict):  # Исправлено: используем isinstance вместо type()
                new_doc_ref = events_ref.document()
                batch.set(new_doc_ref, event)

        # Фиксируем все изменения одной транзакцией
        batch.commit()
        print(f"Успешно загружено {len(events)} событий")
        return True
    except Exception as e:
        print(f"Ошибка при загрузке событий: {e}")
        return False


def load_local_json(filename):
    """Загружает данные из локального JSON-файла"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_schedule_to_file(schedule_manager):
    try:
        with open("schedule.json", "w", encoding="utf-8") as file:
            json.dump(dict(schedule_manager.schedule), file, ensure_ascii=False, indent=4)
        print("Расписание сохранено в файл.")

        # 1. Загружаем данные из локального JSON
        local_data = load_local_json("schedule.json")

        # 2. Преобразуем в формат Firebase
        firebase_events = convert_to_firebase_format(local_data)

        # 3. Удаляем все старые события
        if delete_all_events():
            # 4. Загружаем новые события
            if not upload_to_firestore(firebase_events):
                QMessageBox.warning(None, "Ошибка", "Не удалось загрузить события в Firestore")
        else:
            QMessageBox.warning(None, "Ошибка", "Не удалось удалить старые события")

    except Exception as e:
        QMessageBox.warning(None, "Ошибка", f"Не удалось сохранить расписание: {e}")