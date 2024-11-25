from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QLineEdit, QCalendarWidget, QTableWidget,
    QTableWidgetItem, QMessageBox,
    QFileDialog
)
from PyQt5.QtGui import QTextCharFormat, QFont, QColor
from PyQt5.QtCore import QDate
from data.schedule_manager import ScheduleManager
from ui.add_event_dialog import AddEventDialog
from ui.edit_event_dialog import EditEventDialog
from ui.view_schedule_dialog import ViewScheduleDialog
from export.export_to_docx import export_schedule_to_docx
from utils.file_utils import load_schedule_from_file, save_schedule_to_file

class ScheduleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Планировщик расписания")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5FFFA; /* Светлый оттенок зелени для заднего фона */
            }

            QPushButton {
                background-color: #6B8E23; /* Мшистый зеленый */
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #228B22; /* Темно-зеленый при наведении */
            }

            QPushButton:pressed {
                background-color: #8B4513; /* Землистый коричневый при нажатии */
            }

            QCalendarWidget {
                background-color: #F0FFF0; /* Очень светло-зеленый */
                border: 1px solid #6B8E23;
                font-size: 14px;
                color: #2E8B57; /* Темно-зеленый для текста */
            }

            QCalendarWidget QAbstractItemView {
                selection-background-color: #90EE90; /* Светло-зеленый для выделения */
                gridline-color: #6B8E23;
                border: 1px solid #6B8E23;
            }

            QCalendarWidget QToolButton {
                background-color: #228B22; /* Темно-зеленый */
                color: white;
                font-weight: bold;
                border: none;
                padding: 10px;
            }

            QCalendarWidget QToolButton:hover {
                background-color: #6B8E23; /* Мшистый зеленый */
            }

            QCalendarWidget QToolButton:pressed {
                background-color: #8B4513; /* Землистый коричневый */
            }

            QCalendarWidget QHeaderView::section {
                background-color: #6B8E23; /* Мшистый зеленый */
                color: white;
                font-size: 16px;
                padding: 10px;
                border: none;
                text-align: center;
            }

            QCalendarWidget QTextCharFormat {
                color: #2E8B57;
            }

            QTableWidget {
                border: 1px solid #8B4513;
                font-size: 14px;
                background-color: #F0FFF0;
                gridline-color: #6B8E23;
            }

            QTableWidget::item {
                padding: 10px;
            }

            QTableWidget::item:hover {
                background-color: #90EE90;
            }

            QHeaderView::section {
                background-color: #6B8E23;
                color: white;
                font-size: 16px;
                padding: 10px;
            }

            QLineEdit {
                border: 1px solid #6B8E23;
                border-radius: 5px;
                padding: 8px;
                background-color: #FFFFFF;
                color: #2E8B57;
                font-size: 14px;
            }

            QLineEdit:focus {
                border: 2px solid #228B22;
            }

            QMessageBox {
                background-color: #F5FFFA;
                color: #2E8B57;
                font-size: 14px;
            }

            QFileDialog {
                background-color: #F5FFFA;
                color: #2E8B57;
                font-size: 14px;
            }
        """)

        self.schedule_manager = ScheduleManager()

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        self.add_event_button = QPushButton("Добавить событие")

        self.add_event_button.clicked.connect(self.show_add_event_dialog)
        self.button_layout.addWidget(self.add_event_button)

        self.view_schedule_button = QPushButton("Просмотреть расписание")

        self.view_schedule_button.clicked.connect(self.show_view_schedule_dialog)
        self.button_layout.addWidget(self.view_schedule_button)

        self.export_button = QPushButton("Экспортировать в .docx")

        self.export_button.clicked.connect(self.export_to_docx)
        self.button_layout.addWidget(self.export_button)

        self.calendar = QCalendarWidget()
        self.calendar.setStyleSheet("""
            QCalendarWidget {
                background-color: #ffffff;
                border: 1px solid #6B8E23;
                font-size: 14px;
            }
            QCalendarWidget QAbstractItemView {
                selection-background-color: #90EE90;
            }
            QCalendarWidget QToolButton {
                background-color: #228B22;
                color: white;
                font-weight: bold;
                border: none;
                padding: 10px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #6B8E23;
            }
            QCalendarWidget QToolButton:pressed {
                background-color: #8B4513;
            }
            QCalendarWidget QHeaderView::section {
                background-color: #6B8E23;
                color: white;
                font-size: 16px;
                padding: 10px;
                border: none;
                text-align: center;
            }
        """)
        self.calendar.clicked.connect(self.update_schedule_view)
        self.calendar.setMinimumDate(QDate(1, 1, 1))
        self.calendar.setMaximumDate(QDate(9999, 1, 1))
        self.layout.addWidget(self.calendar)

        self.event_table = QTableWidget()
        self.event_table.setColumnCount(5)
        self.event_table.setHorizontalHeaderLabels(["Дата", "Начало", "Конец", "Тема", "Описание"])
        self.event_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #8B4513;
                font-size: 14px;
                background-color: #F0FFF0;  /* Очень светло-зеленый */
                gridline-color: #6B8E23;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QTableWidget::item:hover {
                background-color: #90EE90; /* Светло-зеленый */
            }
            QHeaderView::section {
                background-color: #228B22;
                color: white;
                font-size: 16px;
                padding: 10px;
            }
        """)
        self.layout.addWidget(self.event_table)
        # Обновление отображения точек при изменении месяца или выборе даты
        self.calendar.selectionChanged.connect(self.add_event_dots)
        self.calendar.currentPageChanged.connect(self.add_event_dots)

        # Первоначальная настройка точек
        self.add_event_dots()

        self.delete_event_button = QPushButton("Удалить событие")
        self.delete_event_button.setStyleSheet("""
            background-color: #8B0000; 
            color: white; 
            font-size: 14px; 
            padding: 10px; 
            border-radius: 5px;
        """)
        self.delete_event_button.clicked.connect(self.delete_event)
        self.layout.addWidget(self.delete_event_button)

        self.edit_event_button = QPushButton("Редактировать событие")
        self.edit_event_button.setStyleSheet("""
            background-color: #6B8E23; 
            color: white; 
            font-size: 14px; 
            padding: 10px; 
            border-radius: 5px;
        """)
        self.edit_event_button.clicked.connect(self.edit_event)
        self.layout.addWidget(self.edit_event_button)

        self.search_layout = QHBoxLayout()
        self.layout.addLayout(self.search_layout)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите текст для поиска...")
        self.search_layout.addWidget(self.search_input)

        self.search_button = QPushButton("Поиск")
        self.search_button.setStyleSheet(
            "background-color: #FFA726; color: white; font-size: 14px; padding: 10px; border-radius: 5px;")
        self.search_button.clicked.connect(self.search_events)
        self.search_layout.addWidget(self.search_button)
        self.search_input.returnPressed.connect(self.search_button.click)

        self.load_schedule_from_file()
        self.update_schedule_view()
        self.add_event_dots()

    def load_schedule_from_file(self):
        load_schedule_from_file(self.schedule_manager)

    def show_add_event_dialog(self):
        dialog = AddEventDialog(self.calendar.selectedDate().toString("yyyy-MM-dd"), self.schedule_manager)
        dialog.exec()  # Исправлено с dialog.exec_() на dialog.exec()
        self.update_schedule_view()

    def delete_event(self):
        selected_row = self.event_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите событие для удаления.")
            return

        date = self.event_table.item(selected_row, 0).text()
        start_time = self.event_table.item(selected_row, 1).text()
        end_time = self.event_table.item(selected_row, 2).text()
        theme = self.event_table.item(selected_row, 3).text()
        description = self.event_table.item(selected_row, 4).text()

        self.schedule_manager.delete_event(date, start_time, end_time, theme, description)
        self.update_schedule_view()

    def edit_event(self):
        selected_row = self.event_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите событие для редактирования.")
            return

        date = self.event_table.item(selected_row, 0).text()
        start_time = self.event_table.item(selected_row, 1).text()
        end_time = self.event_table.item(selected_row, 2).text()
        theme = self.event_table.item(selected_row, 3).text()
        description = self.event_table.item(selected_row, 4).text()

        dialog = EditEventDialog(date, start_time, end_time, theme, description, self.schedule_manager)
        dialog.exec()  # Исправлено с dialog.exec_() на dialog.exec()
        self.update_schedule_view()
        self.add_event_dots()

    def add_event_dots(self):
        """
        Добавляет красную точку над днями с событиями.
        """
        # Очищаем старые текстовые форматы
        self.calendar.setDateTextFormat(QDate(), QTextCharFormat())

        # Настройка текста для дней с событиями
        text_format = QTextCharFormat()
        font = QFont()
        font.setBold(True)
        text_format.setFont(font)
        text_format.setFontUnderline(True)

        # Применяем точки для дат с событиями
        for date_str in self.schedule_manager.get_schedule():
            date = QDate.fromString(date_str, "yyyy-MM-dd")
            if date.isValid():
                self.calendar.setDateTextFormat(date, text_format)

    def show_view_schedule_dialog(self):
        dialog = ViewScheduleDialog(self.schedule_manager)
        dialog.exec()  # Исправлено с dialog.exec_() на dialog.exec()

    def search_events(self):
        search_term = self.search_input.text().strip().lower()
        if not search_term:
            QMessageBox.warning(self, "Ошибка", "Введите текст для поиска.")
            return

        filtered_schedule = self.schedule_manager.search_events(search_term)
        self.update_schedule_view(filtered_schedule)

    def update_schedule_view(self, filtered_schedule=None):
        """
        Обновляет виджет таблицы расписания.
        Если передан filtered_schedule, отображает только отфильтрованные данные.
        """
        self.event_table.setRowCount(0)

        if filtered_schedule is None:
            selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
            events = self.schedule_manager.get_schedule(selected_date)
            data = {selected_date: events}.items()
        else:
            if isinstance(filtered_schedule, QDate):
                print(f"Expected a dictionary, but got a QDate: {filtered_schedule}")
                selected_date = filtered_schedule.toString("yyyy-MM-dd")
                events = self.schedule_manager.get_schedule(selected_date)
                data = {selected_date: events}.items()
            elif isinstance(filtered_schedule, dict):
                data = filtered_schedule.items()
            else:
                print(f"Unexpected type for filtered_schedule: {type(filtered_schedule)}")
                return

        for date, events in data:
            for event in events:
                row = self.event_table.rowCount()
                self.event_table.insertRow(row)
                self.event_table.setItem(row, 0, QTableWidgetItem(date))
                self.event_table.setItem(row, 1, QTableWidgetItem(event['start_time']))
                self.event_table.setItem(row, 2, QTableWidgetItem(event['end_time']))
                self.event_table.setItem(row, 3, QTableWidgetItem(event['theme']))
                self.event_table.setItem(row, 4, QTableWidgetItem(event['description']))

        self.event_table.resizeColumnsToContents()

    def export_to_docx(self):
        if not self.schedule_manager.get_schedule():
            QMessageBox.warning(self, "Ошибка", "Нет событий для экспорта.")
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить расписание", "", "Документ Word (*.docx)")

        if not file_name:
            return

        try:
            export_schedule_to_docx(self.schedule_manager.get_schedule(), file_name)
            QMessageBox.information(self, "Экспорт", f"Все события успешно экспортированы в {file_name}.")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить документ: {e}")

    def save_schedule_to_file(self):
        save_schedule_to_file(self.schedule_manager)

    def closeEvent(self, event):
        self.save_schedule_to_file()
        event.accept()