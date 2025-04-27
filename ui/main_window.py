from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QLabel, QLineEdit, QCalendarWidget, QTableWidget,
    QTableWidgetItem, QTimeEdit, QTextEdit, QMessageBox, QComboBox,
    QFileDialog, QSplitter, QFrame
)
from PyQt5.QtCore import Qt, QTime, QDate, QRect
from PyQt5.QtGui import QTextCharFormat, QBrush, QColor, QFont
from data.schedule_manager import ScheduleManager
from ui.add_event_dialog import AddEventDialog
from ui.edit_event_dialog import EditEventDialog
from ui.view_schedule_dialog import ViewScheduleDialog
from export.export_to_docx import export_schedule_to_docx
from utils.file_utils import load_schedule_from_file, save_schedule_to_file

class RoundedCalendar(QCalendarWidget):
    def paintCell(self, painter, rect, date):
        if date == self.selectedDate():
            painter.setBrush(QBrush(QColor(139, 93, 36)))  # Цвет фона выделенной ячейки
        else:
            painter.setBrush(QBrush(QColor(240, 240, 240)))  # Обычный фон

        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 5, 5)  # Скругленные углы

        if date.month() != self.monthShown():  # Дни предыдущего или следующего месяца
            text_color = QColor(180, 180, 180)  # Более бледный цвет
        elif date.dayOfWeek() in [6, 7]:  # Суббота и воскресенье
            text_color = Qt.red
        else:
            text_color = Qt.black if date != self.selectedDate() else Qt.white

        painter.setPen(text_color)
        text_rect = QRect(rect.x() + 5, rect.y() + 10, rect.width() - 20, rect.height() - 18)
        painter.drawText(text_rect, Qt.AlignRight | Qt.AlignTop, str(date.day()))

class ScheduleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Планировщик расписания")
        self.setGeometry(100, 100, 1000, 800)

        self.schedule_manager = ScheduleManager()

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        self.add_event_button = QPushButton("Добавить событие")
        self.add_event_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(62, 93, 7); 
                color: white; 
                font-size: 14px; 
                padding: 10px; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: rgb(62, 84, 7);
            }
        """)
        self.add_event_button.clicked.connect(self.show_add_event_dialog)
        self.button_layout.addWidget(self.add_event_button)

        self.view_schedule_button = QPushButton("Просмотреть расписание")
        self.view_schedule_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(139, 93, 36); 
                color: white; 
                font-size: 14px; 
                padding: 10px; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: rgb(122, 80, 28);
            }
        """)
        self.view_schedule_button.clicked.connect(self.show_view_schedule_dialog)
        self.button_layout.addWidget(self.view_schedule_button)

        self.export_button = QPushButton("Экспортировать в .docx")
        self.export_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(230, 224, 200); 
                color: black; 
                font-size: 14px; 
                padding: 10px; 
                border-radius: 5px; 
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgb(209, 201, 169);
            }
        """)
        self.export_button.clicked.connect(self.export_to_docx)
        self.button_layout.addWidget(self.export_button)

        self.calendar = RoundedCalendar()
        self.calendar.setVerticalHeaderFormat(self.calendar.NoVerticalHeader)
        self.calendar.setStyleSheet("""
            #qt_calendar_navigationbar {
                background-color: rgb(139, 93, 36);
                min-height: 60px;
                max-height: 60px;
                padding: 10px;
                border-radius: 5px;
            }
            #qt_calendar_prevmonth, #qt_calendar_nextmonth {
                border: none;
                margin-top: 0px;
                color: white;
                min-width: 50px;
                max-width: 50px;
                min-height: 50px;
                max-height: 50px;
                border Cradius: 18px;
                font-weight: bold;
                qproperty-icon: none;
                background-color: transparent;
            }
            #qt_calendar_prevmonth {
                qproperty-text: "<-";
            }
            #qt_calendar_nextmonth {
                qproperty-text: "->";
            }
            #qt_calendar_prevmonth:hover, #qt_calendar_nextmonth:hover {
                background-color: rgba(225, 225, 225, 100);
            }
            #qt_calendar_prevmonth:pressed, #qt_calendar_nextmonth:pressed {
                background-color: rgba(235, 235, 235, 100);
            }
            #qt_calendar_yearbutton, #qt_calendar_monthbutton {
                color: white;
                margin: 18px;
                min-width: 100px;
                max-width: 100px;
                border-radius: 18px;
            }
            #qt_calendar_yearbutton:hover, #qt_calendar_monthbutton:hover {
                background-color: rgba(225, 225, 225, 100);
            }
            #qt_calendar_yearbutton:pressed, #qt_calendar_monthbutton:pressed {
                background-color: rgba(235, 235, 235, 100);
            }
            #qt_calendar_yearedit {
                min-width: 100px;
                max-width: 100px;
                color: white;
                background: transparent;
            }
            #qt_calendar_yearedit::up-button {
                width: 30px;
                subcontrol-position: right;
            }
            #qt_calendar_yearedit::down-button {
                width: 30px;
                subcontrol-position: left;
            }
            CalendarWidget QToolButton QMenu {
                background-color: white;
            }
            CalendarWidget QToolButton QMenu::item {
                padding: 10px;
            }
            CalendarWidget QToolButton QMenu::item:selected:enabled {
                background-color: rgb(230, 230, 230);
            }
            CalendarWidget QToolButton::menu-indicator {
                image: none;
                subcontrol-position: right center;
            }
            #qt_calendar_calendarview {
                outline: 5px;
                selection-background-color: rgb(139, 93, 36);
            }
        """)
        self.calendar.clicked.connect(self.update_schedule_view)
        self.calendar.setMinimumDate(QDate(1, 1, 1))
        self.calendar.setMaximumDate(QDate(9999, 1, 1))
        self.layout.addWidget(self.calendar)

        self.toggle_button = QPushButton("Скрыть события")
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(62, 93, 7); 
                color: white; 
                font-size: 14px; 
                padding: 10px; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: rgb(62, 84, 7);
            }
        """)
        self.toggle_button.clicked.connect(self.toggle_hidden_frame)
        self.layout.addWidget(self.toggle_button)

        self.hidden_frame = QWidget()
        self.hidden_layout = QVBoxLayout()
        self.hidden_frame.setLayout(self.hidden_layout)
        self.layout.addWidget(self.hidden_frame)

        self.event_table = QTableWidget()
        self.event_table.setColumnCount(5)
        self.event_table.setHorizontalHeaderLabels(["Дата", "Начало", "Конец", "Тема", "Описание"])
        self.event_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                font-size: 14px;
                background-color: rgb(230, 224, 200);
                gridline-color: #ddd;
                padding: 5px;
                border-radius: 5px;
                outline: 0px;
            }
            QTableCornerButton::section {
                background-color: rgb(230, 224, 200);
            }
            QTableWidget::item {
                padding: 10px;
                outline: 0px;
            }
            QTableWidget::item:hover {
                background-color: #f1f1f1;
                padding: 10px;
                border-radius: 5px;
                outline: 0px;
            }
            QTableWidget::item:selected:enabled {
                background-color: #f1f1f1;
                padding: 10px;
                border-radius: 5px;
                outline: 0px;
                color: black;
                border: none;
            }
            QTableWidget::item:selected:disabled {
                outline: 5px;
                border: none;
            }
            QHeaderView {
                background-color: rgb(230, 224, 200);
            }
            QHeaderView::section {
                background-color: rgb(62, 93, 7);
                color: white;
                font-size: 16px;
                padding: 10px 10px;
                margin: 1px;
                border-radius: 5px;
                min-height: 20px;
                max-height: 20px;
                outline: 1px;
            }
            QHeaderView::section:hover 먹다
                background-color: rgb(62, 84, 7);
                outline: 5px;
            }
            QHeaderView::section:selected:enabled {
                selection-background-color: rgb(62, 84, 7);
                outline: 5px;
            }
        """)
        self.hidden_layout.addWidget(self.event_table)

        self.button_layout_low = QHBoxLayout()
        self.hidden_layout.addLayout(self.button_layout_low)

        self.delete_event_button = QPushButton("Удалить событие")
        self.delete_event_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(139, 93, 36); 
                color: white; 
                font-size: 14px; 
                padding: 10px; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: rgb(122, 80, 28);
            }
        """)
        self.delete_event_button.clicked.connect(self.delete_event)
        self.button_layout_low.addWidget(self.delete_event_button)

        self.edit_event_button = QPushButton("Редактировать событие")
        self.edit_event_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(62, 93, 7); 
                color: white; 
                font-size: 14px; 
                padding: 10px; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: rgb(62, 84, 7);
            }
        """)
        self.edit_event_button.clicked.connect(self.edit_event)
        self.button_layout_low.addWidget(self.edit_event_button)

        self.search_layout = QHBoxLayout()
        self.hidden_layout.addLayout(self.search_layout)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите текст для поиска...")
        self.search_input.setStyleSheet(
            "background-color: rgb(230, 224, 200); font-size: 14px; padding: 8px; border-radius: 5px;")
        self.search_layout.addWidget(self.search_input)

        self.search_button = QPushButton("Поиск")
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(139, 93, 36); 
                color: white; 
                font-size: 14px; 
                padding: 10px; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: rgb(122, 80, 28);
            }
        """)
        self.search_button.clicked.connect(self.search_events)
        self.search_layout.addWidget(self.search_button)
        self.search_input.returnPressed.connect(self.search_button.click)

        self.calendar.selectionChanged.connect(self.add_event_dots)
        self.calendar.currentPageChanged.connect(self.add_event_dots)

        self.load_schedule_from_file()
        self.update_schedule_view()
        self.add_event_dots()

    def toggle_hidden_frame(self):
        self.hidden_frame.setVisible(not self.hidden_frame.isVisible())
        self.toggle_button.setText("Отобразить события" if not self.hidden_frame.isVisible() else "Скрыть события")

    def add_event_dots(self):
        self.calendar.setDateTextFormat(QDate(), QTextCharFormat())
        text_format = QTextCharFormat()
        font = QFont()
        font.setBold(True)
        text_format.setFont(font)
        text_format.setFontUnderline(True)
        for date_str in self.schedule_manager.get_schedule():
            date = QDate.fromString(date_str, "yyyy-MM-dd")
            if date.isValid():
                self.calendar.setDateTextFormat(date, text_format)

    def load_schedule_from_file(self):
        load_schedule_from_file(self.schedule_manager)

    def show_add_event_dialog(self):
        dialog = AddEventDialog(self.calendar.selectedDate().toString("yyyy-MM-dd"), self.schedule_manager)
        dialog.exec()
        self.update_schedule_view()
        self.add_event_dots()

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
        self.add_event_dots()

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
        dialog.exec()
        self.update_schedule_view()
        self.add_event_dots()

    def show_view_schedule_dialog(self):
        dialog = ViewScheduleDialog(self.schedule_manager)
        dialog.exec()

    def search_events(self):
        search_term = self.search_input.text().strip().lower()
        if not search_term:
            QMessageBox.warning(self, "Ошибка", "Введите текст для поиска.")
            return
        filtered_schedule = self.schedule_manager.search_events(search_term)
        self.update_schedule_view(filtered_schedule)

    def update_schedule_view(self, filtered_schedule=None):
        self.event_table.setRowCount(0)
        if filtered_schedule is None:
            selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
            events = self.schedule_manager.get_schedule(selected_date)
            data = {selected_date: events}.items()
        else:
            if isinstance(filtered_schedule, QDate):
                selected_date = filtered_schedule.toString("yyyy-MM-dd")
                events = self.schedule_manager.get_schedule(selected_date)
                data = {selected_date: events}.items()
            elif isinstance(filtered_schedule, dict):
                data = filtered_schedule.items()
            else:
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

if __name__ == '__main__':
    app = QApplication([])
    window = ScheduleApp()
    window.show()
    app.exec()