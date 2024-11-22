import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QLabel, QLineEdit, QCalendarWidget, QTableWidget,
    QTableWidgetItem, QTimeEdit, QTextEdit, QMessageBox
)
from PyQt5.QtCore import QTime


from docx import Document
from docx.shared import Pt
from docx.enum.table import WD_ALIGN_VERTICAL

from collections import defaultdict

#huрмпглрщшдощдгиоилнеагш

class ScheduleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Планировщик расписания")
        self.setGeometry(100, 100, 800, 600)

        # Словарь для хранения расписания
        self.schedule = defaultdict(list)

        # Основной виджет
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        # Верхняя панель с кнопками
        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        self.add_event_button = QPushButton("Добавить событие")
        self.add_event_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
        self.add_event_button.clicked.connect(self.show_add_event_dialog)
        self.button_layout.addWidget(self.add_event_button)

        self.view_schedule_button = QPushButton("Просмотреть расписание")
        self.view_schedule_button.setStyleSheet("background-color: #2196F3; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
        self.view_schedule_button.clicked.connect(self.show_view_schedule_dialog)
        self.button_layout.addWidget(self.view_schedule_button)

        self.export_button = QPushButton("Экспортировать в .docx")
        self.export_button.setStyleSheet("background-color: #FFC107; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
        self.export_button.clicked.connect(self.export_to_docx)
        self.button_layout.addWidget(self.export_button)

        # Календарь
        self.calendar = QCalendarWidget()
        self.calendar.setStyleSheet("""
            QCalendarWidget {
                background-color: #ffffff;
                border: 1px solid #ddd;
                font-size: 14px;
            }
            QCalendarWidget QAbstractItemView {
                selection-background-color: #4CAF50;
            }
            QCalendarWidget QToolButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                border: none;
                padding: 10px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #45a049;
            }
            QCalendarWidget QToolButton:pressed {
                background-color: #3e8e41;
            }
            QCalendarWidget QHeaderView::section {
                background-color: #2196F3;
                color: white;
                font-size: 16px;
                padding: 10px;
                border: none;
                text-align: center;
            }
        """)
        self.calendar.clicked.connect(self.update_schedule_view)
        self.layout.addWidget(self.calendar)

        # Таблица для отображения событий
        self.event_table = QTableWidget()
        self.event_table.setColumnCount(4)  # Теперь 4 столбца
        self.event_table.setHorizontalHeaderLabels(["Дата", "Начало", "Конец", "Описание"])
        self.event_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                font-size: 14px;
                background-color: #f9f9f9;
                gridline-color: #ddd;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QTableWidget::item:hover {
                background-color: #f1f1f1;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 10px;
            }
        """)
        self.layout.addWidget(self.event_table)

        # Кнопка для удаления события
        self.delete_event_button = QPushButton("Удалить событие")
        self.delete_event_button.setStyleSheet("background-color: #f44336; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
        self.delete_event_button.clicked.connect(self.delete_event)
        self.layout.addWidget(self.delete_event_button)

        # Кнопка для редактирования события
        self.edit_event_button = QPushButton("Редактировать событие")
        self.edit_event_button.setStyleSheet("background-color: #009688; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
        self.edit_event_button.clicked.connect(self.edit_event)
        self.layout.addWidget(self.edit_event_button)
        
        self.search_layout = QHBoxLayout()
        self.layout.addLayout(self.search_layout)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите текст для поиска...")
        self.search_layout.addWidget(self.search_input)

        self.search_button = QPushButton("Поиск")
        self.search_button.setStyleSheet("background-color: #FFA726; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
        self.search_button.clicked.connect(self.search_events)
        self.search_layout.addWidget(self.search_button)

        # Обновить расписание для выбранной даты
        self.update_schedule_view()

    def show_add_event_dialog(self):
        # Диалог для добавления события
        dialog = QWidget()
        dialog.setWindowTitle("Добавить событие")
        dialog_layout = QVBoxLayout()
        dialog.setLayout(dialog_layout)

        # Ввод даты
        date_label = QLabel("Дата:")
        dialog_layout.addWidget(date_label)
        date_input = QLineEdit(self.calendar.selectedDate().toString("yyyy-MM-dd"))
        dialog_layout.addWidget(date_input)

        # Ввод времени начала
        start_time_label = QLabel("Время начала:")
        dialog_layout.addWidget(start_time_label)
        start_time_input = QTimeEdit()
        start_time_input.setTime(QTime(9, 0))
        dialog_layout.addWidget(start_time_input)

        # Ввод времени окончания
        end_time_label = QLabel("Время окончания:")
        dialog_layout.addWidget(end_time_label)
        end_time_input = QTimeEdit()
        end_time_input.setTime(QTime(10, 0))
        dialog_layout.addWidget(end_time_input)

        # Ввод описания
        description_label = QLabel("Описание:")
        dialog_layout.addWidget(description_label)
        description_input = QTextEdit()
        dialog_layout.addWidget(description_input)

        # Кнопки "Добавить" и "Отмена"
        button_layout = QHBoxLayout()
        dialog_layout.addLayout(button_layout)
        add_button = QPushButton("Добавить")
        cancel_button = QPushButton("Отмена")
        button_layout.addWidget(add_button)
        button_layout.addWidget(cancel_button)

        def add_event():
            date = date_input.text()
            start_time = start_time_input.time().toString("HH:mm")
            end_time = end_time_input.time().toString("HH:mm")
            description = description_input.toPlainText()

            # Проверка накладок
            for event in self.schedule[date]:
                if not (end_time <= event['start_time'] or start_time >= event['end_time']):
                    reply = QMessageBox.question(
                        dialog,
                        "Накладка",
                        f"Событие пересекается с '{event['description']}' "
                        f"({event['start_time']} - {event['end_time']}). Добавить всё равно?",
                        QMessageBox.Yes | QMessageBox.No
                    )
                    if reply == QMessageBox.No:
                        return

            # Добавление события
            self.schedule[date].append({
                'start_time': start_time,
                'end_time': end_time,
                'description': description
            })
            QMessageBox.information(dialog, "Успех", "Событие добавлено!")
            dialog.close()
            self.update_schedule_view()

        add_button.clicked.connect(add_event)
        cancel_button.clicked.connect(dialog.close)
        dialog.show()

    def delete_event(self):
        # Получаем выбранную строку в таблице
        selected_row = self.event_table.currentRow()
        if selected_row == -1:  # Если строка не выбрана
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите событие для удаления.")
            return

        # Получаем данные из выбранной строки
        start_time = self.event_table.item(selected_row, 0).text()
        end_time = self.event_table.item(selected_row, 1).text()
        description = self.event_table.item(selected_row, 2).text()

        # Получаем выбранную дату из календаря
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")

        # Ищем и удаляем событие из словаря
        for event in self.schedule[selected_date]:
            if (event['start_time'] == start_time and
                event['end_time'] == end_time and
                event['description'] == description):
                self.schedule[selected_date].remove(event)
                QMessageBox.information(self, "Удаление", "Событие успешно удалено.")
                break
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось найти событие для удаления.")

        # Обновление таблицы
        self.update_schedule_view()

    def edit_event(self):
        # Получаем выбранную строку в таблице
        selected_row = self.event_table.currentRow()
        if selected_row == -1:  # Если строка не выбрана
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите событие для редактирования.")
            return

        # Получаем данные из выбранной строки
        start_time = self.event_table.item(selected_row, 1).text()
        end_time = self.event_table.item(selected_row, 2).text()
        description = self.event_table.item(selected_row, 3).text()

        # Получаем выбранную дату из календаря
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")

        # Открываем диалог редактирования
        dialog = QWidget()
        dialog.setWindowTitle("Редактировать событие")
        dialog_layout = QVBoxLayout()
        dialog.setLayout(dialog_layout)

        # Ввод времени начала
        start_time_label = QLabel("Время начала:")
        dialog_layout.addWidget(start_time_label)
        start_time_input = QTimeEdit(QTime.fromString(start_time, "HH:mm"))
        dialog_layout.addWidget(start_time_input)

        # Ввод времени окончания
        end_time_label = QLabel("Время окончания:")
        dialog_layout.addWidget(end_time_label)
        end_time_input = QTimeEdit(QTime.fromString(end_time, "HH:mm"))
        dialog_layout.addWidget(end_time_input)

        # Ввод описания
        description_label = QLabel("Описание:")
        dialog_layout.addWidget(description_label)
        description_input = QTextEdit(description)
        dialog_layout.addWidget(description_input)

        # Кнопки "Сохранить" и "Отмена"
        button_layout = QHBoxLayout()
        dialog_layout.addLayout(button_layout)
        save_button = QPushButton("Сохранить")
        cancel_button = QPushButton("Отмена")
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        def save_changes():
            new_start_time = start_time_input.time().toString("HH:mm")
            new_end_time = end_time_input.time().toString("HH:mm")
            new_description = description_input.toPlainText()

            # Проверка накладок с другими событиями
            #for event in self.schedule[selected_date]:
            #    if not (new_end_time <= event['start_time'] or new_start_time >= event['end_time']):
            #        reply = QMessageBox.question(
            #            dialog,
            #            "Накладка",
            #            f"Событие пересекается с '{event['description']}' "
            #            f"({event['start_time']} - {event['end_time']}). Сохранить изменения?",
            #            QMessageBox.Yes | QMessageBox.No
            #       )
            #        if reply == QMessageBox.No:
            #            return

            # Обновление события
            for event in self.schedule[selected_date]:
                if (event['start_time'] == start_time and
                    event['end_time'] == end_time and
                    event['description'] == description):
                    event['start_time'] = new_start_time
                    event['end_time'] = new_end_time
                    event['description'] = new_description
                    break
            
            # Сортировка событий по времени начала
            self.schedule[selected_date].sort(key=lambda event: event['start_time'])
        
            QMessageBox.information(dialog, "Успех", "Событие успешно обновлено.")
            dialog.close()
            self.update_schedule_view()

        save_button.clicked.connect(save_changes)
        cancel_button.clicked.connect(dialog.close)
        dialog.show()
        
    def show_view_schedule_dialog(self):
        # Проверка, открыто ли уже окно расписания
        if hasattr(self, "view_schedule_dialog") and self.view_schedule_dialog is not None:
            self.view_schedule_dialog.close()

        # Диалог для просмотра расписания
        self.view_schedule_dialog = QWidget()
        self.view_schedule_dialog.setWindowTitle("Просмотреть расписание")
        dialog_layout = QVBoxLayout()
        self.view_schedule_dialog.setLayout(dialog_layout)

        # Добавление выбора даты
        filter_layout = QHBoxLayout()
        dialog_layout.addLayout(filter_layout)

        date_filter_label = QLabel("Фильтр по дате:")
        filter_layout.addWidget(date_filter_label)

        date_filter_input = QCalendarWidget()
        date_filter_input.setMaximumHeight(200)
        filter_layout.addWidget(date_filter_input)

        filter_button = QPushButton("Применить фильтр")
        filter_layout.addWidget(filter_button)

        show_all_button = QPushButton("Показать всё расписание")
        filter_layout.addWidget(show_all_button)

        # Таблица для вывода расписания
        schedule_table = QTableWidget()
        schedule_table.setColumnCount(4)
        schedule_table.setHorizontalHeaderLabels(["Дата", "Время начала", "Время окончания", "Описание"])
        dialog_layout.addWidget(schedule_table)

        def populate_table(filtered_schedule=None):
            """Обновляет таблицу расписания."""
            schedule_table.setRowCount(0)  # Очистить таблицу

            # Если фильтр пустой, показываем всё расписание
            data = self.schedule.items() if filtered_schedule is None else filtered_schedule.items()

            for date, events in sorted(data):
                for event in sorted(events, key=lambda e: e['start_time']):
                    row = schedule_table.rowCount()
                    schedule_table.insertRow(row)
                    schedule_table.setItem(row, 0, QTableWidgetItem(date))
                    schedule_table.setItem(row, 1, QTableWidgetItem(event['start_time']))
                    schedule_table.setItem(row, 2, QTableWidgetItem(event['end_time']))
                    schedule_table.setItem(row, 3, QTableWidgetItem(event['description']))

        def apply_filter():
            """Применяет фильтр по выбранной дате."""
            selected_date = date_filter_input.selectedDate().toString("yyyy-MM-dd")
            filtered_schedule = {selected_date: self.schedule.get(selected_date, [])}
            populate_table(filtered_schedule)

        def show_all_schedule():
            """Сбрасывает фильтр и показывает всё расписание."""
            populate_table()

        filter_button.clicked.connect(apply_filter)
        show_all_button.clicked.connect(show_all_schedule)

        # Изначально показываем всё расписание
        populate_table()

        # Кнопка закрытия
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.view_schedule_dialog.close)
        dialog_layout.addWidget(close_button)

        self.view_schedule_dialog.show()
        
    def search_events(self):
        """Поиск событий по описанию."""
        search_term = self.search_input.text().strip().lower()  # Получаем поисковый запрос

        if not search_term:  # Если строка поиска пустая
            QMessageBox.warning(self, "Ошибка", "Введите текст для поиска.")
            return

        # Создаём отфильтрованное расписание
        filtered_schedule = defaultdict(list)
        for date, events in self.schedule.items():
            for event in events:
                if search_term in event['description'].lower():  # Поиск в описании события
                    filtered_schedule[date].append(event)

        if not filtered_schedule:  # Если ничего не найдено
            QMessageBox.information(self, "Поиск", f"Ничего не найдено по запросу: {search_term}")
            return

        # Обновляем таблицу с отфильтрованными событиями
        self.update_schedule_view(filtered_schedule)
        
    def update_schedule_view(self, filtered_schedule=None):
        """
        Обновляет виджет таблицы расписания.
        Если передан filtered_schedule, отображает только отфильтрованные данные.
        """
        # Если передан словарь с фильтром
        if isinstance(filtered_schedule, dict):
            data = filtered_schedule.items()
        else:
            # Получаем расписание для выбранной даты из календаря
            selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
            events = self.schedule.get(selected_date, [])
            data = {selected_date: events}.items()

        # Очищаем таблицу
        self.event_table.setRowCount(0)

        # Заполняем таблицу новыми данными
        for date, events in data:
            for event in events:
                row = self.event_table.rowCount()
                self.event_table.insertRow(row)
                self.event_table.setItem(row, 0, QTableWidgetItem(date))  # Дата
                self.event_table.setItem(row, 1, QTableWidgetItem(event['start_time']))  # Начало
                self.event_table.setItem(row, 2, QTableWidgetItem(event['end_time']))    # Конец
                self.event_table.setItem(row, 3, QTableWidgetItem(event['description']))  # Описание

        # Обновляем отображение таблицы
        self.event_table.resizeColumnsToContents()


    def export_to_docx(self):
        # Получаем все данные из расписания
        if not self.schedule:
            QMessageBox.warning(self, "Ошибка", "Нет событий для экспорта.")
            return

        # Создаем новый документ Word
        doc = Document()
        doc.add_heading("Расписание", 0)

        # Создаем таблицу с 4 столбцами: Дата, Время начала, Время окончания, Описание
        table = doc.add_table(rows=1, cols=4)

        # Настроим заголовки таблицы
        headers = table.rows[0].cells
        headers[0].text = "Дата"
        headers[1].text = "Время начала"
        headers[2].text = "Время окончания"
        headers[3].text = "Описание"

        # Устанавливаем ширину столбцов
        table.columns[0].width = Pt(100)  # Дата
        table.columns[1].width = Pt(80)   # Время начала
        table.columns[2].width = Pt(80)   # Время окончания
        table.columns[3].width = Pt(250)  # Описание (широкий столбец для описания)

        # Применим стиль к заголовкам
        for cell in headers:
            cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].alignment = 1  # Центрируем заголовки

        # Добавляем все события в таблицу
        for date, events in sorted(self.schedule.items()):
            for event in sorted(events, key=lambda e: e['start_time']):
                row_cells = table.add_row().cells
                row_cells[0].text = date
                row_cells[1].text = event['start_time']
                row_cells[2].text = event['end_time']
                row_cells[3].text = event['description']

                # Настроим выравнивание для текста в ячейках
                row_cells[0].paragraphs[0].alignment = 1  # Выравнивание даты по центру
                row_cells[1].paragraphs[0].alignment = 1  # Выравнивание времени начала по центру
                row_cells[2].paragraphs[0].alignment = 1  # Выравнивание времени окончания по центру
                row_cells[3].paragraphs[0].alignment = 0  # Описание выравниваем по левому краю

                # Сделаем текст в столбце "Описание" многострочным (перенос слов)
                for paragraph in row_cells[3].paragraphs:
                    for run in paragraph.runs:
                        run.font.size = Pt(10)  # Устанавливаем размер шрифта для текста в описании

                # Вертикальное выравнивание для столбцов
                for cell in row_cells:
                    cell.paragraphs[0].alignment = 0  # Выравнивание текста по левому краю для всех столбцов
                    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER  # Выравнивание по вертикали

        # Сохраняем файл
        doc.save("Расписание.docx")
        QMessageBox.information(self, "Экспорт", "Все события успешно экспортированы в Расписание.docx.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ScheduleApp()
    window.show()
    sys.exit(app.exec_())
