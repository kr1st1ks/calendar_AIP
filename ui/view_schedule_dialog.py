from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QCalendarWidget, QTableWidget, QTableWidgetItem, QPushButton, QComboBox
)
from PyQt5.QtCore import QDate, Qt, QRect
from PyQt5.QtGui import QTextCharFormat, QBrush, QColor, QFont


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
        # Уменьшаем отступы и увеличиваем область текста
        text_rect = QRect(rect.x() + 3, rect.y() + 5, rect.width() - 6, rect.height() - 10)
        # Увеличиваем шрифт для цифр
        font = QFont()
        font.setPixelSize(14)  # Увеличиваем размер шрифта
        painter.setFont(font)
        painter.drawText(text_rect, Qt.AlignRight | Qt.AlignTop, str(date.day()))


class ViewScheduleDialog(QDialog):
    def __init__(self, schedule_manager):
        super().__init__()
        self.schedule_manager = schedule_manager
        self.setWindowTitle("Просмотреть расписание")
        self.setStyleSheet("""
            QDialog {
                background-color: rgb(240, 240, 240);
            }
            QLabel {
                font-size: 14px;
                color: rgb(62, 93, 7);
            }
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
            QHeaderView::section:hover {
                background-color: rgb(62, 84, 7);
                outline: 5px;
            }
            QComboBox {
                background-color: rgb(230, 224, 200);
                color: rgb(62, 93, 7);
                font-size: 14px;
                padding: 8px;
                border-radius: 5px;
                border: 1px solid #ddd;
            }
            QComboBox:hover {
                background-color: rgb(209, 201, 169);
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                width: 10px;
                height: 10px;
            }
            QComboBox QAbstractItemView {
                background-color: rgb(230, 224, 200);
                color: rgb(62, 93, 7);
                selection-background-color: rgb(209, 201, 169);
                border-radius: 5px;
            }
        """)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        filter_layout = QHBoxLayout()
        self.layout.addLayout(filter_layout)

        start_date_label = QLabel("Выберите дату начала:")
        filter_layout.addWidget(start_date_label)
        start_date_input = RoundedCalendar()
        start_date_input.setSelectedDate(QDate.currentDate())
        # Увеличиваем минимальный размер календаря
        start_date_input.setMinimumSize(400, 300)
        start_date_input.setGridVisible(True)  # Включаем сетку для лучшей читаемости
        start_date_input.setStyleSheet("""
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
                border-radius: 18px;
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
        filter_layout.addWidget(start_date_input)

        range_label = QLabel("Выберите диапазон:")
        filter_layout.addWidget(range_label)
        date_range_input = QComboBox()
        date_range_input.addItem("1 неделя")
        date_range_input.addItem("1 месяц")
        date_range_input.addItem("3 месяца")
        filter_layout.addWidget(date_range_input)

        theme_filter_label = QLabel("Фильтр по теме:")
        filter_layout.addWidget(theme_filter_label)
        theme_filter_input = QComboBox()
        theme_filter_input.addItem("Все темы")
        all_themes = set()
        for date, events in self.schedule_manager.get_schedule().items():
            for event in events:
                all_themes.add(event['theme'])
        for theme in sorted(all_themes):
            theme_filter_input.addItem(theme)
        filter_layout.addWidget(theme_filter_input)

        filter_button = QPushButton("Применить фильтр")
        filter_layout.addWidget(filter_button)

        schedule_table = QTableWidget()
        schedule_table.setColumnCount(5)
        schedule_table.setHorizontalHeaderLabels(["Дата", "Время начала", "Время окончания", "Тема", "Описание"])
        self.layout.addWidget(schedule_table)

        def populate_table(filtered_schedule=None):
            schedule_table.setRowCount(0)
            data = self.schedule_manager.get_schedule().items() if filtered_schedule is None else filtered_schedule.items()
            selected_start_date = start_date_input.selectedDate()
            selected_range = date_range_input.currentText()
            if selected_range == "1 неделя":
                end_date = selected_start_date.addDays(7)
            elif selected_range == "1 месяц":
                end_date = selected_start_date.addMonths(1)
            elif selected_range == "3 месяца":
                end_date = selected_start_date.addMonths(3)
            selected_theme = theme_filter_input.currentText()
            for date, events in sorted(data):
                row_date = QDate.fromString(date, "yyyy-MM-dd")
                if selected_start_date <= row_date <= end_date:
                    for event in sorted(events, key=lambda e: e['start_time']):
                        if selected_theme == "Все темы" or event['theme'] == selected_theme:
                            row = schedule_table.rowCount()
                            schedule_table.insertRow(row)
                            schedule_table.setItem(row, 0, QTableWidgetItem(date))
                            schedule_table.setItem(row, 1, QTableWidgetItem(event['start_time']))
                            schedule_table.setItem(row, 2, QTableWidgetItem(event['end_time']))
                            schedule_table.setItem(row, 3, QTableWidgetItem(event['theme']))
                            schedule_table.setItem(row, 4, QTableWidgetItem(event['description']))

        def apply_filter():
            filtered_schedule = {}
            selected_start_date = start_date_input.selectedDate().toString("yyyy-MM-dd")
            selected_range = date_range_input.currentText()
            if selected_range == "1 неделя":
                end_date = start_date_input.selectedDate().addDays(7)
            elif selected_range == "1 месяц":
                end_date = start_date_input.selectedDate().addMonths(1)
            elif selected_range == "3 месяца":
                end_date = start_date_input.selectedDate().addMonths(3)
            for date, events in self.schedule_manager.get_schedule().items():
                row_date = QDate.fromString(date, "yyyy-MM-dd")
                if start_date_input.selectedDate() <= row_date <= end_date:
                    filtered_schedule[date] = events
            populate_table(filtered_schedule)

        filter_button.clicked.connect(apply_filter)
        populate_table()

        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.close)
        self.layout.addWidget(close_button)